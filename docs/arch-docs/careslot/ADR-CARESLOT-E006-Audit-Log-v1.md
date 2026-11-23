Epic: E006 — Audit Log
Covers: US-014, FR-AUDIT-001

Every view or change of a patient's data is logged with who did it, which patient and when, and the log is kept for
5 years.

## ADR-CARESLOT-E006-001: Use an append-only AuditLog table written by the service layer, with 5-year retention
### Status
Proposed
### Type
Decision
### Context
BR-015 / FR-AUDIT-001 / NFR-SEC-004: the DPO wants to know who looked at patient data, kept for 5 years. How the DPO
reads the log is still open (PRD OQ 7).
### Options Considered
1. Web-server access logs only: they show URLs, not which patient, and are kept in CloudWatch, not with the data.
2. Database triggers: they see writes but not reads.
3. An `AuditLog` table written by the service functions that read or change patient data (patient record,
   appointment, day list, doctor list).
### Decision
Option 3. Each entry records actor, patient, action (`view`, `create`, `update`, `cancel`), object and timestamp. The
application's database role has INSERT and SELECT only on the table. A monthly scheduled job, running under a
separate role, deletes rows older than 5 years.
### Rationale
It captures reads as well as writes, at the place where the patient is known. With no UPDATE/DELETE for the app,
entries can't be altered by application code.
### Consequences
List views write one entry per patient shown. Volume was not estimated. An index on `(patient_id, at)` keeps
lookups fast. The DPO's read path (screen or export) is deferred (ARCH §9 Q7).
### Affected Epics
E002, E003, E004, E006
### Architecture Document Reference
ARCH-CARESLOT-v1 §4 "Audit log", §5 AuditLog, §8 NFR-SEC-004
