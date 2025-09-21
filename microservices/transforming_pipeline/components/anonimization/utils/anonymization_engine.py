from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngine, NlpArtifacts
from transformers import pipeline

class TransformersNlpEngine(NlpEngine):
    """
    NLP Engine using HuggingFace Transformers for Named Entity Recognition (NER).

    Methods
    -------
    analyze_text(text, language):
        Analyze text and return detected entities as NlpArtifacts.
    """
    def __init__(self):
        self.nlp = pipeline("ner", processors="dbmdz/bert-large-cased-finetuned-conll03-english")

    def analyze_text(self, text, language):
        results = self.nlp(text)
        entities = [
            {"entity_type": res["entity"], "start": res["start"], "end": res["end"]}
            for res in results
        ]
        return NlpArtifacts(entities=entities, tokens=[], language=language)