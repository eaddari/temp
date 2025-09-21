# microservices.transforming_pipeline.components.anonimization.utils.chunk_df

Source file: `microservices\transforming_pipeline\components\anonimization\utils\chunk_df.py`

## Source Code

```python
def chunk_dataframe(df, chunk_size):
    for i in range(0, len(df), chunk_size):
        yield df.iloc[i:i + chunk_size]
```
