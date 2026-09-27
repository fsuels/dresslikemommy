"""Load the runner engine for one spec without touching Shopify (for seeding/analysis)."""
import json, os
from pathlib import Path
ENGINE = Path(__file__).resolve().parent / "runner_engine.py"

def load(spec_path):
    os.environ.setdefault("SHOPIFY_STORE_DOMAIN", "offline.invalid")
    os.environ.setdefault("SHOPIFY_ADMIN_ACCESS_TOKEN", "offline")
    ns = {"__name__": "engine_offline", "SPEC": json.loads(Path(spec_path).read_text(encoding="utf-8"))}
    code = "from __future__ import annotations\n" + ENGINE.read_text(encoding="utf-8")
    exec(compile(code, str(ENGINE), "exec"), ns)
    return ns
