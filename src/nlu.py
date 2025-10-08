from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sentence_transformers import SentenceTransformer
import numpy as np
import openai
from .config import Config

# Simple TF-IDF + Logistic classifier for intents
class IntentClassifier:
    def __init__(self):
        self.pipeline = make_pipeline(
            TfidfVectorizer(ngram_range=(1,2), max_features=10000),
            LogisticRegression(class_weight="balanced", max_iter=1000)
        )
        self.labels = None

    def train(self, X, y):
        self.pipeline.fit(X, y)
        self.labels = list(set(y))

    def predict(self, text):
        return self.pipeline.predict([text])[0]

# Optional semantic matching using sentence-transformers
class SemanticMatcher:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(model_name)

    def embed(self, texts):
        return self.embedder.encode(texts, convert_to_numpy=True)

    def similarity(self, query, candidates):
        qv = self.embed([query])
        cvs = self.embed(candidates)
        sim = (qv @ cvs.T).squeeze()
        idx = int(np.argmax(sim))
        return idx, float(sim[idx])

# LLM helper for generating next utterance or summary (OpenAI example)
def generate_agent_response(system_prompt, conversation_history, temperature=0.0, max_tokens=150):
    if not Config.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set for LLM generation.")
    openai.api_key = Config.OPENAI_API_KEY
    prompt = system_prompt + "\n\nConversation:\n" + conversation_history
    resp = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return resp.choices[0].text.strip()
