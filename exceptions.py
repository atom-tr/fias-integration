class InvalidRecord(Exception):
    """Exception raised for invalid record format"""
    def __init__(self, record, message="Invalid record format"):
        self.record = record
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.record}"

class UndefinedRecordType(Exception):
    """Exception raised for undefined record type"""
    def __init__(self, record, message="Undefined record type"):
        self.record = record
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.record}"
    
class Ignore(Exception):
    """Exception raised for ignore record"""
    def __init__(self, record, message="Ignore this record"):
        self.record = record
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.record}"