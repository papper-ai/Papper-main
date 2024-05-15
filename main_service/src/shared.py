from transformers import AutoTokenizer

ml_models = dict()
ml_models["tokenizer"] = AutoTokenizer.from_pretrained("lightblue/suzume-llama-3-8B-multilingual")
