# microservices.input_integration_pipeline.source.repo_downloader.endpoints.status

Source file: `microservices\input_integration_pipeline\source\repo_downloader\endpoints\status.py`

## Source Code

```python
from fastapi import APIRouter
from typing import Dict

router = APIRouter(prefix="/v1", tags=["Check Status"])

@router.get("/status", summary="Check the status of the API.")
def get_status() -> Dict:
    """
    Check the health status of the API.

    Returns:
        Dict: A dictionary containing the status message
    """
    return {"message": 200}

```
