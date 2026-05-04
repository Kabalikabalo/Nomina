from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from sql_generator import *


# =============================================================================
# Nomina SQL Helper Functions
# -----------------------------------------------------------------------------
# These helpers sit on top of NominaSQLBuilder.
#
# They do not replace the builder.
# They just reduce repeated code for common patterns:
# - concept -> word -> name
# - concept -> word -> word -> name
# - base name -> variant name
# - word parts -> compound word -> name
# =============================================================================


@dataclass
class MeaningEdge:
    concept_slug: str
    explanation: str
    certainty: float = 0.90


@dataclass
class ChainEdge:
    from_slug: str
    to_slug: str
    edge_type_code: str
    explanation: str
    certainty: float = 0.88


@dataclass
class CompoundPart:
    word: WordNode
    explanation_to_compound: str
    certainty_to_compound: float = 0.88
    concept_edges: list[MeaningEdge] = field(default_factory=list)


def ensure_languages(b: NominaSQLBuilder, languages: Iterable[Language]) -> None:
    for language in languages:
        b.ensure_language(language)


def ensure_concepts(b: NominaSQLBuilder, concepts: Iterable[ConceptNode]) -> None:
    for concept in concepts:
        b.ensure_concept(concept)


def require_existing_node(
    b: NominaSQLBuilder,
    *,
    node_type: str,
    slug: str,
    label: str | None = None,
    canonical_key: str | None = None,
    description_short: str | None = None,
    lookup_slugs: list[str] | None = None,
    lookup_labels: list[str] | None = None,
    lookup_canonical_keys: list[str] | None = None,
) -> str:
    """
    Registers an existing node in the current builder without creating it.

    Use this when a previous batch already created a node, but this new batch
    needs a variable handle for it.

    Example:
        require_existing_node(
            b,
            node_type="concept",
            slug="star-concept",
            label="star",
            canonical_key="star",
        )
    """

    label = label or slug
    canonical_key = canonical_key or slug.replace("-", " ")
    description_short = description_short or f"Existing {node_type} node: {label}."

    v = var_name("n", slug)

    b.node_vars[slug] = v
    b.declare(v, "uuid")

    all_slugs = uniq([slug, *(lookup_slugs or [])])
    b.node_lookup_slugs.update(all_slugs)

    if node_type == "name":
        b.name_slugs.add(slug)
    elif node_type == "word":
        b.word_slugs.add(slug)
    elif node_type == "concept":
        b.concept_slugs.add(slug)

    condition = b.lookup_condition(
        slug=slug,
        label=label,
        canonical_key=canonical_key,
        lookup_slugs=lookup_slugs,
        lookup_labels=lookup_labels,
        lookup_canonical_keys=lookup_canonical_keys,
    )

    b.add(f"""
---------------------------------------------------------------------------
-- Required existing node: {node_type} / {slug}
---------------------------------------------------------------------------

SELECT id INTO {v}
FROM nodes
WHERE node_type = {sql_literal(node_type)}
  AND {condition}
LIMIT 1;

IF {v} IS NULL THEN
  RAISE EXCEPTION {sql_literal(f"Required existing {node_type} node not found: {slug}")};
END IF;
""")

    return v


def add_direct_name(
    b: NominaSQLBuilder,
    *,
    word: WordNode,
    name: NameNode,
    concept_edges: list[MeaningEdge],
    word_to_name_explanation: str,
    word_to_name_certainty: float = 0.90,
    lineage_title: str | None = None,
    lineage_summary: str | None = None,
    lineage_certainty: float | None = None,
    source_group: str | list[str] | None = None,
) -> None:
    """
    Pattern:
        concept(s) -> word -> name

    Best for:
        Welsh seren -> Seren
        Japanese sora -> Sora
        Arabic nūr -> Nur
        Sanskrit jyotis -> Jyoti
    """

    source_group = source_group or name.source_group

    b.ensure_word(word)
    b.ensure_name(name)

    for concept_edge in concept_edges:
        b.ensure_edge(Edge(
            from_slug=concept_edge.concept_slug,
            to_slug=word.slug,
            edge_type_code="meaning_of",
            certainty=concept_edge.certainty,
            explanation=concept_edge.explanation,
            source_group=source_group,
        ))

    b.ensure_edge(Edge(
        from_slug=word.slug,
        to_slug=name.slug,
        edge_type_code="element_of",
        certainty=word_to_name_certainty,
        explanation=word_to_name_explanation,
        source_group=source_group,
    ))

    concept_slugs = uniq(edge.concept_slug for edge in concept_edges)

    if concept_slugs:
        path = [
            concept_slugs,
            [word.slug],
            [name.slug],
        ]
    else:
        path = [
            [word.slug],
            [name.slug],
        ]

    b.ensure_primary_lineage(Lineage(
        name_slug=name.slug,
        title=lineage_title or f"Etymology of {name.display_name}",
        summary=lineage_summary or f"{name.display_name} derives from {word.label}.",
        path=path,
        certainty=lineage_certainty if lineage_certainty is not None else word_to_name_certainty,
        source_group=source_group,
    ))


def add_word_chain_name(
    b: NominaSQLBuilder,
    *,
    words: list[WordNode],
    name: NameNode,
    concept_edges: list[MeaningEdge],
    chain_edges: list[ChainEdge],
    final_word_to_name_explanation: str,
    final_word_to_name_certainty: float = 0.90,
    lineage_title: str | None = None,
    lineage_summary: str | None = None,
    lineage_certainty: float | None = None,
    source_group: str | list[str] | None = None,
) -> None:
    """
    Pattern:
        concept(s) -> word1 -> word2 -> ... -> name

    Best for:
        Latin stella -> Old French estelle -> Estelle
        Persian yāsamīn -> Arabic yāsamīn -> English jasmine -> Jasmine
        Latin caelum -> Spanish cielo -> Cielo
    """

    if not words:
        raise ValueError("add_word_chain_name requires at least one WordNode")

    if len(chain_edges) != max(0, len(words) - 1):
        raise ValueError(
            "chain_edges must have exactly len(words) - 1 entries"
        )

    source_group = source_group or name.source_group

    for word in words:
        b.ensure_word(word)

    b.ensure_name(name)

    first_word = words[0]
    final_word = words[-1]

    for concept_edge in concept_edges:
        b.ensure_edge(Edge(
            from_slug=concept_edge.concept_slug,
            to_slug=first_word.slug,
            edge_type_code="meaning_of",
            certainty=concept_edge.certainty,
            explanation=concept_edge.explanation,
            source_group=source_group,
        ))

    for chain_edge in chain_edges:
        b.ensure_edge(Edge(
            from_slug=chain_edge.from_slug,
            to_slug=chain_edge.to_slug,
            edge_type_code=chain_edge.edge_type_code,
            certainty=chain_edge.certainty,
            explanation=chain_edge.explanation,
            source_group=source_group,
        ))

    b.ensure_edge(Edge(
        from_slug=final_word.slug,
        to_slug=name.slug,
        edge_type_code="element_of",
        certainty=final_word_to_name_certainty,
        explanation=final_word_to_name_explanation,
        source_group=source_group,
    ))

    concept_slugs = uniq(edge.concept_slug for edge in concept_edges)

    path: list[list[str]] = []

    if concept_slugs:
        path.append(concept_slugs)

    for word in words:
        path.append([word.slug])

    path.append([name.slug])

    b.ensure_primary_lineage(Lineage(
        name_slug=name.slug,
        title=lineage_title or f"Etymology of {name.display_name}",
        summary=lineage_summary or f"{name.display_name} derives through the {' → '.join(w.label for w in words)} route.",
        path=path,
        certainty=lineage_certainty if lineage_certainty is not None else final_word_to_name_certainty,
        source_group=source_group,
    ))


def add_name_variant(
    b: NominaSQLBuilder,
    *,
    variant: NameNode,
    base_slug: str,
    variant_explanation: str,
    variant_certainty: float = 0.88,
    lineage_title: str | None = None,
    lineage_summary: str | None = None,
    lineage_certainty: float | None = None,
    lineage_path: list[list[str]] | None = None,
    source_group: str | list[str] | None = None,
) -> None:
    """
    Pattern:
        variant_name -> base_name

    Best for:
        Aakash -> Akash
        Noor -> Nur
        Zia -> Ziya
        Lucy -> Lucia

    Important:
        base_slug must already be registered in this builder.
        Use require_existing_node(...) if the base was created in an earlier batch.
    """

    if base_slug not in b.node_vars:
        raise KeyError(
            f"Base node '{base_slug}' is not registered in this builder. "
            f"Use require_existing_node(...) first."
        )

    source_group = source_group or variant.source_group

    b.ensure_name(variant)

    b.ensure_edge(Edge(
        from_slug=variant.slug,
        to_slug=base_slug,
        edge_type_code="variant_of",
        certainty=variant_certainty,
        explanation=variant_explanation,
        source_group=source_group,
    ))

    path = lineage_path or [
        [base_slug],
        [variant.slug],
    ]

    b.ensure_primary_lineage(Lineage(
        name_slug=variant.slug,
        title=lineage_title or f"Etymology of {variant.display_name}",
        summary=lineage_summary or f"{variant.display_name} is a variant of {base_slug}.",
        path=path,
        certainty=lineage_certainty if lineage_certainty is not None else variant_certainty,
        source_group=source_group,
    ))


def add_compound_name(
    b: NominaSQLBuilder,
    *,
    parts: list[CompoundPart],
    compound_word: WordNode,
    name: NameNode,
    compound_meaning_edges: list[MeaningEdge],
    compound_to_name_explanation: str,
    compound_to_name_certainty: float = 0.88,
    lineage_title: str | None = None,
    lineage_summary: str | None = None,
    lineage_certainty: float | None = None,
    lineage_path: list[list[str]] | None = None,
    source_group: str | list[str] | None = None,
) -> None:
    """
    Pattern:
        concept(s) -> word parts -> compound word -> name

    Best for:
        Pankaj = mud + born -> mud-born / lotus
        Ambuja = water + born -> water-born / lotus
        Aygül = moon + rose
        Gülnur = rose + light
    """

    if not parts:
        raise ValueError("add_compound_name requires at least one CompoundPart")

    source_group = source_group or name.source_group

    for part in parts:
        b.ensure_word(part.word)

    b.ensure_word(compound_word)
    b.ensure_name(name)

    for part in parts:
        for concept_edge in part.concept_edges:
            b.ensure_edge(Edge(
                from_slug=concept_edge.concept_slug,
                to_slug=part.word.slug,
                edge_type_code="meaning_of",
                certainty=concept_edge.certainty,
                explanation=concept_edge.explanation,
                source_group=source_group,
            ))

    for concept_edge in compound_meaning_edges:
        b.ensure_edge(Edge(
            from_slug=concept_edge.concept_slug,
            to_slug=compound_word.slug,
            edge_type_code="meaning_of",
            certainty=concept_edge.certainty,
            explanation=concept_edge.explanation,
            source_group=source_group,
        ))

    for part in parts:
        b.ensure_edge(Edge(
            from_slug=part.word.slug,
            to_slug=compound_word.slug,
            edge_type_code="element_of",
            certainty=part.certainty_to_compound,
            explanation=part.explanation_to_compound,
            source_group=source_group,
        ))

    b.ensure_edge(Edge(
        from_slug=compound_word.slug,
        to_slug=name.slug,
        edge_type_code="element_of",
        certainty=compound_to_name_certainty,
        explanation=compound_to_name_explanation,
        source_group=source_group,
    ))

    if lineage_path is None:
        part_concepts = uniq(
            edge.concept_slug
            for part in parts
            for edge in part.concept_edges
        )

        compound_concepts = uniq(
            edge.concept_slug
            for edge in compound_meaning_edges
        )

        first_group = uniq([*part_concepts, *compound_concepts])

        path: list[list[str]] = []

        if first_group:
            path.append(first_group)

        path.append([part.word.slug for part in parts])
        path.append([compound_word.slug])
        path.append([name.slug])
    else:
        path = lineage_path

    b.ensure_primary_lineage(Lineage(
        name_slug=name.slug,
        title=lineage_title or f"Etymology of {name.display_name}",
        summary=lineage_summary or f"{name.display_name} derives from {compound_word.label}.",
        path=path,
        certainty=lineage_certainty if lineage_certainty is not None else compound_to_name_certainty,
        source_group=source_group,
    ))
