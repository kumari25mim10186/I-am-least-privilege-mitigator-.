# I-am-least-privilege-mitigator-.
# Ledger — Autonomous Cloud IAM Least-Privilege Mitigator

**Track 5: Cybersecurity — Problem Statement 10**
Submission for Code-X-Novas Innovathon 2026 / Agentic AI Hackathon

## Overview

Ledger is an autonomous agent that reduces excessive IAM permissions across cloud services **without breaking the workflows that depend on them**. Rather than trusting a static audit rule ("unused for 90 days = remove"), the agent simulates the impact of every proposed change, catches the cases where removal would break something, and revises its own policy until it satisfies both security and functionality constraints.

## Problem Statement

Over-permissioned IAM roles are one of the most common sources of cloud breach impact — a compromised service account often has far more access than it ever uses. Manually auditing and tightening these permissions is slow, error-prone, and risky: pull the wrong permission and you break production.

This project builds an agent that:
1. Inspects IAM role assignments and access history
2. Identifies candidate permissions for removal
3. Simulates the impact of proposed changes against service dependencies
4. Reasons over failures or dependency information when a simulation breaks
5. Revises the policy accordingly
6. Verifies the revised policy preserves required access

## Required Workflow Mapping

| Stage | What the agent does |
|---|---|
| **Goal** | Reduce IAM over-permissioning across all monitored services without breaking simulated dependencies |
| **Decision** | Parse 90-day access logs per role, flag permissions with zero invocations as removal candidates |
| **Action** | Deploy the proposed
