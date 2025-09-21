# microservices.input_integration_pipeline.source.fetch_repo_from_blob.source.schemas

Source file: `microservices\input_integration_pipeline\source\fetch_repo_from_blob\source\schemas.py`

## Source Code

```python
from pydantic import BaseModel
from typing import Optional

### Blob schemas for FastAPI ###

# Requests
class BlobRequest(BaseModel):
    container_name: str
    blob_name: str

class BlobToParquetRequest(BaseModel):
    container_name: str
    blob_name: str

# Responses
class BlobDownloadResponse(BaseModel):
    status: bool
    details: str

### Container schemas for FastAPI ###

# Requests
class ContainerRequest(BaseModel):
    container_name: str

class ContainerDownloadRequest(BaseModel):
    container_name: str

class FilesByTypeRequest(BaseModel):
    container_name: str
    file_extension: str

class ContainerToParquetRequest(BaseModel):
    container_name: str
    single_parquet: Optional[bool] = False


# Responses
class ContainerAccessResponse(BaseModel):
    status: bool
    details: str

class ContainerDownloadResponse(BaseModel):
    status: bool
    details: str
    content: str

class FilesByTypeResponse(BaseModel):
    status: bool
    details: str
    files: list

```
