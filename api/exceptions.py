class APIError(Exception):
    """Exception raised for API-related errors."""
    
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response
    
    def __str__(self):
        if self.status_code:
            return f"APIError {self.status_code}: {self.message}"
        return f"APIError: {self.message}"