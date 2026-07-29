import time, json, urllib.request, sys

TID = "e870c630"

def get():
    with urllib.request.urlopen(f"http://127.0.0.1:8000/api/tasks/{TID}") as r:
        return json.load(r)

deadline = time.time() + 540
while time.time() < deadline:
    d = get()
    st = d.get("status")
    extra = d.get("extra")
    log = d.get("log", "")
    nlines = log.count("\n")
    print(f"[poll] status={st} loglines={nlines} has_extra={bool(extra)}", flush=True)
    if extra:
        print("EXTRA=" + json.dumps(extra, ensure_ascii=False)[:800], flush=True)
    if st in ("done", "error"):
        print("=== LOG TAIL (last 1800) ===", flush=True)
        print(log[-1800:], flush=True)
        break
    time.sleep(15)
else:
    print("TIMEOUT: still running", flush=True)
