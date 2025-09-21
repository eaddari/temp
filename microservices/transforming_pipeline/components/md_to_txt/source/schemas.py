from pydantic import BaseModel
from typing import Optional

"""
Schemas for FastAPI endpoints related to file conversion.

Defines request and response models for converting files to text.
"""

class ParquetConverterResponse(BaseModel):
    """
    Response model for file conversion to text.

    Attributes
    ----------
    status : bool
        Whether the conversion was successful.
    details : str
        Details about the conversion process.
    output_path : str, optional
        Path to the output file, if available.
    """
    status: bool
    details: str
    output_path: Optional[str] = None

class ParquetConverterRequest(BaseModel):
    """
    Request model for file conversion to text.

    Attributes
    ----------
    input_path : str
        Path to the input file.
    output_path : str
        Path to the output file.
    """
    input_path: str
    output_path: str