from sql_generator import *
from sql_helpers import *
from pathlib import Path


def build_fish_names_02_global_corrected_sql() -> str:
    b = NominaSQLBuilder()
    b.include_edge_types()

    ensure_languages(b, [
        Language(
            slug="ancient-greek",
            name="Ancient Greek",
            language_family="Hellenic / Indo-European",
            period_label="Ancient Greek",
            region_note="Historically used in ancient Greece and the wider Hellenic world.",
            additional_notes="Used here for Greek dolphin vocabulary behind Delphina and Delphine.",
        ),
        Language(
            slug="latin",
            name="Latin",
            language_family="Italic / Indo-European",
            period_label="Classical and Late Latin",
            region_note="Historically used in ancient Rome and later across Europe.",
            additional_notes="Used here for Latinised dolphin forms such as delphinus and Delphina.",
        ),
        Language(
            slug="french",
            name="French",
            language_family="Romance / Indo-European",
            period_label="Modern French",
            region_note="Used primarily in France and French-speaking communities.",
            additional_notes="Used here for French name forms such as Delphine.",
        ),
        Language(
            slug="irish",
            name="Irish",
            alternative_names_json='["Irish Gaelic", "Gaeilge"]',
            language_family="Celtic / Indo-European",
            period_label="Modern Irish with older Irish roots",
            region_note="Used primarily in Ireland and Irish diaspora communities.",
            additional_notes="Used here for Irish fish names such as Bradán.",
        ),
        Language(
            slug="english",
            name="English",
            language_family="Germanic / Indo-European",
            period_label="Modern English",
            region_note="Used in Britain, Ireland, North America, Australia, New Zealand, and many other regions.",
            additional_notes="Used here for English nickname routes such as Kip from kipper.",
        ),
        Language(
            slug="tupi",
            name="Tupi",
            language_family="Tupian",
            period_label="Indigenous Tupi language context",
            region_note="Historically associated with Indigenous peoples of Brazil and neighbouring regions.",
            additional_notes="Used here cautiously for Tupi mythological name routes such as Jurupari.",
        ),
        Language(
            slug="yoruba",
            name="Yoruba",
            language_family="Yoruboid / Niger-Congo",
            period_label="Traditional and modern Yoruba contexts",
            region_note="Used primarily in southwestern Nigeria, Benin, Togo, and Yoruba diaspora traditions.",
            additional_notes="Used here for Yoruba deity-name routes such as Yemoja, built from mother, child, and fish elements.",
        ),
        Language(
            slug="portuguese",
            name="Portuguese",
            language_family="Romance / Indo-European",
            period_label="Modern Portuguese",
            region_note="Used primarily in Portugal, Brazil, and Portuguese-speaking communities.",
            additional_notes="Used here for Afro-Brazilian Portuguese forms such as Iemanjá.",
        ),
        Language(
            slug="spanish",
            name="Spanish",
            language_family="Romance / Indo-European",
            period_label="Modern Spanish",
            region_note="Used primarily in Spain, Latin America, and Spanish-speaking communities.",
            additional_notes="Used here for diaspora forms such as Yemaya.",
        ),
    ])

    b.ensure_sources(
        group_name="fish_names_02_global_corrected",
        sources=[
            Source(
                title="Behind the Name - Names Tagged Fish",
                author="Behind the Name",
                source_type="name list / name dictionary",
                url="https://www.behindthename.com/names/tag/fish",
                citation_text="Behind the Name, names tagged “fish”.",
                notes="Used for Kip, Jurupari, and related fish-tagged names.",
            ),
            Source(
                title="Behind the Name - Names Meaning Salmon",
                author="Behind the Name",
                source_type="name list / name dictionary",
                url="https://www.behindthename.com/names/meaning/salmon",
                citation_text="Behind the Name, names with meaning “salmon”.",
                notes="Used for Bradán meaning salmon and Kip from kipper, male salmon.",
            ),
            Source(
                title="Britannica - Yemonja",
                author="Encyclopaedia Britannica",
                source_type="encyclopaedia",
                url="https://www.britannica.com/topic/Yemonja",
                citation_text="Encyclopaedia Britannica, “Yemonja”.",
                notes="Used for Yemonja/Yemoja as a Yoruba deity name from mother, child/children, and fish elements.",
            ),
            Source(
                title="Wikipedia - Yemoja",
                author="Wikipedia contributors",
                source_type="encyclopaedia",
                url="https://en.wikipedia.org/wiki/Yem%E1%BB%8Dja",
                citation_text="Wikipedia, “Yemọja”.",
                notes="Used cautiously for variants such as Yemọja, Yemaya, and Iemanjá, and for the Yoruba mother + children + fish explanation.",
            ),
            Source(
                title="Behind the Name - Delphine",
                author="Behind the Name",
                source_type="name dictionary",
                url="https://www.behindthename.com/name/delphine",
                citation_text="Behind the Name, “Delphine”.",
                notes="Used for Delphine as a French form in the Delphina / Delphinus dolphin-related route.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # Existing concept nodes
    # -------------------------------------------------------------------------

    require_existing_node(
        b,
        node_type="concept",
        slug="mother",
        label="mother",
        canonical_key="mother",
        lookup_slugs=["motherhood"],
        lookup_labels=["mother", "motherhood"],
        lookup_canonical_keys=["mother", "motherhood"],
    )

    require_existing_node(
        b,
        node_type="concept",
        slug="child",
        label="child",
        canonical_key="child",
        lookup_slugs=["child-offspring"],
        lookup_labels=["child", "offspring", "child / offspring"],
        lookup_canonical_keys=["child", "offspring", "child offspring"],
    )

    require_existing_node(
        b,
        node_type="concept",
        slug="deity-god",
        label="deity / god",
        canonical_key="deity god",
        lookup_slugs=["deity", "god", "goddess"],
        lookup_labels=["deity", "god", "goddess", "deity / god"],
        lookup_canonical_keys=["deity", "god", "goddess", "deity god"],
    )

    # -------------------------------------------------------------------------
    # Added / reused concepts
    # No separate dolphin, salmon, or fish-trap concept nodes.
    # Those words connect directly to fish.
    # -------------------------------------------------------------------------

    ensure_concepts(b, [
        ConceptNode(
            slug="fish",
            label="fish",
            canonical_key="fish",
            description_short="The idea of a fish or fish-like aquatic creature.",
            description="The idea of a fish or fish-like aquatic creature. Used for names where the meaning comes directly from fish vocabulary, fish imagery, fish types, or fish-related mythological language.",
            source_group="fish_names_02_global_corrected",
            lookup_slugs=["fish"],
            lookup_labels=["fish"],
            lookup_canonical_keys=["fish"],
        ),
        ConceptNode(
            slug="mouth",
            label="mouth",
            canonical_key="mouth",
            description_short="The idea of a mouth or opening.",
            description="The idea of a mouth or opening. Used for Tupi îuru in the Jurupari route.",
            source_group="fish_names_02_global_corrected",
            lookup_slugs=["mouth"],
            lookup_labels=["mouth"],
            lookup_canonical_keys=["mouth"],
        ),
    ])

    # -------------------------------------------------------------------------
    # Delphina / Delphine
    # fish -> Greek delphis, dolphin -> Latin delphinus -> Delphina -> Delphine
    # -------------------------------------------------------------------------

    greek_delphis = WordNode(
        slug="greek-delphis-dolphin",
        label="delphis / δελφίς",
        canonical_key="delphis dolphin",
        description_short="Ancient Greek word meaning dolphin.",
        language_slug="ancient-greek",
        display_text="δελφίς",
        original_script="δελφίς",
        transliteration="delphis",
        word_type="noun / name element",
        literal_meaning="dolphin",
        grammar_notes="Ancient Greek noun meaning dolphin.",
        additional_notes="Delphis supplies the dolphin root behind Latin delphinus and later Delphina / Delphine forms. In this model, dolphin-type words are connected to the wider fish concept rather than given a separate concept node.",
        source_group="fish_names_02_global_corrected",
        lookup_labels=["delphis", "δελφίς"],
        lookup_canonical_keys=["delphis", "delphis dolphin"],
    )

    latin_delphinus = WordNode(
        slug="latin-delphinus",
        label="delphinus",
        canonical_key="delphinus",
        description_short="Latin word/name form meaning dolphin.",
        language_slug="latin",
        display_text="delphinus",
        original_script="delphinus",
        transliteration="delphinus",
        word_type="noun / name element",
        literal_meaning="dolphin",
        grammar_notes="Latin form from Greek delphis, dolphin.",
        additional_notes="Delphinus is the Latin dolphin route behind Delphina and Delphine. It is also familiar through classical and astronomical naming.",
        source_group="fish_names_02_global_corrected",
        lookup_labels=["delphinus", "Delphinus"],
        lookup_canonical_keys=["delphinus"],
    )

    b.ensure_word(greek_delphis)
    b.ensure_word(latin_delphinus)

    b.ensure_edge(Edge(
        from_slug="fish",
        to_slug="greek-delphis-dolphin",
        edge_type_code="meaning_of",
        certainty=0.82,
        explanation="Ancient Greek delphis means dolphin; this fish-related aquatic creature term is grouped under the broader fish concept in Nomina.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="greek-delphis-dolphin",
        to_slug="latin-delphinus",
        edge_type_code="evolves_to",
        certainty=0.88,
        explanation="Latin delphinus is a Latin dolphin form from Greek delphis.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_name(NameNode(
        slug="delphina",
        label="Delphina",
        canonical_key="delphina",
        description_short="Latin feminine name form connected with delphinus, dolphin.",
        display_name="Delphina",
        original_script="Delphina",
        transliteration="Delphina",
        primary_language_slug="latin",
        gender_usage="feminine given name",
        short_summary="Delphina is a feminine name form connected with Latin delphinus, dolphin.",
        long_summary="Delphina is a feminine form in the Latin Delphinus route, connected with the word for dolphin. In this graph, the dolphin word is placed under the wider fish-related concept rather than a separate dolphin concept.",
        literary_notes=None,
        cultural_notes="Delphina is rarer than Delphine, but it preserves the Latin form more visibly.",
        pronunciation_notes="Often pronounced del-FEE-na or del-FY-na in English.",
        certainty_notes="Good certainty for Delphina as a feminine form connected with Latin delphinus and the dolphin route.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="latin-delphinus",
        to_slug="delphina",
        edge_type_code="element_of",
        certainty=0.86,
        explanation="Latin delphinus supplies the dolphin-related route behind Delphina.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_primary_lineage(Lineage(
        name_slug="delphina",
        title="Etymology of Delphina",
        summary="Delphina is connected with Latin delphinus, dolphin, from Greek delphis.",
        path=[
            ["fish"],
            ["greek-delphis-dolphin"],
            ["latin-delphinus"],
            ["delphina"],
        ],
        certainty=0.86,
        source_group="fish_names_02_global_corrected",
    ))

    add_name_variant(
        b,
        variant=NameNode(
            slug="delphine",
            label="Delphine",
            canonical_key="delphine",
            description_short="French form related to Delphina and the dolphin name route.",
            display_name="Delphine",
            original_script="Delphine",
            transliteration="Delphine",
            primary_language_slug="french",
            gender_usage="feminine given name",
            short_summary="Delphine is a French feminine name related to Delphina and the dolphin name route.",
            long_summary="Delphine is a French form related to Delphina. It belongs near the Greek and Latin dolphin route through delphis and delphinus, while also carrying a classical European feel.",
            literary_notes=None,
            cultural_notes="Delphine is used in French and international contexts and has an elegant classical feel.",
            pronunciation_notes="French pronunciation is roughly del-FEEN; English speakers may say DEL-feen or del-FEEN.",
            certainty_notes="Good certainty for Delphine as a French form related to Delphina. The exact balance between Delphi and dolphin associations should be handled with nuance.",
            source_group="fish_names_02_global_corrected",
        ),
        base_slug="delphina",
        variant_explanation="Delphine is a French form related to Delphina in the dolphin/classical route.",
        variant_certainty=0.86,
        lineage_path=[
            ["fish"],
            ["greek-delphis-dolphin"],
            ["latin-delphinus"],
            ["delphina"],
            ["delphine"],
        ],
        lineage_title="Etymology of Delphine",
        lineage_summary="Delphine is a French form related to Delphina, ultimately connected with the Greek and Latin dolphin route.",
        lineage_certainty=0.84,
        source_group="fish_names_02_global_corrected",
    )

    # -------------------------------------------------------------------------
    # Bradán
    # fish -> Irish bradán, salmon -> Bradán
    # -------------------------------------------------------------------------

    irish_bradan = WordNode(
        slug="irish-bradan",
        label="bradán",
        canonical_key="bradan salmon",
        description_short="Irish word meaning salmon.",
        language_slug="irish",
        display_text="bradán",
        original_script="bradán",
        transliteration="bradan",
        word_type="noun / name element",
        literal_meaning="salmon",
        grammar_notes="Irish noun meaning salmon.",
        additional_notes="Bradán means salmon in Irish. Salmon has a strong cultural resonance in Irish tradition, especially through wisdom-salmon imagery. In this model, salmon words connect to the wider fish concept.",
        source_group="fish_names_02_global_corrected",
        lookup_labels=["bradán", "bradan", "Bradán"],
        lookup_canonical_keys=["bradan", "bradan salmon"],
    )

    add_direct_name(
        b,
        word=irish_bradan,
        name=NameNode(
            slug="bradan",
            label="Bradán",
            canonical_key="bradan",
            description_short="Irish name from bradán, meaning salmon.",
            display_name="Bradán",
            original_script="Bradán",
            transliteration="Bradan",
            primary_language_slug="irish",
            gender_usage="masculine given name; historical / medieval name",
            short_summary="Bradán is an Irish name from bradán, meaning salmon.",
            long_summary="Bradán comes directly from Irish bradán, meaning salmon. The name belongs to the fish family through a specific culturally important fish rather than a generic fish word.",
            literary_notes="The salmon is important in Irish myth and story, especially in wisdom-salmon traditions such as the Salmon of Knowledge.",
            cultural_notes="Bradán has a distinctly Irish feel and is more specialised than many everyday nature names.",
            pronunciation_notes="Often approximated as brah-DAWN.",
            certainty_notes="Good certainty for Irish bradán meaning salmon.",
            source_group="fish_names_02_global_corrected",
        ),
        concept_edges=[
            MeaningEdge("fish", "Irish bradán means salmon, a fish.", 0.90),
        ],
        word_to_name_explanation="Irish bradán forms the name Bradán.",
        word_to_name_certainty=0.90,
        lineage_title="Etymology of Bradán",
        lineage_summary="Bradán comes from Irish bradán, meaning salmon.",
        lineage_certainty=0.90,
        source_group="fish_names_02_global_corrected",
    )

    # -------------------------------------------------------------------------
    # Kip
    # fish -> English kipper, male salmon -> Kip
    # -------------------------------------------------------------------------

    english_kipper = WordNode(
        slug="english-kipper",
        label="kipper",
        canonical_key="kipper salmon",
        description_short="English word meaning male salmon in this nickname route.",
        language_slug="english",
        display_text="kipper",
        original_script="kipper",
        transliteration="kipper",
        word_type="noun / nickname source",
        literal_meaning="male salmon",
        grammar_notes="English word used in the name route for Kip as a nickname source.",
        additional_notes="Kip is explained by Behind the Name as probably from English kipper, male salmon. This should be treated cautiously as a nickname route rather than a formal ancient given-name etymology. The kipper word connects to the broader fish concept.",
        source_group="fish_names_02_global_corrected",
        lookup_labels=["kipper"],
        lookup_canonical_keys=["kipper", "kipper salmon"],
    )

    add_direct_name(
        b,
        word=english_kipper,
        name=NameNode(
            slug="kip",
            label="Kip",
            canonical_key="kip",
            description_short="English nickname-name probably from kipper, male salmon.",
            display_name="Kip",
            original_script="Kip",
            transliteration="Kip",
            primary_language_slug="english",
            gender_usage="masculine given name / nickname",
            short_summary="Kip is an English nickname-name probably from kipper, male salmon.",
            long_summary="Kip is explained as a nickname, probably from the English word kipper, meaning male salmon. The route is therefore fish-related, but it is less direct and less formal than a transparent vocabulary-name such as Meena or Bada.",
            literary_notes=None,
            cultural_notes="Kip has a short, informal English nickname feel. Its fish connection should be presented with caution because the source itself marks the derivation as probable.",
            pronunciation_notes="Usually pronounced KIP.",
            certainty_notes="Moderate certainty. Kip is probably from kipper, male salmon, but the route is nickname-based and should not be overclaimed.",
            source_group="fish_names_02_global_corrected",
        ),
        concept_edges=[
            MeaningEdge("fish", "English kipper can mean male salmon, a fish, in this nickname route.", 0.72),
        ],
        word_to_name_explanation="English kipper is the probable nickname source of Kip.",
        word_to_name_certainty=0.74,
        lineage_title="Etymology of Kip",
        lineage_summary="Kip is probably from English kipper, male salmon.",
        lineage_certainty=0.74,
        source_group="fish_names_02_global_corrected",
    )

    # -------------------------------------------------------------------------
    # Jurupari
    # mouth + fish -> Tupi îuru + pari, possibly fish trap -> Jurupari
    # -------------------------------------------------------------------------

    tupi_iuru = WordNode(
        slug="tupi-iuru",
        label="îuru",
        canonical_key="iuru mouth",
        description_short="Tupi element meaning mouth.",
        language_slug="tupi",
        display_text="îuru",
        original_script="îuru",
        transliteration="iuru",
        word_type="noun / name element",
        literal_meaning="mouth",
        grammar_notes="Tupi element meaning mouth.",
        additional_notes="Îuru supplies the mouth element in the usual explanation of Jurupari.",
        source_group="fish_names_02_global_corrected",
        lookup_labels=["îuru", "iuru", "juru"],
        lookup_canonical_keys=["iuru", "iuru mouth"],
    )

    tupi_pari = WordNode(
        slug="tupi-pari-fish-trap",
        label="pari",
        canonical_key="pari fish trap",
        description_short="Tupi element possibly meaning fish trap.",
        language_slug="tupi",
        display_text="pari",
        original_script="pari",
        transliteration="pari",
        word_type="noun / name element",
        literal_meaning="possibly fish trap",
        grammar_notes="Tupi element; in the Jurupari route it is given cautiously as possibly fish trap.",
        additional_notes="The pari element in Jurupari is uncertain. In this model, it connects to the wider fish concept because it is fish-related, but no separate fish-trap concept is created.",
        source_group="fish_names_02_global_corrected",
        lookup_labels=["pari"],
        lookup_canonical_keys=["pari", "pari fish trap"],
    )

    tupi_jurupari = WordNode(
        slug="tupi-jurupari",
        label="Jurupari",
        canonical_key="jurupari",
        description_short="Tupi mythological name form from mouth and possibly fish-trap elements.",
        language_slug="tupi",
        display_text="Jurupari",
        original_script="Jurupari",
        transliteration="Jurupari",
        word_type="mythological name form",
        literal_meaning="mouth + possibly fish trap",
        grammar_notes="Tupi mythological name form, commonly explained from îuru, mouth, and possibly pari, fish trap.",
        additional_notes="Jurupari is a mythological name from Tupi traditions. The fish-related part is uncertain because the pari element is given as possible rather than definite.",
        source_group="fish_names_02_global_corrected",
        lookup_labels=["Jurupari"],
        lookup_canonical_keys=["jurupari"],
    )

    b.ensure_word(tupi_iuru)
    b.ensure_word(tupi_pari)
    b.ensure_word(tupi_jurupari)

    b.ensure_edge(Edge(
        from_slug="mouth",
        to_slug="tupi-iuru",
        edge_type_code="meaning_of",
        certainty=0.88,
        explanation="Tupi îuru means mouth.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="fish",
        to_slug="tupi-pari-fish-trap",
        edge_type_code="meaning_of",
        certainty=0.58,
        explanation="Tupi pari is given cautiously as possibly meaning fish trap in the Jurupari route; it is connected to the wider fish concept rather than a separate fish-trap concept.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="tupi-iuru",
        to_slug="tupi-jurupari",
        edge_type_code="element_of",
        certainty=0.82,
        explanation="Tupi îuru supplies the mouth element in Jurupari.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="tupi-pari-fish-trap",
        to_slug="tupi-jurupari",
        edge_type_code="element_of",
        certainty=0.58,
        explanation="Tupi pari may supply a fish-trap element in Jurupari, though this analysis is uncertain.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_name(NameNode(
        slug="jurupari",
        label="Jurupari",
        canonical_key="jurupari",
        description_short="Tupi mythological name from mouth and possibly fish-trap elements.",
        display_name="Jurupari",
        original_script="Jurupari",
        transliteration="Jurupari",
        primary_language_slug="tupi",
        gender_usage="masculine mythological name",
        short_summary="Jurupari is a Tupi mythological name from mouth and possibly fish-trap elements.",
        long_summary="Jurupari is a name from Tupi mythology. It is commonly explained from Tupi îuru, mouth, and possibly pari, fish trap. The fish-related element is therefore present but cautious, because the pari analysis is not fully certain.",
        literary_notes="In Tupi legend, Jurupari is a mythological hero associated with laws and customs. Later missionary interpretation altered the way the figure was understood.",
        cultural_notes="Jurupari should be handled respectfully as an Indigenous mythological name rather than simply as a baby-name word.",
        pronunciation_notes="Often approximated as joo-roo-PAH-ree.",
        certainty_notes="Good certainty for the mythological name and the îuru mouth element; lower certainty for pari as fish trap.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="tupi-jurupari",
        to_slug="jurupari",
        edge_type_code="element_of",
        certainty=0.82,
        explanation="The Tupi mythological name form Jurupari gives the name Jurupari.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_primary_lineage(Lineage(
        name_slug="jurupari",
        title="Etymology of Jurupari",
        summary="Jurupari is a Tupi mythological name from îuru, mouth, and possibly pari, fish trap.",
        path=[
            ["mouth", "fish"],
            ["tupi-iuru", "tupi-pari-fish-trap"],
            ["tupi-jurupari"],
            ["jurupari"],
        ],
        certainty=0.68,
        source_group="fish_names_02_global_corrected",
    ))

    # -------------------------------------------------------------------------
    # Yemoja / Yemaya / Iemanjá
    # mother + child + fish + deity/god -> Yoruba name form -> Yemoja
    # -------------------------------------------------------------------------

    yoruba_iya = WordNode(
        slug="yoruba-iya-mother",
        label="ìyá / yeye",
        canonical_key="iya mother",
        description_short="Yoruba element meaning mother.",
        language_slug="yoruba",
        display_text="ìyá / yeye",
        original_script="ìyá / yeye",
        transliteration="iya / yeye",
        word_type="noun / name element",
        literal_meaning="mother",
        grammar_notes="Yoruba mother element used in the Yemoja / Yemonja explanation.",
        additional_notes="This is the maternal element in the explanation of Yemoja / Yemonja.",
        source_group="fish_names_02_global_corrected",
        lookup_labels=["ìyá", "iya", "yeye"],
        lookup_canonical_keys=["iya", "yeye", "iya mother"],
    )

    yoruba_omo = WordNode(
        slug="yoruba-omo-child",
        label="ọmọ",
        canonical_key="omo child",
        description_short="Yoruba word meaning child.",
        language_slug="yoruba",
        display_text="ọmọ",
        original_script="ọmọ",
        transliteration="omo",
        word_type="noun / name element",
        literal_meaning="child",
        grammar_notes="Yoruba noun meaning child or offspring.",
        additional_notes="Ọmọ supplies the child/children element in the Yemoja / Yemonja explanation.",
        source_group="fish_names_02_global_corrected",
        lookup_labels=["ọmọ", "omo"],
        lookup_canonical_keys=["omo", "omo child"],
    )

    yoruba_eja = WordNode(
        slug="yoruba-eja-fish",
        label="ẹja",
        canonical_key="eja fish",
        description_short="Yoruba word meaning fish.",
        language_slug="yoruba",
        display_text="ẹja",
        original_script="ẹja",
        transliteration="eja",
        word_type="noun / name element",
        literal_meaning="fish",
        grammar_notes="Yoruba noun meaning fish.",
        additional_notes="Ẹja supplies the fish element in the Yemoja / Yemonja explanation.",
        source_group="fish_names_02_global_corrected",
        lookup_labels=["ẹja", "eja"],
        lookup_canonical_keys=["eja", "eja fish"],
    )

    yoruba_yemoja_form = WordNode(
        slug="yoruba-yemoja-form",
        label="Yemọja / Yemonja",
        canonical_key="yemoja",
        description_short="Yoruba deity-name form meaning mother whose children are fish.",
        language_slug="yoruba",
        display_text="Yemọja",
        original_script="Yemọja",
        transliteration="Yemoja / Yemonja",
        word_type="deity name form",
        literal_meaning="mother whose children are fish",
        grammar_notes="Name form commonly explained from mother + child/children + fish elements.",
        additional_notes="Yemoja is a Yoruba orisha/deity name. The fish elements express abundant motherhood and water-associated divinity, not a simple animal name.",
        source_group="fish_names_02_global_corrected",
        lookup_labels=["Yemọja", "Yemoja", "Yemonja"],
        lookup_canonical_keys=["yemoja", "yemonja"],
    )

    b.ensure_word(yoruba_iya)
    b.ensure_word(yoruba_omo)
    b.ensure_word(yoruba_eja)
    b.ensure_word(yoruba_yemoja_form)

    b.ensure_edge(Edge(
        from_slug="mother",
        to_slug="yoruba-iya-mother",
        edge_type_code="meaning_of",
        certainty=0.90,
        explanation="Yoruba ìyá / yeye supplies the mother element in the Yemoja route.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="child",
        to_slug="yoruba-omo-child",
        edge_type_code="meaning_of",
        certainty=0.90,
        explanation="Yoruba ọmọ means child or offspring.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="fish",
        to_slug="yoruba-eja-fish",
        edge_type_code="meaning_of",
        certainty=0.92,
        explanation="Yoruba ẹja means fish.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="deity-god",
        to_slug="yoruba-yemoja-form",
        edge_type_code="meaning_of",
        certainty=0.90,
        explanation="Yemoja / Yemonja is a Yoruba orisha or deity associated with waters and motherhood.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="yoruba-iya-mother",
        to_slug="yoruba-yemoja-form",
        edge_type_code="element_of",
        certainty=0.86,
        explanation="The mother element contributes to the Yemoja / Yemonja name form.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="yoruba-omo-child",
        to_slug="yoruba-yemoja-form",
        edge_type_code="element_of",
        certainty=0.86,
        explanation="The child/children element contributes to the Yemoja / Yemonja name form.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="yoruba-eja-fish",
        to_slug="yoruba-yemoja-form",
        edge_type_code="element_of",
        certainty=0.86,
        explanation="The fish element contributes to the Yemoja / Yemonja name form.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_name(NameNode(
        slug="yemoja",
        label="Yemoja",
        canonical_key="yemoja",
        description_short="Yoruba deity name meaning mother whose children are fish.",
        display_name="Yemoja",
        original_script="Yemọja",
        transliteration="Yemoja / Yemọja / Yemonja",
        primary_language_slug="yoruba",
        gender_usage="feminine deity name",
        short_summary="Yemoja is a Yoruba deity name meaning mother whose children are fish.",
        long_summary="Yemoja is a Yoruba orisha/deity name commonly explained from elements meaning mother, child or children, and fish: mother whose children are fish. The fish imagery expresses abundant motherhood, water, fertility, and divine guardianship rather than a literal personal-name animal meaning.",
        literary_notes="Yemoja is central in Yoruba religion and has important Atlantic diaspora forms and traditions.",
        cultural_notes="Yemoja should be presented respectfully as a living religious and cultural name, not just as a decorative sea name.",
        pronunciation_notes="Often approximated as yeh-MOH-jah or yeh-MOH-yah; Yoruba pronunciation includes tonal and vowel details not shown fully in plain English.",
        certainty_notes="Good certainty for the mother + child + fish explanation and for Yemoja as a Yoruba orisha/deity name.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_edge(Edge(
        from_slug="yoruba-yemoja-form",
        to_slug="yemoja",
        edge_type_code="element_of",
        certainty=0.90,
        explanation="The Yoruba deity-name form Yemọja / Yemoja gives the name Yemoja.",
        source_group="fish_names_02_global_corrected",
    ))

    b.ensure_primary_lineage(Lineage(
        name_slug="yemoja",
        title="Etymology of Yemoja",
        summary="Yemoja is a Yoruba deity name commonly explained as mother whose children are fish.",
        path=[
            ["mother", "child", "fish", "deity-god"],
            ["yoruba-iya-mother", "yoruba-omo-child", "yoruba-eja-fish"],
            ["yoruba-yemoja-form"],
            ["yemoja"],
        ],
        certainty=0.88,
        source_group="fish_names_02_global_corrected",
    ))

    add_name_variant(
        b,
        variant=NameNode(
            slug="yemaya",
            label="Yemaya",
            canonical_key="yemaya",
            description_short="Spanish/Atlantic-diaspora form related to Yoruba Yemoja.",
            display_name="Yemaya",
            original_script="Yemaya",
            transliteration="Yemaya",
            primary_language_slug="spanish",
            gender_usage="feminine deity name",
            short_summary="Yemaya is a diaspora form related to Yoruba Yemoja.",
            long_summary="Yemaya is a Spanish/Atlantic-diaspora form related to Yoruba Yemoja, whose name is commonly explained as mother whose children are fish. The form is strongly associated with Afro-Caribbean religious traditions.",
            literary_notes=None,
            cultural_notes="Yemaya belongs to living religious traditions and should be presented respectfully as a deity/orisha name, not only as an ocean-themed name.",
            pronunciation_notes="Often approximated as yeh-MY-ah or yeh-MAH-yah depending on tradition and language.",
            certainty_notes="Good certainty for Yemaya as a diaspora form of Yemoja / Yemonja.",
            source_group="fish_names_02_global_corrected",
        ),
        base_slug="yemoja",
        variant_explanation="Yemaya is a Spanish/Atlantic-diaspora form related to Yoruba Yemoja.",
        variant_certainty=0.84,
        lineage_path=[
            ["mother", "child", "fish", "deity-god"],
            ["yoruba-iya-mother", "yoruba-omo-child", "yoruba-eja-fish"],
            ["yoruba-yemoja-form"],
            ["yemoja"],
            ["yemaya"],
        ],
        lineage_title="Etymology of Yemaya",
        lineage_summary="Yemaya is a diaspora form of Yemoja, whose name is commonly explained as mother whose children are fish.",
        lineage_certainty=0.82,
        source_group="fish_names_02_global_corrected",
    )

    add_name_variant(
        b,
        variant=NameNode(
            slug="iemanja",
            label="Iemanjá",
            canonical_key="iemanja",
            description_short="Portuguese/Afro-Brazilian form related to Yoruba Yemoja.",
            display_name="Iemanjá",
            original_script="Iemanjá",
            transliteration="Iemanjá",
            primary_language_slug="portuguese",
            gender_usage="feminine deity name",
            short_summary="Iemanjá is a Portuguese/Afro-Brazilian form related to Yoruba Yemoja.",
            long_summary="Iemanjá is a Portuguese/Afro-Brazilian form related to Yoruba Yemoja, whose name is commonly explained as mother whose children are fish. In Brazil, Iemanjá is strongly associated with sea devotion and Afro-Brazilian religious traditions.",
            literary_notes=None,
            cultural_notes="Iemanjá is a living religious and cultural name in Afro-Brazilian contexts. It should be handled with respect and not treated as a casual ocean-name decoration.",
            pronunciation_notes="Portuguese pronunciation varies by region; often approximated as ee-eh-man-ZHAH.",
            certainty_notes="Good certainty for Iemanjá as a Portuguese/Afro-Brazilian form related to Yemoja.",
            source_group="fish_names_02_global_corrected",
        ),
        base_slug="yemoja",
        variant_explanation="Iemanjá is a Portuguese/Afro-Brazilian form related to Yoruba Yemoja.",
        variant_certainty=0.84,
        lineage_path=[
            ["mother", "child", "fish", "deity-god"],
            ["yoruba-iya-mother", "yoruba-omo-child", "yoruba-eja-fish"],
            ["yoruba-yemoja-form"],
            ["yemoja"],
            ["iemanja"],
        ],
        lineage_title="Etymology of Iemanjá",
        lineage_summary="Iemanjá is an Afro-Brazilian Portuguese form of Yemoja, whose name is commonly explained as mother whose children are fish.",
        lineage_certainty=0.82,
        source_group="fish_names_02_global_corrected",
    )

    return b.render()


if __name__ == "__main__":
    sql = build_fish_names_02_global_corrected_sql()
    output = Path("nomina_batch_fish_names_02_global_corrected.sql")
    output.write_text(sql, encoding="utf-8")
    print(f"Wrote {output}")
