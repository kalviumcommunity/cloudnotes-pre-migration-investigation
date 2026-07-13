# CloudNotes Current Architecture

This document describes the current, pre-migration deployment of the
CloudNotes service. Review it carefully as part of your investigation.

## Deployment Topology

```text
        User
          |
          v
      Web VM        (serves the user interface, single instance)
          |
          v
   Application VM   (runs app.py, single instance)
          |
          v
    Database VM     (single database server)
```

## Component Notes

- **Web VM** — A single virtual machine terminates user traffic and
  serves the front end. There is no additional web instance behind it.
- **Application VM** — A single virtual machine runs the application
  process. All requests are handled here.
- **Database VM** — A single database server stores all application
  data. It is the sole source of truth for the system.

## Operational Characteristics

- Traffic flows directly from the user to the Web VM with no
  intermediate traffic distribution tier.
- Each tier is served by exactly one virtual machine.
- There is no automated copy of the database maintained on a schedule.
- Traffic between tiers and from the user is carried without transport
  encryption.
- Each virtual machine hosts a single tier of the stack.

## Review Task

Using the topology and notes above, evaluate this architecture and
complete `reports/migration-readiness.md`.
