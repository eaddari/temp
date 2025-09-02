# FileConverter - Markdown & reStructuredText to Text

Questo modulo fornisce una classe e funzioni asincrone per convertire file Markdown (`.md`) e reStructuredText (`.rst`) in testo HTML, utilizzando pandas DataFrame come input.

## Funzionalità
- Conversione asincrona di testo Markdown in HTML tramite `md_to_text`
- Conversione asincrona di testo reStructuredText in HTML tramite `rst_to_text`
- Classe `FileConverter` per gestire DataFrame contenenti file multipli e restituire un DataFrame con i contenuti convertiti

## Utilizzo

### 1. Funzioni di conversione
```python
import asyncio
from components.md_to_txt.source.converter import md_to_text, rst_to_text

md = "# Titolo\nTesto **importante**."
rst = "Titolo\n====="

html_md = asyncio.run(md_to_text(md))
html_rst = asyncio.run(rst_to_text(rst))
```

### 2. Classe FileConverter
```python
import pandas as pd
from components.md_to_txt.source.converter import FileConverter
import asyncio

df = pd.DataFrame({
    'name': ['file1.md', 'file2.rst'],
    'content': ["# Titolo", "Titolo\n====="]
})
converter = FileConverter(df, ['.md', '.rst'])
result_df = asyncio.run(converter.file_to_text())
print(result_df)
```

## Requisiti
- pandas
- markdown
- docutils
- logging
- asyncio

Installa i pacchetti necessari:
```bash
pip install pandas markdown docutils
```

## Testing
Vedi `test_converter.py` per test automatici con `pytest` e `pytest-asyncio`.

## Note
- La conversione restituisce HTML, non testo puro.
- Gestione degli errori tramite logging.
- Supporto estendibile per altri formati aggiungendo funzioni e mappature.
