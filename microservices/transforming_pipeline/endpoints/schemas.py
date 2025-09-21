from pydantic import BaseModel
from typing import List, Optional

class PipelineRequest(BaseModel):
    """
    Request model for pipeline execution.

    Attributes
    ----------
    input_path : str
        Path to the input data file.
    keep_comments : bool, optional
        Whether to keep comments in the output (default is False).
    steps : list
        List of transformation steps to execute.
    """
    input_path: str
    keep_comments: bool = False
    steps: list