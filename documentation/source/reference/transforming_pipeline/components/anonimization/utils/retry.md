# microservices.transforming_pipeline.components.anonimization.utils.retry

Source file: `microservices\transforming_pipeline\components\anonimization\utils\retry.py`

## Source Code

```python
import time
from random import uniform

def retry_with_backoff(func, max_retries=5, backoff_factor=2):
    """
    Retry a function with exponential backoff.

    Args:
        func (callable): The function to retry.
        max_retries (int): Maximum number of retries.
        backoff_factor (int): Backoff multiplier.

    Returns:
        Any: The result of the function.
    """
    for attempt in range(max_retries):
        try:
            return func()
        except (httpx.ConnectTimeout, APITimeoutError) as e:
            if attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt
                print(f"Retrying in {wait_time} seconds due to: {e}")
                time.sleep(wait_time)
            else:
                raise
```
