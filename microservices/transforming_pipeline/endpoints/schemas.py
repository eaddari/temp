from pydantic import BaseModel
from typing import List, Optional

class PipelineRequest(BaseModel):
    input_path: str
    keep_comments: bool = False
    steps: list