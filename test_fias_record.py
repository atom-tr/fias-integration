import pytest
from fias.record import FIASRecord
from fias.exceptions import InvalidRecord, UndefinedRecordType, Ignore

def test_valid_gi_record():
    data = "GI|G#123|RN101|GNJohn Doe|DA241109|TI185700"
    record = FIASRecord(data)
    assert record.is_valid()
    assert record.type == "GI"
    assert record.GID == 123
    assert record.RN == "101"
    assert record.GN == "John Doe"
    assert str(record) == data
    assert "Record(type=GI" in repr(record)

def test_valid_gm_record():
    record = FIASRecord("GC|G#123|RN101|GNJohn Doe|RO102|")
    assert record.type == "GM"

def test_invalid_record():
    with pytest.raises(InvalidRecord):
        FIASRecord("InvalidRecord")

def test_undefined_record_type():
    record = FIASRecord("XX|G#123|RN101")
    assert not record.is_valid()
    with pytest.raises(UndefinedRecordType):
        record.is_valid(raise_exception=True)

def test_ignore_record():
    record = FIASRecord("DS|SomeData")
    assert not record.is_valid()
    with pytest.raises(Ignore):
        record.is_valid(raise_exception=True)

def test_missing_attributes():
    record = FIASRecord("GI|G#123|RN101")
    assert not record.is_valid()
    with pytest.raises(InvalidRecord):
        record.is_valid(raise_exception=True)