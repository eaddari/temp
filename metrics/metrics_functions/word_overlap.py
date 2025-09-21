import re

def tokenize(text: str) -> list:
	text = re.sub(r'[^\w\s]', ' ', text.lower())
	return [word for word in text.split() if word.strip()]

def calculate_word_overlap(generated: str, reference: str) -> dict:
	gen_words = set(tokenize(generated))
	ref_words = set(tokenize(reference))
	if not gen_words or not ref_words:
		return {
			"word_precision": 0.0,
			"word_recall": 0.0,
			"word_f1": 0.0,
			"word_overlap_count": 0
		}
	overlap = gen_words & ref_words
	precision = len(overlap) / len(gen_words)
	recall = len(overlap) / len(ref_words)
	f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
	return {
		"word_precision": precision,
		"word_recall": recall,
		"word_f1": f1,
		"word_overlap_count": len(overlap)
	}
