# microservices.transforming_pipeline.components.anonimization.source.anonimizator_local

Source file: `microservices\transforming_pipeline\components\anonimization\source\anonimizator_local.py`

## Source Code

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import re
from components.anonimization.utils.patterns import SECRET_PATTERNS
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from components.anonimization.utils.anonymization_engine import TransformersNlpEngine

class DataFrameAnonymizer:
    def __init__(self):
        self.allowed_entities = ['PERSON', 'PHONE_NUMBER', 'EMAIL_ADDRESS', 'IP_ADDRESS']
        self.score_threshold = 0.8
        self.analyzer = AnalyzerEngine(TransformersNlpEngine())
        self.anonymizer = AnonymizerEngine()
        self.combined_patterns = [re.compile(p, re.IGNORECASE) if '(?i)' in p else re.compile(p) for p in SECRET_PATTERNS]

    def regex_anonymization(self, series):
        return series.str.replace(self.combined_patterns, '***', regex=True)

    def presidio_anonymization(self, text):
        results = self.analyzer.analyze(
            text=text,
            language='en',
            score_threshold=self.score_threshold
        )
        filtered_results = [result for result in results if result.entity_type in self.allowed_entities]
        anonymized_text = self.anonymizer.anonymize(text=text, analyzer_results=filtered_results)
        return anonymized_text.text

    def anonymize(self, df, column='content'):
        df = df.copy()
        df[column] = self.regex_anonymization(df[column])

        df[column] = df[column].swifter.apply(self.presidio_anonymization)

        with ProcessPoolExecutor() as executor:
            df[column] = list(executor.map(self.presidio_anonymization, df[column]))
        return df
    


# approccio ibrido con llm che fornisce coordinata della stringa da sostituire
```
