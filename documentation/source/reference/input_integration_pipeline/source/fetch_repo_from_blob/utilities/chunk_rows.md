# microservices.input_integration_pipeline.source.fetch_repo_from_blob.utilities.chunk_rows

Source file: `microservices\input_integration_pipeline\source\fetch_repo_from_blob\utilities\chunk_rows.py`

## Source Code

```python
from typing import List, Any, Iterable

def chunk_rows(rows: List[Any], chunk_size: int) -> Iterable[List[Any]]:
    """
    Splitta il file che arriva in input in chunk di righe di dimensione massima chunk_size.
    Args:
        rows (list): lista di righe da splittare.
        chunk_size (int): La dimensione massima di righe per chunk.
    Yields:
        list: Un chunk di righe.
    """
    for i in range(0, len(rows), chunk_size):
        yield rows[i:i + chunk_size]
```
