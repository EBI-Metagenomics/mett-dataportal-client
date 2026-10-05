from __future__ import annotations

from mett_client.request_utils import coerce_tsv_value, parse_tsv_response


def test_coerce_bool_and_json() -> None:
    assert coerce_tsv_value("False") is False
    assert coerce_tsv_value("True") is True
    assert coerce_tsv_value("") is None
    assert coerce_tsv_value('{"pipeline": "x"}') == {"pipeline": "x"}
    assert coerce_tsv_value('[{"ref_name": "c1"}]') == [{"ref_name": "c1"}]
    assert coerce_tsv_value("plain") == "plain"


def test_parse_genome_like_tsv() -> None:
    tsv = (
        "isolate_name\ttype_strain\tannotation\tcontigs\n"
        'PV_H4\tFalse\t{"pipeline": "mett"}\t[{"ref_name": "c1", "length": 10}]\n'
    )
    rows = parse_tsv_response(tsv)
    assert len(rows) == 1
    assert rows[0]["isolate_name"] == "PV_H4"
    assert rows[0]["type_strain"] is False
    assert rows[0]["annotation"] == {"pipeline": "mett"}
    assert rows[0]["contigs"] == [{"ref_name": "c1", "length": 10}]


def test_parse_tsv_without_nested_contigs() -> None:
    """API TSV may omit nested contigs; rows should still parse as dicts."""
    tsv = (
        "species_scientific_name\tisolate_name\ttype_strain\tannotation\n"
        'Phocaeicola vulgatus\tPV_H4\tFalse\t{"pipeline": "mett"}\n'
    )
    rows = parse_tsv_response(tsv)
    assert rows[0]["type_strain"] is False
    assert "contigs" not in rows[0]
