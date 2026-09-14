"""Exercise the actual batch-request guard using fake responses; zero network.

Original live receipts are only read for integrity checks and never rewritten.
"""
import importlib.util
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("landing_guard", BASE / "public_locale_readback.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
checks = []

for code in [429, 401, 403]:
    runner.STOP_REQUESTS.clear()
    calls = []

    class FakeOpener:
        def open(self, request, timeout):
            calls.append(request.full_url)
            raise HTTPError(request.full_url, code, "simulated stop", None, None)

    runner.build_opener = lambda *args: FakeOpener()
    with ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(lambda i: runner.fetch(str(i), f"https://www.dresslikemommy.com/example-{i}", "collection"), range(21)))
    assert len(calls) == 1, (code, calls)
    assert sum(r["extraction_status"] == "SKIPPED_GLOBAL_STOP" for r in rows) == 20
    assert rows[0]["attempts"] == 1
    # The same fetch guard blocks any later deep product request.
    deep = runner.fetch("en", "https://www.dresslikemommy.com/products/example", "product")
    assert deep["extraction_status"] == "SKIPPED_GLOBAL_STOP" and len(calls) == 1
    checks.append({"case": f"HTTP{code} stops queued and deep requests", "pass": True, "simulated_network_calls": len(calls)})

chronology = json.loads((BASE / "http_throttle_chronology.json").read_text())
hashes = chronology["original_artifact_sha256"]
assert all(hashlib.sha256((BASE / name).read_bytes()).hexdigest() == sha for name, sha in hashes.items())
checks.append({"case": "all original capture artifacts unchanged", "pass": True, "files": len(hashes)})
result = {"status": "PASS", "external_requests": 0, "live_rerun": "NOT_RUN", "scope": "Simulated guard regression and preserved source receipts; no live or rendered acceptance", "checks": checks, "guarded_runner_sha256": hashlib.sha256((BASE / "public_locale_readback.py").read_bytes()).hexdigest()}
(BASE / "local_guard_validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
