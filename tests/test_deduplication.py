"""
Tests for LegalMitra Deduplication Engine.
"""

from legalmitra.schemas.statute import StatuteSection
from legalmitra.validation.deduplication import DeduplicationEngine


def test_deduplication_engine_file_checksum():
    engine = DeduplicationEngine()
    chk = "a" * 64
    assert not engine.is_file_duplicate(chk)

    engine.register_file(chk)
    assert engine.is_file_duplicate(chk)
    assert engine.is_file_duplicate(chk.upper())


def test_deduplication_engine_text_fingerprint():
    engine = DeduplicationEngine()
    text_a = "Section 61.  Admissibility of   electronic records."
    text_b = "section 61. admissibility of electronic records. "

    dup_id = engine.check_and_register_text("SEC-001", text_a)
    assert dup_id is None

    # Near-duplicate with different whitespace / casing
    dup_id_2 = engine.check_and_register_text("SEC-002", text_b)
    assert dup_id_2 == "SEC-001"


def test_deduplication_items_filtering():
    engine = DeduplicationEngine()

    s1 = StatuteSection(
        section_id="SEC-01",
        source_id="SRC-1",
        act_title="Act",
        section_number="1",
        section_title="Title",
        full_verbatim_text="Verbatim exact provision text.",
    )
    s2 = StatuteSection(
        section_id="SEC-02",
        source_id="SRC-2",
        act_title="Act",
        section_number="1",
        section_title="Title",
        full_verbatim_text="  Verbatim exact provision text. \n",
    )
    s3 = StatuteSection(
        section_id="SEC-03",
        source_id="SRC-1",
        act_title="Act",
        section_number="2",
        section_title="Title 2",
        full_verbatim_text="A completely distinct provision text.",
    )

    unique = engine.deduplicate_items([s1, s2, s3])
    assert len(unique) == 2
    assert unique[0].section_id == "SEC-01"
    assert unique[1].section_id == "SEC-03"

