import json
from pathlib import Path

from .models import LLMTemplate, WebuiConfig
from .security import encrypt, decrypt

CONFIG_PATH = Path(__file__).resolve().parent.parent / "webui_config.json"
DEFAULT_PROJECTS_ROOT = Path(__file__).resolve().parent.parent / "projects"


def mask_key(key: str) -> str:
    if not key:
        return ""
    if len(key) <= 8:
        return "****"
    return key[:3] + "*" * (len(key) - 7) + key[-4:]


def load() -> WebuiConfig:
    if CONFIG_PATH.exists():
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        for t in data.get("templates", {}).values():
            enc = t.pop("api_key_enc", None)
            t["api_key"] = decrypt(enc) if enc else ""
        return WebuiConfig(**data)
    cfg = WebuiConfig(projects_root=str(DEFAULT_PROJECTS_ROOT))
    save(cfg)
    return cfg


def save(cfg: WebuiConfig) -> None:
    data = cfg.model_dump()
    for t in data.get("templates", {}).values():
        if t.get("api_key"):
            t["api_key_enc"] = encrypt(t["api_key"])
        t.pop("api_key", None)
    CONFIG_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def public_template(name: str, t: LLMTemplate, active: str) -> dict:
    d = t.model_dump()
    d.pop("api_key", None)
    d["api_key_masked"] = mask_key(t.api_key)
    d["is_active"] = name == active
    return d
