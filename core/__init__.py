"""
Domain configuration loader.

Each domain is a folder under domains/ containing:
  - domain.yaml   — categories, query_pool, personas, MCP config, metadata schema
  - distiller_prompt.md  — Gemini prompt for skill extraction
  - planner_prompts.py   — (optional) task decomposition prompts
"""
from __future__ import annotations

import yaml
from pathlib import Path

_DOMAINS_DIR = Path(__file__).resolve().parent.parent / "domains"

_VALID_EXECUTION_MODES = {"sync_engine", "async_mcp"}

# Keys required for all domains.
_REQUIRED_KEYS = {
    "name", "display_name", "categories", "mcp",
    "agent_prompt_file",
}

# Keys required for new domains (those that declare execution_mode).
_REQUIRED_KEYS_NEW = _REQUIRED_KEYS | {
    "execution_mode", "persona", "query_pool", "failure_patterns",
    "tools_fallback_file",
}


def _find_domains_dir() -> Path:
    """Locate the domains/ directory relative to this file."""
    return _DOMAINS_DIR


def load_domain(name: str, domains_dir: Path | None = None) -> dict:
    """Load a domain configuration by name.

    Args:
        name: Domain name (must match a subfolder in domains/).
        domains_dir: Override domains directory.

    Returns:
        Parsed domain config dict with resolved paths.
    """
    base = Path(domains_dir) if domains_dir else _find_domains_dir()
    domain_dir = base / name
    config_path = domain_dir / "domain.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Domain config not found: {config_path}\n"
            f"Available domains: {list_domains(base)}"
        )

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Resolve paths relative to domain dir.
    config["_domain_dir"] = domain_dir
    config["_distiller_prompt_path"] = domain_dir / "distiller_prompt.md"

    # Ensure required fields.
    config.setdefault("name", name)
    config.setdefault("categories", {})
    config.setdefault("query_pool", [])
    config.setdefault("rerank_prompt", "")
    config.setdefault("metadata_fields", {})
    config.setdefault("mcp", None)
    config.setdefault("execution_mode", None)  # None = legacy domain (not validated)

    # Build flat category list (keys of the categories dict).
    config["category_list"] = list(config["categories"].keys()) + ["other"]

    # Build keyword map: category -> flat list of keywords.
    config["category_keywords"] = {}
    for cat, keywords in config["categories"].items():
        if isinstance(keywords, list):
            config["category_keywords"][cat] = keywords
        elif isinstance(keywords, dict):
            # Support nested structure: {en: [...], zh: [...]}
            flat = []
            for v in keywords.values():
                if isinstance(v, list):
                    flat.extend(v)
            config["category_keywords"][cat] = flat

    return config


def validate_domain(name: str, domains_dir: Path | None = None) -> list[str]:
    """Validate a domain configuration and return a list of error messages.

    Returns an empty list if the domain is valid.
    """
    errors: list[str] = []
    try:
        config = load_domain(name, domains_dir)
    except FileNotFoundError as e:
        return [str(e)]

    domain_dir = config["_domain_dir"]
    execution_mode = config.get("execution_mode")

    # If execution_mode is declared, enforce new-domain validation.
    if execution_mode is not None:
        if execution_mode not in _VALID_EXECUTION_MODES:
            errors.append(
                f"Invalid execution_mode: '{execution_mode}'. "
                f"Must be one of: {sorted(_VALID_EXECUTION_MODES)}"
            )

        for key in _REQUIRED_KEYS_NEW:
            if key not in config or config[key] is None:
                errors.append(f"Missing required key: '{key}'")
    else:
        # Legacy domain — just check basics.
        for key in _REQUIRED_KEYS:
            if key not in config or config[key] is None:
                # mcp can be None for dry-run-only domains.
                if key == "mcp":
                    continue
                errors.append(f"Missing required key: '{key}'")

    # Check that referenced files exist.
    agent_prompt_file = config.get("agent_prompt_file")
    if agent_prompt_file:
        if not (domain_dir / agent_prompt_file).exists():
            errors.append(f"agent_prompt_file not found: {agent_prompt_file}")

    tools_fallback_file = config.get("tools_fallback_file")
    if tools_fallback_file:
        if not (domain_dir / tools_fallback_file).exists():
            errors.append(f"tools_fallback_file not found: {tools_fallback_file}")

    if not config.get("categories"):
        errors.append("categories is empty — must define at least one category")

    return errors


def list_domains(domains_dir: Path | None = None) -> list[str]:
    """List available domain names."""
    base = Path(domains_dir) if domains_dir else _find_domains_dir()
    if not base.exists():
        return []
    return sorted(
        d.name for d in base.iterdir()
        if d.is_dir() and (d / "domain.yaml").exists()
    )


def get_distiller_prompt(domain_config: dict) -> str:
    """Load the distiller prompt for a domain."""
    path = domain_config.get("_distiller_prompt_path")
    if path and Path(path).exists():
        return Path(path).read_text(encoding="utf-8")
    raise FileNotFoundError(f"Distiller prompt not found: {path}")


def get_library_dir(domain_name: str) -> Path:
    """Return the active skills directory for a domain.

    Honours the per-domain ``library_backend`` flag in ``domain.yaml``:

      - ``library_backend: legacy`` (default) → ``skills_library/<domain>/``
      - ``library_backend: wiki`` → ``skills_wiki/<domain>/``

    The chosen directory is created if missing so callers can rely on the
    path existing.
    """
    project_root = Path(__file__).resolve().parent.parent
    backend = "legacy"
    try:
        domain_config = load_domain(domain_name)
        backend = str(domain_config.get("library_backend", "legacy")).lower()
    except (FileNotFoundError, ValueError):
        backend = "legacy"
    if backend == "wiki":
        lib_dir = project_root / "skills_wiki" / domain_name
    else:
        lib_dir = project_root / "skills_library" / domain_name
    lib_dir.mkdir(parents=True, exist_ok=True)
    return lib_dir


def get_active_library_backend(domain_name: str) -> str:
    """Return the configured backend label for a domain (``legacy`` or ``wiki``)."""
    try:
        domain_config = load_domain(domain_name)
    except (FileNotFoundError, ValueError):
        return "legacy"
    value = str(domain_config.get("library_backend", "legacy")).lower()
    return value if value in {"legacy", "wiki"} else "legacy"
