from rouge_score import rouge_scorer

def calculate_rouge(generated: str, reference: str) -> dict:
	"""Calculate ROUGE scores using official rouge-score library."""
	scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
	scores = scorer.score(reference, generated)
	return {
		"rouge1_f1": scores['rouge1'].fmeasure,
		"rouge2_f1": scores['rouge2'].fmeasure,
		"rougeL_f1": scores['rougeL'].fmeasure,
		"rouge1_precision": scores['rouge1'].precision,
		"rouge1_recall": scores['rouge1'].recall,
		"rouge2_precision": scores['rouge2'].precision,
		"rouge2_recall": scores['rouge2'].recall,
		"rougeL_precision": scores['rougeL'].precision,
		"rougeL_recall": scores['rougeL'].recall,
	}
