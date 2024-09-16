import pytest
from record import FIASRecord
from exceptions import InvalidRecord, UndefinedRecordType, Ignore

def test_valid_gi_record():
    record = FIASRecord("GI|G#123|RN101|GNJohn Doe")
    assert record.is_valid()
    assert record.type == "GI"
    assert record.GID == 123
    assert record.RN == "101"
    assert record.GN == "John Doe"

def test_invalid_record():
    with pytest.raises(InvalidRecord):
        FIASRecord("InvalidRecord")

def test_undefined_record_type():
    with pytest.raises(UndefinedRecordType):
        record = FIASRecord("XX|G#123|RN101")
        record.is_valid(raise_exception=True)

def test_ignore_record():
    with pytest.raises(Ignore):
        record = FIASRecord("DS|SomeData")
        record.is_valid(raise_exception=True)

def test_missing_attributes():
    record = FIASRecord("GI|G#123|RN101")
    assert not record.is_valid()
    with pytest.raises(InvalidRecord):
        record.is_valid(raise_exception=True)