from nltk.translate.meteor_score import meteor_score
from nltk.tokenize import word_tokenize
import re

def tokenize(text: str) -> list:
	"""Tokenize text using NLTK if available, otherwise simple regex."""
	try:
		return word_tokenize(text.lower())
	except Exception:
		text = re.sub(r'[^\w\s]', ' ', text.lower())
		return [word for word in text.split() if word.strip()]

def calculate_meteor(generated: str, reference: str) -> dict:
	"""Calculate METEOR score using official NLTK implementation."""
	reference_tokens = tokenize(reference)
	generated_tokens = tokenize(generated)
	meteor = meteor_score([reference_tokens], generated_tokens)
	return {"meteor_score": meteor}
