# index_match

## Description

Two-way INDEX/MATCH lookup, more robust than VLOOKUP

## Parameters

```json
{
  "example": "=INDEX(C2:C100, MATCH(\"Apr\", A2:A100, 0))",
  "pattern": "=INDEX({return_range},MATCH({lookup_value},{lookup_range},0))",
  "result_format": null
}
```