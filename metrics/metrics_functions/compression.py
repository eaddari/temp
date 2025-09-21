import re

def tokenize(text: str) -> list:
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    return [word for word in text.split() if word.strip()]

def calculate_compression_ratio(generated: str, reference: str) -> dict:
    char_ratio = len(generated) / len(reference) if len(reference) > 0 else 0
    gen_words = len(tokenize(generated))
    ref_words = len(tokenize(reference))
    word_ratio = gen_words / ref_words if ref_words > 0 else 0
    gen_sentences = len([s for s in generated.split('.') if s.strip()])
    ref_sentences = len([s for s in reference.split('.') if s.strip()])
    sentence_ratio = gen_sentences / ref_sentences if ref_sentences > 0 else 0
    return {
        "character_compression_ratio": char_ratio,
        "word_compression_ratio": word_ratio,
        "sentence_compression_ratio": sentence_ratio,
        "generated_length": len(generated),
        "reference_length": len(reference),
        "generated_words": gen_words,
        "reference_words": ref_words
    }
