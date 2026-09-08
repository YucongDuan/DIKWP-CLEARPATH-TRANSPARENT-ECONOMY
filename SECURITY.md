# Security Policy

ClearPath is a local decision-support reference implementation. It does not execute trades, payments, employment decisions, account changes, remote publication, or other external actions.

## Supported version

Version 1.0.x is the current supported reference line.

## Reporting

Report reproducible security issues through a private channel chosen by the repository owner. Do not include real financial, health, family, political, religious, or identity data in public issues.

## Boundaries

- The loopback API refuses non-loopback binding unless an explicit override is supplied.
- Runtime dependencies are zero.
- Input files remain local unless the operator moves them.
- The reference core does not authenticate users; production deployments must add authentication, authorization, encryption, retention, audit, and independent review.
- A hash chain detects later modification; it does not prove that the original input was true.
