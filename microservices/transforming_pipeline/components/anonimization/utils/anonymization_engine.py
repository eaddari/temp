from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngine, NlpArtifacts
from transformers import pipeline

class TransformersNlpEngine(NlpEngine):
    def __init__(self):
        self.nlp = pipeline("ner", processors="dbmdz/bert-large-cased-finetuned-conll03-english")

    def analyze_text(self, text, language):
        results = self.nlp(text)
        entities = [
            {"entity_type": res["entity"], "start": res["start"], "end": res["end"]}
            for res in results
        ]
        return NlpArtifacts(entities=entities, tokens=[], language=language)