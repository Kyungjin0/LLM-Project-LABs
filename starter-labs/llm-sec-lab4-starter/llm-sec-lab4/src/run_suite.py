import os, json, argparse, time
from typing import Callable, Dict, Any, List
from dotenv import load_dotenv
from google import genai
from src.guardrails import load_policy, check_input, check_output, build_user_prompt, call_model, enforce_output_schema


def process_attack(atk: str, mode: str, policy: Dict[str, Any], *, call_model_fn: Callable[[Any, str, str], str], client, model_id: str) -> Dict[str, Any]:
    item = {"attack": atk, "mode": mode}
    if mode == "guarded":
        ok, reason = check_input(policy, atk)
        if not ok:
            item.update({"blocked": True, "stage": "input", "reason": reason, "model_text": "", "decision": {"is_safe":"no","rationale":reason}})
            return item

    prompt = build_user_prompt(atk)
    model_text = call_model_fn(client, model_id, prompt)

    if mode == "guarded":
        ok, reason = check_output(policy, model_text)
        if not ok:
            item.update({"blocked": True, "stage": "output", "reason": reason, "model_text": model_text, "decision": {"is_safe":"no","rationale":reason}})
            return item

    valid, err, obj = enforce_output_schema(model_text)
    item.update({"blocked": False, "stage": "none", "reason": "", "model_text": model_text, "schema_ok": valid, "schema_err": err, "decision": obj})
    return item


def run(attacks: List[str], mode: str, out_path: str, *, client=None, model_id: str | None = None, policy=None, call_model_fn=call_model, sleep_seconds: float = 0.2) -> str:
    if client is None:
        load_dotenv()
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        model_id = os.getenv("MODEL_ID","gemini-2.5-flash")
    if policy is None:
        policy = load_policy("config/policy.yaml")

    results = []
    for i, atk in enumerate(attacks, 1):
        item = process_attack(atk, mode, policy, call_model_fn=call_model_fn, client=client, model_id=model_id)
        item["id"] = i
        results.append(item)
        time.sleep(max(sleep_seconds, 0))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Wrote {out_path}")
    return out_path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["unguarded","guarded"], required=True)
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--attacks", default="attacks/attacks.txt")
    p.add_argument("--policy", default="config/policy.yaml")
    p.add_argument("--out", default=None)
    args = p.parse_args()

    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model_id = os.getenv("MODEL_ID","gemini-2.5-flash")
    attacks = [l.strip() for l in open(args.attacks, encoding="utf-8").read().splitlines() if l.strip() and not l.startswith("#")][:args.limit]
    policy = load_policy(args.policy)
    out = args.out or f"reports/{args.mode}.json"

    run(attacks, args.mode, out, client=client, model_id=model_id, policy=policy)


if __name__ == "__main__":
    main()
