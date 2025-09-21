from bert_score import score as bert_score

def calculate_bertscore(generated: str, reference: str) -> dict:
	"""Calculate BERTScore using official bert-score library."""
	P, R, F1 = bert_score([generated], [reference], lang="en", verbose=False)
	return {
		"bertscore_precision": P.item(),
		"bertscore_recall": R.item(),
		"bertscore_f1": F1.item()
	}
