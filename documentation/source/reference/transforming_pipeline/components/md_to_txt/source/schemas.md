# microservices.transforming_pipeline.components.md_to_txt.source.schemas

Source file: `microservices\transforming_pipeline\components\md_to_txt\source\schemas.py`

## Source Code

```python
from pydantic import BaseModel
from typing import Optional

### Schemas for FastAPI ###

class ParquetConverterResponse(BaseModel):
    status: bool
    details: str
    output_path: Optional[str] = None

class ParquetConverterRequest(BaseModel):
    input_path: str
    output_path: str
```
