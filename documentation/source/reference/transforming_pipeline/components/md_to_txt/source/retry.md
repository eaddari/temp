# microservices.transforming_pipeline.components.md_to_txt.source.retry

Source file: `microservices\transforming_pipeline\components\md_to_txt\source\retry.py`

## Source Code

```python
import asyncio
import logging

async def retry_async(func,*args, retries=3, delay=0.5, **kwargs):
    for attempt in range(retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                logging.error(f"Function failed after {retries} attempts: {e}")
                raise
            
async def safe_convert(func, text, retries=3, delay=0.5):
    try:
        return await retry_async(func, text, retries=retries, delay=delay)
    except Exception:
        return text
```
