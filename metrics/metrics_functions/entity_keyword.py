import re
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

model_name = "microsoft/codebert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)


ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

def extract_entities_keywords(text: str):

    ner_results = ner_pipeline(text)
    entities = [result['word'] for result in ner_results if result['entity'].startswith("B-")]

    tokens = tokenizer.tokenize(text)
    keywords = [token for token in tokens if token.isalpha() and len(token) > 2]

    return entities, keywords

def calculate_entity_keyword_recall(generated: str, reference: str) -> dict:
    ref_entities, ref_keywords = extract_entities_keywords(reference)
    gen_entities, gen_keywords = extract_entities_keywords(generated)
    if ref_entities:
        entity_overlap = len(set(gen_entities) & set(ref_entities))
        entity_recall = entity_overlap / len(set(ref_entities))
    else:
        entity_recall = 0.0
    if ref_keywords:
        keyword_overlap = len(set(gen_keywords) & set(ref_keywords))
        keyword_recall = keyword_overlap / len(set(ref_keywords))
    else:
        keyword_recall = 0.0
    return {
        "entity_recall": entity_recall,
        "keyword_recall": keyword_recall,
        "entities_found": len(set(gen_entities) & set(ref_entities)),
        "total_reference_entities": len(set(ref_entities)),
        "keywords_found": len(set(gen_keywords) & set(ref_keywords)),
        "total_reference_keywords": len(set(ref_keywords))
    }
