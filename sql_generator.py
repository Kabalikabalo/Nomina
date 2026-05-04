from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


# =============================================================================
# Nomina SQL Builder
# -----------------------------------------------------------------------------
# This script does not connect to Supabase.
# It generates reviewable PostgreSQL / Supabase SQL.
#
# Safety rule:
# - Existing nodes are reused.
# - Existing concept / word / name details are NOT overwritten by default.
# - To intentionally revise an existing word/name, set update_existing_node=True
#   and/or update_existing_detail=True on that WordNode or NameNode.
# =============================================================================


def uniq(values: Iterable[str | None]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []

    for value in values:
        if value is None:
            continue

        text = str(value)

        if text not in seen:
            seen.add(text)
            out.append(text)

    return out


def sql_literal(value: str | None) -> str:
    if value is None:
        return "NULL"
    return "'" + value.replace("'", "''") + "'"


def sql_jsonb_array_literal(raw_json: str) -> str:
    return f"{sql_literal(raw_json)}::jsonb"


def sql_in(values: Iterable[str]) -> str:
    clean = uniq(values)
    if not clean:
        return "(NULL)"
    return "(" + ", ".join(sql_literal(v) for v in clean) + ")"


def sql_lower_in(values: Iterable[str]) -> str:
    return sql_in([v.lower() for v in uniq(values)])


def var_name(prefix: str, slug: str) -> str:
    safe = "".join(ch if ch.isalnum() else "_" for ch in slug.lower())
    while "__" in safe:
        safe = safe.replace("__", "_")
    return f"{prefix}_{safe.strip('_')}"


def source_groups(value: str | list[str]) -> list[str]:
    if isinstance(value, str):
        return [value]
    return value


@dataclass
class Language:
    slug: str
    name: str
    alternative_names_json: str = "[]"
    language_family: str | None = None
    period_label: str | None = None
    region_note: str | None = None
    additional_notes: str | None = None


@dataclass
class Source:
    title: str
    author: str | None
    source_type: str
    url: str | None
    citation_text: str
    notes: str | None = None


@dataclass
class ConceptNode:
    slug: str
    label: str
    canonical_key: str
    description_short: str
    description: str
    source_group: str | list[str]

    lookup_slugs: list[str] = field(default_factory=list)
    lookup_labels: list[str] = field(default_factory=list)
    lookup_canonical_keys: list[str] = field(default_factory=list)

    update_existing_node: bool = False
    update_existing_detail: bool = False


@dataclass
class WordNode:
    slug: str
    label: str
    canonical_key: str
    description_short: str

    language_slug: str
    display_text: str
    original_script: str | None
    transliteration: str | None
    word_type: str | None
    literal_meaning: str | None
    grammar_notes: str | None
    additional_notes: str | None
    source_group: str | list[str]

    lookup_slugs: list[str] = field(default_factory=list)
    lookup_labels: list[str] = field(default_factory=list)
    lookup_canonical_keys: list[str] = field(default_factory=list)

    update_existing_node: bool = False
    update_existing_detail: bool = False


@dataclass
class NameNode:
    slug: str
    label: str
    canonical_key: str
    description_short: str

    display_name: str
    original_script: str | None
    transliteration: str | None
    primary_language_slug: str
    gender_usage: str | None
    short_summary: str | None
    long_summary: str | None
    literary_notes: str | None
    cultural_notes: str | None
    pronunciation_notes: str | None
    certainty_notes: str | None
    source_group: str | list[str]

    lookup_slugs: list[str] = field(default_factory=list)
    lookup_labels: list[str] = field(default_factory=list)
    lookup_canonical_keys: list[str] = field(default_factory=list)

    update_existing_node: bool = False
    update_existing_detail: bool = False


@dataclass
class Edge:
    from_slug: str
    to_slug: str
    edge_type_code: str
    certainty: float
    explanation: str
    source_group: str | list[str]


@dataclass
class Lineage:
    name_slug: str
    title: str
    summary: str
    path: list[list[str]]
    certainty: float
    source_group: str | list[str]


class NominaSQLBuilder:
    def __init__(self) -> None:
        self.declarations: dict[str, str] = {}
        self.statements: list[str] = []

        self.language_vars: dict[str, str] = {}
        self.source_vars: dict[str, str] = {}
        self.node_vars: dict[str, str] = {}

        self.node_lookup_slugs: set[str] = set()
        self.name_slugs: set[str] = set()
        self.word_slugs: set[str] = set()
        self.concept_slugs: set[str] = set()
        self.edge_specs: list[Edge] = []
        self.lineage_specs: list[Lineage] = []

    def declare(self, name: str, dtype: str) -> None:
        self.declarations[name] = dtype

    def add(self, sql: str) -> None:
        self.statements.append(sql.strip())

    def source_expr(self, group_or_groups: str | list[str]) -> str:
        groups = source_groups(group_or_groups)
        missing = [g for g in groups if g not in self.source_vars]
        if missing:
            raise KeyError(f"Unknown source group(s): {missing}")
        return " || ".join(self.source_vars[g] for g in groups)

    def language_var(self, slug: str) -> str:
        if slug not in self.language_vars:
            raise KeyError(f"Language has not been ensured yet: {slug}")
        return self.language_vars[slug]

    def node_var(self, slug: str) -> str:
        if slug not in self.node_vars:
            raise KeyError(f"Node has not been ensured yet: {slug}")
        return self.node_vars[slug]

    def include_edge_types(self) -> None:
        self.add("""
---------------------------------------------------------------------------
-- Edge types
---------------------------------------------------------------------------

IF NOT EXISTS (SELECT 1 FROM edge_types WHERE code = 'meaning_of') THEN
  INSERT INTO edge_types (code, label) VALUES ('meaning_of', 'meaning of');
END IF;

IF NOT EXISTS (SELECT 1 FROM edge_types WHERE code = 'element_of') THEN
  INSERT INTO edge_types (code, label) VALUES ('element_of', 'element of');
END IF;

IF NOT EXISTS (SELECT 1 FROM edge_types WHERE code = 'variant_of') THEN
  INSERT INTO edge_types (code, label) VALUES ('variant_of', 'variant of');
END IF;

IF NOT EXISTS (SELECT 1 FROM edge_types WHERE code = 'evolves_to') THEN
  INSERT INTO edge_types (code, label) VALUES ('evolves_to', 'evolves to');
END IF;
""")

    def ensure_language(self, language: Language) -> str:
        v = var_name("l", language.slug)
        self.language_vars[language.slug] = v
        self.declare(v, "uuid")

        self.add(f"""
---------------------------------------------------------------------------
-- Language: {language.name}
---------------------------------------------------------------------------

SELECT id INTO {v}
FROM languages
WHERE slug = {sql_literal(language.slug)}
   OR lower(name) = lower({sql_literal(language.name)})
LIMIT 1;

IF {v} IS NULL THEN
  INSERT INTO languages
    (
      name,
      slug,
      alternative_names,
      language_family,
      period_label,
      region_note,
      additional_notes,
      source_ids,
      created_at,
      updated_at
    )
  VALUES
    (
      {sql_literal(language.name)},
      {sql_literal(language.slug)},
      {sql_jsonb_array_literal(language.alternative_names_json)},
      {sql_literal(language.language_family)},
      {sql_literal(language.period_label)},
      {sql_literal(language.region_note)},
      {sql_literal(language.additional_notes)},
      '[]'::jsonb,
      NOW(),
      NOW()
    )
  RETURNING id INTO {v};
END IF;
""")
        return v

    def ensure_sources(self, group_name: str, sources: list[Source]) -> str:
        if not sources:
            raise ValueError("ensure_sources requires at least one Source")

        v = var_name("src", group_name)
        self.source_vars[group_name] = v
        self.declare(v, "jsonb")

        inserts: list[str] = []
        titles: list[str] = []

        for source in sources:
            titles.append(source.title)
            inserts.append(f"""
IF NOT EXISTS (SELECT 1 FROM sources WHERE title = {sql_literal(source.title)}) THEN
  INSERT INTO sources
    (title, author, source_type, url, citation_text, notes, created_at, updated_at)
  VALUES
    (
      {sql_literal(source.title)},
      {sql_literal(source.author)},
      {sql_literal(source.source_type)},
      {sql_literal(source.url)},
      {sql_literal(source.citation_text)},
      {sql_literal(source.notes)},
      NOW(),
      NOW()
    );
END IF;
""".strip())

        self.add(f"""
---------------------------------------------------------------------------
-- Sources: {group_name}
---------------------------------------------------------------------------

{chr(10).join(inserts)}

SELECT COALESCE(jsonb_agg(id::text), '[]'::jsonb)
INTO {v}
FROM sources
WHERE title IN {sql_in(titles)};
""")
        return v

    def lookup_condition(
        self,
        *,
        slug: str,
        label: str,
        canonical_key: str,
        lookup_slugs: list[str] | None = None,
        lookup_labels: list[str] | None = None,
        lookup_canonical_keys: list[str] | None = None,
    ) -> str:
        slugs = uniq([slug, *(lookup_slugs or [])])
        labels = uniq([label, *(lookup_labels or [])])
        keys = uniq([canonical_key, *(lookup_canonical_keys or [])])

        return f"""(
      slug IN {sql_in(slugs)}
      OR lower(canonical_key) IN {sql_lower_in(keys)}
      OR lower(display_label) IN {sql_lower_in(labels)}
    )"""

    def ensure_node(
        self,
        *,
        node_type: str,
        slug: str,
        label: str,
        canonical_key: str,
        description_short: str,
        lookup_slugs: list[str] | None = None,
        lookup_labels: list[str] | None = None,
        lookup_canonical_keys: list[str] | None = None,
        update_existing_node: bool = False,
    ) -> str:
        v = var_name("n", slug)
        self.node_vars[slug] = v
        self.declare(v, "uuid")

        all_slugs = uniq([slug, *(lookup_slugs or [])])
        self.node_lookup_slugs.update(all_slugs)

        conditions = self.lookup_condition(
            slug=slug,
            label=label,
            canonical_key=canonical_key,
            lookup_slugs=lookup_slugs,
            lookup_labels=lookup_labels,
            lookup_canonical_keys=lookup_canonical_keys,
        )

        if node_type == "name":
            self.name_slugs.add(slug)
        elif node_type == "word":
            self.word_slugs.add(slug)
        elif node_type == "concept":
            self.concept_slugs.add(slug)

        update_block = ""
        if update_existing_node:
            update_block = f"""
ELSE
  UPDATE nodes
  SET display_label = {sql_literal(label)},
      canonical_key = {sql_literal(canonical_key)},
      description_short = {sql_literal(description_short)},
      updated_at = NOW()
  WHERE id = {v};
"""

        self.add(f"""
---------------------------------------------------------------------------
-- Node: {node_type} / {slug}
---------------------------------------------------------------------------

SELECT id INTO {v}
FROM nodes
WHERE node_type = {sql_literal(node_type)}
  AND {conditions}
LIMIT 1;

IF {v} IS NULL THEN
  INSERT INTO nodes
    (node_type, slug, display_label, canonical_key, description_short, created_at, updated_at)
  VALUES
    (
      {sql_literal(node_type)},
      {sql_literal(slug)},
      {sql_literal(label)},
      {sql_literal(canonical_key)},
      {sql_literal(description_short)},
      NOW(),
      NOW()
    )
  RETURNING id INTO {v};
{update_block}END IF;
""")
        return v

    def ensure_concept(self, concept: ConceptNode) -> str:
        v = self.ensure_node(
            node_type="concept",
            slug=concept.slug,
            label=concept.label,
            canonical_key=concept.canonical_key,
            description_short=concept.description_short,
            lookup_slugs=concept.lookup_slugs,
            lookup_labels=concept.lookup_labels,
            lookup_canonical_keys=concept.lookup_canonical_keys,
            update_existing_node=concept.update_existing_node,
        )

        src = self.source_expr(concept.source_group)

        if concept.update_existing_detail:
            self.add(f"""
IF EXISTS (SELECT 1 FROM concepts WHERE node_id = {v}) THEN
  UPDATE concepts
  SET display_text = {sql_literal(concept.label)},
      canonical_key = {sql_literal(concept.canonical_key)},
      description = {sql_literal(concept.description)},
      source_ids = {src},
      updated_at = NOW()
  WHERE node_id = {v};
ELSE
  INSERT INTO concepts
    (node_id, display_text, canonical_key, description, source_ids, created_at, updated_at)
  VALUES
    (
      {v},
      {sql_literal(concept.label)},
      {sql_literal(concept.canonical_key)},
      {sql_literal(concept.description)},
      {src},
      NOW(),
      NOW()
    );
END IF;
""")
        else:
            self.add(f"""
IF NOT EXISTS (SELECT 1 FROM concepts WHERE node_id = {v}) THEN
  INSERT INTO concepts
    (node_id, display_text, canonical_key, description, source_ids, created_at, updated_at)
  VALUES
    (
      {v},
      {sql_literal(concept.label)},
      {sql_literal(concept.canonical_key)},
      {sql_literal(concept.description)},
      {src},
      NOW(),
      NOW()
    );
END IF;
""")

        return v

    def ensure_word(self, word: WordNode) -> str:
        v = self.ensure_node(
            node_type="word",
            slug=word.slug,
            label=word.label,
            canonical_key=word.canonical_key,
            description_short=word.description_short,
            lookup_slugs=word.lookup_slugs,
            lookup_labels=word.lookup_labels,
            lookup_canonical_keys=word.lookup_canonical_keys,
            update_existing_node=word.update_existing_node,
        )

        lang = self.language_var(word.language_slug)
        src = self.source_expr(word.source_group)

        if word.update_existing_detail:
            self.add(f"""
IF EXISTS (SELECT 1 FROM words WHERE node_id = {v}) THEN
  UPDATE words
  SET display_text = {sql_literal(word.display_text)},
      language_id = {lang},
      original_script = {sql_literal(word.original_script)},
      transliteration = {sql_literal(word.transliteration)},
      word_type = {sql_literal(word.word_type)},
      literal_meaning = {sql_literal(word.literal_meaning)},
      grammar_notes = {sql_literal(word.grammar_notes)},
      additional_notes = {sql_literal(word.additional_notes)},
      source_ids = {src},
      updated_at = NOW()
  WHERE node_id = {v};
ELSE
  INSERT INTO words
    (
      node_id,
      display_text,
      language_id,
      original_script,
      transliteration,
      word_type,
      literal_meaning,
      grammar_notes,
      additional_notes,
      source_ids,
      created_at,
      updated_at
    )
  VALUES
    (
      {v},
      {sql_literal(word.display_text)},
      {lang},
      {sql_literal(word.original_script)},
      {sql_literal(word.transliteration)},
      {sql_literal(word.word_type)},
      {sql_literal(word.literal_meaning)},
      {sql_literal(word.grammar_notes)},
      {sql_literal(word.additional_notes)},
      {src},
      NOW(),
      NOW()
    );
END IF;
""")
        else:
            self.add(f"""
IF NOT EXISTS (SELECT 1 FROM words WHERE node_id = {v}) THEN
  INSERT INTO words
    (
      node_id,
      display_text,
      language_id,
      original_script,
      transliteration,
      word_type,
      literal_meaning,
      grammar_notes,
      additional_notes,
      source_ids,
      created_at,
      updated_at
    )
  VALUES
    (
      {v},
      {sql_literal(word.display_text)},
      {lang},
      {sql_literal(word.original_script)},
      {sql_literal(word.transliteration)},
      {sql_literal(word.word_type)},
      {sql_literal(word.literal_meaning)},
      {sql_literal(word.grammar_notes)},
      {sql_literal(word.additional_notes)},
      {src},
      NOW(),
      NOW()
    );
END IF;
""")

        return v

    def ensure_name(self, name: NameNode) -> str:
        v = self.ensure_node(
            node_type="name",
            slug=name.slug,
            label=name.label,
            canonical_key=name.canonical_key,
            description_short=name.description_short,
            lookup_slugs=name.lookup_slugs,
            lookup_labels=name.lookup_labels,
            lookup_canonical_keys=name.lookup_canonical_keys,
            update_existing_node=name.update_existing_node,
        )

        lang = self.language_var(name.primary_language_slug)
        src = self.source_expr(name.source_group)

        if name.update_existing_detail:
            self.add(f"""
IF EXISTS (SELECT 1 FROM names WHERE node_id = {v}) THEN
  UPDATE names
  SET display_name = {sql_literal(name.display_name)},
      original_script = {sql_literal(name.original_script)},
      transliteration = {sql_literal(name.transliteration)},
      primary_language_id = {lang},
      gender_usage = {sql_literal(name.gender_usage)},
      short_summary = {sql_literal(name.short_summary)},
      long_summary = {sql_literal(name.long_summary)},
      literary_notes = {sql_literal(name.literary_notes)},
      cultural_notes = {sql_literal(name.cultural_notes)},
      pronunciation_notes = {sql_literal(name.pronunciation_notes)},
      certainty_notes = {sql_literal(name.certainty_notes)},
      source_ids = {src},
      updated_at = NOW()
  WHERE node_id = {v};
ELSE
  INSERT INTO names
    (
      node_id,
      display_name,
      original_script,
      transliteration,
      primary_language_id,
      gender_usage,
      short_summary,
      long_summary,
      literary_notes,
      cultural_notes,
      pronunciation_notes,
      certainty_notes,
      source_ids,
      created_at,
      updated_at
    )
  VALUES
    (
      {v},
      {sql_literal(name.display_name)},
      {sql_literal(name.original_script)},
      {sql_literal(name.transliteration)},
      {lang},
      {sql_literal(name.gender_usage)},
      {sql_literal(name.short_summary)},
      {sql_literal(name.long_summary)},
      {sql_literal(name.literary_notes)},
      {sql_literal(name.cultural_notes)},
      {sql_literal(name.pronunciation_notes)},
      {sql_literal(name.certainty_notes)},
      {src},
      NOW(),
      NOW()
    );
END IF;
""")
        else:
            self.add(f"""
IF NOT EXISTS (SELECT 1 FROM names WHERE node_id = {v}) THEN
  INSERT INTO names
    (
      node_id,
      display_name,
      original_script,
      transliteration,
      primary_language_id,
      gender_usage,
      short_summary,
      long_summary,
      literary_notes,
      cultural_notes,
      pronunciation_notes,
      certainty_notes,
      source_ids,
      created_at,
      updated_at
    )
  VALUES
    (
      {v},
      {sql_literal(name.display_name)},
      {sql_literal(name.original_script)},
      {sql_literal(name.transliteration)},
      {lang},
      {sql_literal(name.gender_usage)},
      {sql_literal(name.short_summary)},
      {sql_literal(name.long_summary)},
      {sql_literal(name.literary_notes)},
      {sql_literal(name.cultural_notes)},
      {sql_literal(name.pronunciation_notes)},
      {sql_literal(name.certainty_notes)},
      {src},
      NOW(),
      NOW()
    );
END IF;
""")

        return v

    def ensure_edge(self, edge: Edge) -> None:
        from_var = self.node_var(edge.from_slug)
        to_var = self.node_var(edge.to_slug)
        src = self.source_expr(edge.source_group)

        self.edge_specs.append(edge)

        self.add(f"""
---------------------------------------------------------------------------
-- Edge: {edge.from_slug} -> {edge.to_slug} / {edge.edge_type_code}
---------------------------------------------------------------------------

DELETE FROM edges
WHERE
  (
    from_node_id = {from_var}
    AND to_node_id = {to_var}
  )
  OR
  (
    from_node_id = {to_var}
    AND to_node_id = {from_var}
  );

INSERT INTO edges
  (
    from_node_id,
    to_node_id,
    edge_type_code,
    certainty,
    explanation,
    source_ids,
    created_at,
    updated_at
  )
VALUES
  (
    {from_var},
    {to_var},
    {sql_literal(edge.edge_type_code)},
    {edge.certainty},
    {sql_literal(edge.explanation)},
    {src},
    NOW(),
    NOW()
  );
""")

    def validate_lineage(self, lineage: Lineage) -> None:
        known_edges = {(e.from_slug, e.to_slug) for e in self.edge_specs}
        known_edges |= {(e.to_slug, e.from_slug) for e in self.edge_specs}

        for group_index in range(len(lineage.path) - 1):
            left = lineage.path[group_index]
            right = lineage.path[group_index + 1]

            connected = any((a, b) in known_edges for a in left for b in right)

            if not connected:
                raise ValueError(
                    "Lineage has adjacent groups with no explicit edge: "
                    f"{left} -> {right}. Add an Edge; do not rely on lineage grouping."
                )

    def ensure_primary_lineage(self, lineage: Lineage) -> None:
        self.validate_lineage(lineage)

        name_var = self.node_var(lineage.name_slug)
        src = self.source_expr(lineage.source_group)
        self.lineage_specs.append(lineage)

        path_groups: list[str] = []

        for group in lineage.path:
            group_vars = [f"{self.node_var(slug)}::text" for slug in group]
            path_groups.append("jsonb_build_array(" + ", ".join(group_vars) + ")")

        path_sql = "jsonb_build_array(\n        " + ",\n        ".join(path_groups) + "\n      )"

        self.add(f"""
---------------------------------------------------------------------------
-- Primary lineage: {lineage.name_slug}
---------------------------------------------------------------------------

DELETE FROM lineages
WHERE node_id = {name_var}
  AND lineage_type = 'primary';

INSERT INTO lineages
  (
    node_id,
    lineage_type,
    title,
    summary,
    path_nodes,
    certainty,
    source_ids,
    created_at,
    updated_at
  )
VALUES
  (
    {name_var},
    'primary',
    {sql_literal(lineage.title)},
    {sql_literal(lineage.summary)},
    {path_sql},
    {lineage.certainty},
    {src},
    NOW(),
    NOW()
  );
""")

    def render_quick_checks(self) -> str:
        parts: list[str] = []

        if self.node_lookup_slugs:
            parts.append(f"""
-- Quick check: nodes created or reused by this batch
SELECT node_type, slug, display_label, canonical_key, description_short
FROM nodes
WHERE slug IN {sql_in(sorted(self.node_lookup_slugs))}
ORDER BY node_type, slug;
""".strip())

        if self.name_slugs:
            parts.append(f"""
-- Quick check: name detail rows
SELECT
  n.slug,
  nd.display_name,
  nd.gender_usage,
  nd.short_summary,
  nd.cultural_notes,
  nd.certainty_notes
FROM names nd
JOIN nodes n ON n.id = nd.node_id
WHERE n.slug IN {sql_in(sorted(self.name_slugs))}
ORDER BY n.slug;
""".strip())

        if self.word_slugs:
            parts.append(f"""
-- Quick check: word detail rows
SELECT
  n.slug,
  w.display_text,
  w.transliteration,
  w.literal_meaning,
  w.word_type
FROM words w
JOIN nodes n ON n.id = w.node_id
WHERE n.slug IN {sql_in(sorted(self.word_slugs))}
ORDER BY n.slug;
""".strip())

        if self.edge_specs:
            from_slugs = sorted({e.from_slug for e in self.edge_specs})
            to_slugs = sorted({e.to_slug for e in self.edge_specs})

            parts.append(f"""
-- Quick check: edges added by this batch
SELECT
  from_node.slug AS from_slug,
  from_node.display_label AS from_label,
  e.edge_type_code,
  to_node.slug AS to_slug,
  to_node.display_label AS to_label,
  e.certainty,
  e.explanation
FROM edges e
JOIN nodes from_node ON from_node.id = e.from_node_id
JOIN nodes to_node ON to_node.id = e.to_node_id
WHERE from_node.slug IN {sql_in(from_slugs)}
  AND to_node.slug IN {sql_in(to_slugs)}
ORDER BY from_node.slug, e.edge_type_code, to_node.slug;
""".strip())

        if self.lineage_specs:
            lineage_slugs = sorted({l.name_slug for l in self.lineage_specs})

            parts.append(f"""
-- Quick check: primary lineages
SELECT
  n.slug,
  l.title,
  l.summary,
  l.path_nodes,
  l.certainty
FROM lineages l
JOIN nodes n ON n.id = l.node_id
WHERE n.slug IN {sql_in(lineage_slugs)}
  AND l.lineage_type = 'primary'
ORDER BY n.slug;
""".strip())

        return "\n\n".join(parts)

    def render(self) -> str:
        if not self.statements:
            raise ValueError("No SQL statements generated")

        declarations = "\n  ".join(
            f"{name} {dtype};" for name, dtype in sorted(self.declarations.items())
        )

        body = "\n\n  ".join(self.statements)

        return f"""BEGIN;

DO $$
DECLARE
  {declarations}

BEGIN

  {body}

END $$;

COMMIT;

{self.render_quick_checks()}
"""
