# Web wash frozen fixtures (v1)

Round-11 contract: this directory holds canonical-tuple snapshots of
washed wiki entries. ``wiki-wash --frozen-fixtures`` re-loads these
during a wash and reports any drift between the historical snapshot
and the current run via ``fixture_violations`` in ``wash_report.json``.

## Layout

```
web_v1/
  <skill_id>.json          # canonical-tuple snapshot (REQUIRED)
  <skill_id>/              # optional source-of-record payload
                           # (skill.json + code/ + text/) used to seed
                           # the wash; not consumed by the loader
```

Each top-level ``<skill_id>.json`` carries the keys
``_load_frozen_fixtures`` reads:

```json
{
  "skill_id": "skill_a",
  "tier": "T3",
  "category_path": ["finance", "reporting"],
  "source": {"type": "manual"},
  "exec_ok": true,
  "schema_version": "1.0.0",
  "wash_version": "1.0.0"
}
```

## Acceptance criteria addressed

* AC-2 (deterministic wash) — ``wiki-wash --frozen-fixtures
  fixtures/wash/web_v1`` must report ``fixture_violations: 0`` on
  every machine.
* AC-3 (smoke fixtures) — paired with ``domains/web/smoke_fixtures/``
  for the deterministic gate inside ``core/skill_wiki/qa.py``.

## Re-generating snapshots

When the wash output legitimately changes (e.g. tier inference rule
updated), re-emit the snapshots via:

```
python cli.py wiki-wash --domain web \
    --emit-frozen-fixture-update fixtures/wash/web_v1
```

The ``--emit-frozen-fixture-update`` flag overwrites the top-level
``<skill_id>.json`` files for every skill currently in the registry.
The nested payload directories are left alone.

## CLI fail-on-empty

``wiki-wash --frozen-fixtures <dir>`` will refuse to run when ``<dir>``
exists but loads zero fixtures (Round-11 task64). This prevents the
silent ``fixture_violations=0`` that masked an unwired loader in
earlier rounds.
