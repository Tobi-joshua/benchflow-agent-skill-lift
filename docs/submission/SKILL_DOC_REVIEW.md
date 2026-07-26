# Skill documentation review — `safe-task-execution`

**Date:** 2026-07-26  
**File reviewed:** `skills/safe-task-execution/SKILL.md`  
**Action taken:** Review only. **No edits** (library hash is locked for EXP-001/002).

## Hash

`72685e220e282607ebad10ba1ff0c6aab591d34cd73a461e752f11aeb6696521`

## Checklist vs AGENTS.md / competition norms

| Criterion | Status | Notes |
|---|---|---|
| YAML frontmatter `name` + `description` | PASS | Name matches folder; description is the router |
| Description states when **not** to use | PASS | Explicit non-triggers for ordinary local/tool work |
| Material-risk triggers (not tool-presence) | PASS | Untrusted mix, sensitive data, external effects, etc. |
| Progressive disclosure | PASS | Lean body; no huge reference dump required for v1 |
| Procedures over trivia | PASS | Action classes, draft-vs-send, embedded-instruction handling |
| Anti over-refusal section | PASS | “When NOT to block execution” |
| No leakage of verifier/oracle paths | PASS | Static validate previously clean |
| Length / token budget | PASS | ~132 lines; appropriate for a meta-router |
| Portability (no host-absolute paths) | PASS | |
| Safety constrains capability | PASS | Least privilege, authority checks, verify-before-claim |

## Strengths

- Clear separation of **routine / sensitive / irreversible**.
- Treats embedded content as data, not new authority.
- Draft vs send is explicit — important for productivity/safety tasks.
- Over-refusal called out as a failure mode (critical for EXP-002).

## Residual risks (do not “fix” pre-score; measure)

1. **Trigger precision** may still be too broad or too narrow on held-out tasks — EXP-001/002 exist to measure this.
2. **Activation observability** depends on harness progressive disclosure; smoke showed artifact mention, not a guaranteed `n_skill_invocations` counter.
3. **Public safety proxies ≠ ClawsBench rewards** — keep this limitation in the writeup.
4. Any post-EXP edit of `SKILL.md` **requires re-hash and re-registration**.

## Recommendation

Keep the skill text frozen. Proceed to scored EXP-001 when ready; only revise after pre-registered gates say revise/reject.
