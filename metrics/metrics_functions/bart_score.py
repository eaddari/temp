from transformers import BartForConditionalGeneration, BartTokenizer
import torch

def calculate_bart_score(generated, reference, model_name="facebook/bart-large-cnn"):
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    inputs = tokenizer(generated, return_tensors="pt", truncation=True, max_length=1024)
    labels = tokenizer(text_target=reference, return_tensors="pt", truncation=True, max_length=1024)

    with torch.no_grad():
        outputs = model(**inputs, labels=labels["input_ids"])
        return -outputs.loss.item()

