import json
import os

from gpt_index import LLMPredictor, GPTSimpleVectorIndex
from langchain import OpenAI


def load_json(path):
    with open(path, 'r') as f:
        d_ = json.load(f)
    return d_


def save_json(path, obj):
    with open(path, 'w') as f:
        json.dump(obj, f)


def get_auth(path=''):
    auth_path = './config/auth.json'
    if not path:
        path = auth_path
    return load_json(path)


def get_llm_model():
    llm_predictor_high = LLMPredictor(OpenAI(temperature=0, model_name="text-davinci-003"))
    # llm_predictor_cheep = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-ada-001"))
    # llm_predictor_cheep = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-babbage-001"))
    llm_predictor_cheep = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-curie-001"))
    # llm_predictor_cheep = OpenAI(temperature=0, model_name="text-ada-001")
    model_map = {'high': llm_predictor_high, 'cheep': llm_predictor_cheep}
    return model_map


def _preprocess(index_file):
    os.environ['OPENAI_API_KEY'] = get_auth()['token']
    index = GPTSimpleVectorIndex.load_from_disk(index_file)
    model_map = get_llm_model()
    return index, model_map
