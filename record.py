import re
from datetime import date, time
from exceptions import InvalidRecord, UndefinedRecordType, Ignore

class FIASRecord:
    """
    A class for parsing, validating, and managing records from the FIAS PMS (Property Management System).

    This class handles the following operations:
    1. Parsing raw message strings into structured records.
    2. Extracting and setting record types and attributes.
    3. Validating records based on their type and required attributes.
    4. Raising appropriate exceptions for invalid or undefined record types.

    Attributes:
        message (str): The raw message string representing the record.
        type (str): The type of the record (e.g., 'GI', 'GC', 'GM', 'GO').
        Various dynamic attributes: Set based on the parsed record data.

    Raises:
        InvalidRecord: If the record format is invalid.
        UndefinedRecordType: If the record type is not recognized.
        Ignore: For certain record types that should be ignored.

    Usage:
        record = Record("GI|G#123|RN101|GNJohn Doe")
        if record.is_valid(raise_exception=True):
            # Process the record
    """
    
    ignore_attrs = [
        # Database Synchronization
        'DS', # Database Resync start
        'DE', # Database Resync end
        'LS', # Link Start
        'LE', # Link End
        'LA', # Link Alive
    ]
    to_pms = (
        'LD', # Link Description
        'LR', # Link Record
        # Database Synchronization
        'DR', # Database Resync request
        # Night Audit
        'NS', # Night Audit Start
        'NE', # Night Audit End
    )
    required_attrs = {
        'GI': ['GID', 'RN', 'GN'],
        'GC': ['GID', 'RN',],
        'GM': ['GID', 'RN', 'RO'],
        'GO': ['RN'],
    }

    def __init__(self, message: str):
        self.message = str(message)
        parts = self.message.split('|')
        if len(parts) > 1:
            self._parse_attributes()
            self.type = parts[0] if len(parts[0]) == 2 else None
            if self.type == 'GC' and hasattr(self, 'RO'):
                self.type = 'GM'  # Guest Move
        else:
            raise InvalidRecord(self.message)

    def _parse_attributes(self):
        """Parse all attributes from the data and set them as properties."""
        pattern = r'\|([A-Z#]{2})([^|]*)'
        matches = re.findall(pattern, self.message)
        
        for prefix, value in matches:
            attr_name = prefix if prefix != 'G#' else 'GID'
            setattr(self, attr_name, value)

        # Convert GID to int if it exists
        if hasattr(self, 'GID'):
            self.GID = int(self.GID)
        
        # Convert Date field to date
        for f in ('DA', 'GA', 'GD'):
            if hasattr(self, f):
                setattr(self, f, date.strftime(getattr(self, f)), '%y%m%d')

        # Convert Time field to time
        for f in ('TI','DU'): 
            if hasattr(self, f):
                setattr(self, f, time.strftime(getattr(self, f)), '%H%M%S')
    

    def is_valid(self, raise_exception: bool = False) -> bool:
        """
        Check if the message has valid format or required fields
        
        Args:
            raise_exception (bool, optional): Raise an exception if the record is invalid. Defaults to False.
        
        Returns:
            bool: True if the record is valid, False otherwise.
        """

        if self.type in self.ignore_attrs:
            if raise_exception:
                raise Ignore(self.message)
            return False

        
        if self.type not in self.required_attrs:
            if raise_exception:
                raise UndefinedRecordType(self.type)
            return False
        
        missing = [_ for _ in self.required_attrs[self.type] if not hasattr(self, _)]
        if missing:
            if raise_exception:
                raise InvalidRecord(f"{self.type} is missing attributes: {', '.join(missing)}")
            return False

        return True

    def __str__(self):
        return f"Record(type={self.type}, message={self.message})"

    def __repr__(self):
        return f"Record(type={self.type}, message={self.message})"
