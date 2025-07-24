from transformers.pipelines import pipeline as hf_pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM
import torch
import threading
from collections.abc import Iterable

# Global model cache
_model_cache = {}
_model_lock = threading.Lock()

def get_toxicity_pipeline():
    with _model_lock:
        if 'toxicity' not in _model_cache:
            model_name = 'unitary/toxic-bert'
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
            _model_cache['toxicity'] = hf_pipeline('text-classification', model=model, tokenizer=tokenizer)
        return _model_cache['toxicity']

def get_t5_pipeline():
    with _model_lock:
        if 't5' not in _model_cache:
            model_name = 't5-base'
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            _model_cache['t5'] = hf_pipeline('text2text-generation', model=model, tokenizer=tokenizer, max_length=128)
        return _model_cache['t5']

def get_flan_t5_small_pipeline():
    with _model_lock:
        if 'flan-t5-small' not in _model_cache:
            model_name = 'google/flan-t5-small'
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            _model_cache['flan-t5-small'] = hf_pipeline('text2text-generation', model=model, tokenizer=tokenizer, max_length=128)
        return _model_cache['flan-t5-small']


def detect_toxicity(text, model_name):
    pipe = get_toxicity_pipeline()
    result = pipe(text)
    if not isinstance(result, list):
        try:
            if isinstance(result, Iterable):
                result = list(result)
            else:
                result = []
        except Exception:
            result = []
    result = result[0] if result and isinstance(result[0], dict) else {}
    print("DEBUG: id2label:", getattr(pipe.model.config, 'id2label', None))
    print("DEBUG: Model output:", result)
    label = str(result.get('label', '')).lower() if isinstance(result, dict) else ''
    score = float(result.get('score', 0.0)) if isinstance(result, dict) else 0.0
    # If score is 0, always non-toxic
    if score == 0.0:
        toxic = False
    else:
        toxic = label == 'toxic'
    return {"toxic": toxic, "score": score}

def rewrite_text(text, model_name=None):
    t5_pipe = get_flan_t5_small_pipeline()
    prompt = (
        "You are an assistant that rewrites software/code-related comments to be neutral, professional, and respectful. "
        "Remove any insults, offensive language, or toxicity, but keep all technical meaning and intent. "
        "Do not add unrelated information or change the topic. Only rephrase the original comment in a more respectful way.\n"
        "\n"
        "Example 1:\n"
        "Original: What a piece of crap. Only an idiot would write such garbage code.\n"
        "Rewritten: This code could be improved. There are several issues that need to be addressed.\n"
        "\n"
        "Example 2:\n"
        "Original: You must be the dumbest person to think this library is useful. Just quit coding forever.\n"
        "Rewritten: I don't find this library useful for my needs. Perhaps consider a different approach.\n"
        "\n"
        "Example 3:\n"
        "Original: This is the worst implementation I've ever seen. Did you even test it?\n"
        "Rewritten: This implementation could be improved. Have you considered testing it further?\n"
        "\n"
        f"Original: {text}\nRewritten:"
    )
    result = t5_pipe(prompt)
    if not isinstance(result, list):
        try:
            if isinstance(result, Iterable):
                result = list(result)
            else:
                result = []
        except Exception:
            result = []
    result = result[0] if result and isinstance(result[0], dict) else {}
    rewritten = str(result.get('generated_text', '')).strip() if isinstance(result, dict) else ''
    # Remove any leading 'Rewritten:' or similar
    if rewritten.lower().startswith('rewritten:'):
        rewritten = rewritten[len('rewritten:'):].strip()
    # Remove the original comment if present in the output
    if text in rewritten:
        rewritten = rewritten.replace(text, '').strip()
    # Fallback: If rewritten is empty or too short, use the fallback message
    if not rewritten or len(rewritten.split()) < 3:
        rewritten = "The original comment was too toxic to rephrase. Please consider rewording it."
    return rewritten 