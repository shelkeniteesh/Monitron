class MissingDataMetricsDataException(Exception):
    """Raised when only one of dm_current data or dn_reference data is missing during metrics calculation."""
    def __init__(self, message="Both dm_current_data and dm_reference_data are required but not provided for data metric calculation."):
        self.message = message
        super().__init__(self.message)