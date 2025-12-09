import json, sys, csv

def read(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def main(inp, out_csv):
    data = read(inp)
    rows = []
    if "table" in data:
        head = data["table"]["head"]
        body = data["table"]["body"]
        var_names = head.get("vars", [])
        for b in body:
            vars_ = {k:v for k,v in zip(var_names, b["vars"])}
            for out in b["outputs"]:
                try:
                    obj = json.loads(out.get("text",""))
                    rows.append(obj)
                except Exception:
                    pass
    elif "results" in data:
        for r in data["results"]:
            try:
                obj = json.loads(r.get("output","") or r.get("text",""))
                rows.append(obj)
            except Exception:
                pass

    total = len(rows) or 1
    json_ok = len(rows)
    citation_ok = sum(1 for o in rows if isinstance(o, dict) and isinstance(o.get("citations"), list) and len(o["citations"]) > 0)
    unsafe_ok = sum(1 for o in rows if isinstance(o, dict) and (o.get("safety","").lower() in ["safe","unsafe"]))

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric","value"])
        w.writerow(["json_rate", f"{json_ok/total:.3f}"])
        w.writerow(["citation_rate", f"{citation_ok/total:.3f}"])
        w.writerow(["safety_field_rate", f"{unsafe_ok/total:.3f}"])
    print(f"Wrote {out_csv} with {total} rows")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python tools/metrics.py results.json metrics.csv")
        raise SystemExit(2)
    main(sys.argv[1], sys.argv[2])
