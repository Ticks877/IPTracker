# Consent-based Link Diagnostic

`link_diagnostic.py` is a small HTTP server for network testing on infrastructure you control.

## What it records

For each request it prints:

- Timestamp
- Source IP address
- User-Agent

The web page clearly tells the visitor that basic connection information is recorded for the diagnostic test.

## Run

```bash
python3 link_diagnostic.py
```

It defaults to `127.0.0.1:8080` so it is local-only until you deliberately configure a server you control.

**Do not use this component as a disguised tracking link or to collect another person's network information without their knowledge.**
