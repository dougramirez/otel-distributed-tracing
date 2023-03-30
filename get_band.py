import json
import secrets

import httpx

version = "00"
trace_id = secrets.token_hex(16)
span_id = secrets.token_hex(8)
trace_flags = "01"
headers = {"traceparent": f"{version}-{trace_id}-{span_id}-{trace_flags}"}

with httpx.Client() as client:
    band = client.get(
        f"http://127.0.0.1:8000/bands/553be815-76f3-49db-b9d7-caca4b23cc3e",
        timeout=30.0,
        headers=headers,
    )

print(json.dumps(band.json(), indent=4))
print(f"http://localhost:16686/trace/{trace_id}")
