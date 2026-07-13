# CloudNotes — Pre-Migration Investigation

## Module 1 · Cloud Engineering Practical Assessment

CloudNotes is a small internal service that the operations team is
preparing to migrate to the cloud. The service **does not currently
start**, its health check **does not currently pass**, and its
architecture **has not yet been reviewed**.

Your job is to investigate the repository, get the service running,
prove that it is healthy, and complete an architecture readiness review.

The repository is intentionally shipped in a broken state. Part of the
assessment is discovering *what* is broken and *why* on your own.

---

## Repository Layout

```text
cloudnotes-pre-migration-investigation/
├── app.py                  # Service entry point
├── health_server.py        # Standalone health probe helper
├── requirements.txt        # Dependencies (standard library only)
├── config/
│   └── production.conf      # Application configuration
├── logs/
│   └── service.log          # Existing service logs — start here
├── network/
│   ├── endpoint.conf        # Declared service endpoint
│   └── hosts.conf           # Known hosts
├── architecture/
│   └── cloudnotes-architecture.md   # Current architecture to review
├── reports/
│   └── migration-readiness.md       # Review template to complete
└── README.md
```

---

## Requirements

- Python 3 (standard library only)
- No Docker, no cloud accounts, no paid APIs
- Runs entirely offline

Install step (nothing external is required):

```bash
pip install -r requirements.txt
```

---

## Startup Commands

Attempt to start the service:

```bash
python3 app.py
```

If it does not start, investigate before continuing. The service reads
its configuration location from an environment variable. When you have
identified the correct configuration, provide it and start again:

```bash
export APP_CONFIG=<path-to-configuration-file>
python3 app.py
```

---

## Health Check Command

With the service running, verify it is healthy:

```bash
curl http://localhost:<port>/health
```

A healthy service responds with:

```json
{"status":"healthy"}
```

You may also use the bundled probe:

```bash
python3 health_server.py
```

---

## Investigation Instructions

Work through the following. Discover the specifics yourself — the
answers are **not** provided in this repository.

1. **Get the service to start.**
   - Run `app.py` and observe what happens.
   - Read `logs/service.log` carefully.
   - Determine what the service needs before it can boot, and supply it.

2. **Get the health check to pass.**
   - Compare what the service actually does when it runs against what
     the files under `network/` declare.
   - Reconcile any mismatch so that the health endpoint responds.

3. **Review the architecture.**
   - Read `architecture/cloudnotes-architecture.md`.
   - Complete every section of `reports/migration-readiness.md`:
     - Virtualization Consideration
     - Distributed Systems Risk
     - Cloud Responsibility Concern
     - Architecture Improvement

---

## Definition of Done

- `python3 app.py` starts the service without errors.
- `curl http://localhost:<port>/health` returns `{"status":"healthy"}`.
- `reports/migration-readiness.md` is fully completed.

Good luck — investigate methodically and document what you find.
