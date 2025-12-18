"""
Exception classes for DI-2D
"""
from fastapi import HTTPException, status

class DI2DException(HTTPException):
    """Base exception for DI-2D"""
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code=status_code, detail=detail)

class AIKeyError(DI2DException):
    """AI API key missing or invalid"""
    def __init__(self, detail: str = "AI API key is missing or invalid"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

class FileProcessingError(DI2DException):
    """Error processing uploaded file"""
    def __init__(self, detail: str = "Failed to process uploaded file"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

class AnalysisError(DI2DException):
    """Error during AI analysis"""
    def __init__(self, detail: str = "Analysis failed"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
