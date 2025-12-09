import os, argparse, json
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from google import genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.common.logger import log
from src.common.guards import input_guard, output_guard, enforce_json_schema

SYSTEM = "You answer questions using ONLY the provided documents. Return JSON with {answer, citations, safety, rationale}. If evidence is weak, set safety='unsafe' and explain."

def load_docs(folder: Path):
    docs = []
    for p in sorted(folder.glob("*.txt")):
        docs.append((p.name, p.read_text(encoding='utf-8')))
    return docs

def retrieve(docs, query, k=3):
    ids = [d[0] for d in docs]
    corpus = [d[1] for d in docs]
    vec = TfidfVectorizer().fit(corpus + [query])
    X = vec.transform(corpus)
    q = vec.transform([query])
    sims = cosine_similarity(q, X).ravel()
    order = sims.argsort()[::-1][:k]
    return [(ids[i], corpus[i]) for i in order]

def build_prompt(query, evid):
    chunks = "\n\n".join([f"[{i}] {t}" for i,(i,t) in enumerate(evid, 1)])
    ids = [i for i,_ in evid]
    return f\"\"\"Use ONLY these documents to answer. Cite ids: {ids}.
QUESTION: {query}
DOCUMENTS:
{chunks}
Return strictly JSON with keys: answer, citations (array of doc ids), safety ('safe'|'unsafe'), rationale.
\"\"\"

def call_llm(client, model, prompt):
    resp = client.models.generate_content(model=model, contents=prompt, config={"system_instruction": SYSTEM})
    return resp.text or ""

def run(question: str, k: int = 3, client=None, model: Optional[str] = None):
    """Execute the RAG pipeline and return a JSON-serialisable dict."""
    if client is None:
        load_dotenv()
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        model = os.getenv("MODEL_ID", "gemini-2.5-flash")

    ok, reason = input_guard(question)
    if not ok:
        log({"track":"rag","phase":"input_block","reason":reason,"q":question})
        return {"answer":"","citations":[],"safety":"unsafe","rationale":reason}

    docs = load_docs(Path("data/corpus"))
    evid = retrieve(docs, question, k=k)
    prompt = build_prompt(question, evid)

    raw = call_llm(client, model, prompt)
    ok, reason = output_guard(raw)
    if not ok:
        log({"track":"rag","phase":"output_block","reason":reason,"raw":raw[:200]})
        return {"answer":"","citations":[],"safety":"unsafe","rationale":reason}

    valid, err, obj = enforce_json_schema(raw)
    if not valid:
        log({"track":"rag","phase":"schema_error","err":err,"raw":raw[:200]})
        return {"answer":"","citations":[],"safety":"unsafe","rationale":"Invalid JSON from model"}

    log({"track":"rag","phase":"ok","q":question,"resp":obj})
    return obj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()

    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model = os.getenv("MODEL_ID", "gemini-2.5-flash")

    result = run(args.question, k=args.k, client=client, model=model)
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
