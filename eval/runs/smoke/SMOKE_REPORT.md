# Smoke Test Report — Unscored Control/Treatment Pair

**Final decision: PASS**

The authenticated local smoke test completed successfully for both the no-skill control and the with-skill treatment. The complete BenchFlow execution pipeline was reached, including Docker sandbox startup, Claude agent execution, verifier execution, reward extraction, and trial-result recording.

This smoke test was unscored and was performed only to validate the execution and measurement infrastructure. Its results must not be interpreted as evidence of general skill lift.

**Branch:** `cursor/safe-task-execution-skill-a21e`
**Library hash:** `72685e220e282607ebad10ba1ff0c6aab591d34cd73a461e752f11aeb6696521`
**SkillsBench commit:** `9a1f4dd5f7659f75707435da3ce854b6e48321d1`
**Python / BenchFlow:** Python 3.12 / BenchFlow 0.6.3
**Agent / model:** `claude-agent-acp` / `claude-sonnet-4-6`
**Selected task:** `citation-check`
**Scored experiment impact:** None — EXP-001 and EXP-002 were not executed or modified.

---

## Summary

| Check                         | Control              | Treatment                        |
| ----------------------------- | -------------------- | -------------------------------- |
| Condition                     | Baseline             | With skill                       |
| Skill mode                    | `no-skill`           | `with-skill`                     |
| Skill source                  | `none`               | `custom_runtime`                 |
| Skills directory              | None                 | Repository `skills/` directory   |
| Docker sandbox                | Started successfully | Started successfully             |
| Agent execution               | Completed            | Completed                        |
| Token data                    | Present              | Present                          |
| Infrastructure error          | None                 | None                             |
| Verifier executed             | Yes                  | Yes                              |
| Reward extracted              | `0.0`                | `1.0`                            |
| `safe-task-execution` present | No                   | Mentioned in treatment artifacts |
| Trial health                  | Healthy              | Healthy                          |

The control task received a verifier reward of `0.0`, while the treatment task received a reward of `1.0`.

This single unscored task pair confirms that the pipeline can distinguish the baseline and treatment conditions. It does not establish that the skill consistently improves performance across tasks or repetitions.

---

## Attempt 1 — Authentication Failure

**Date:** 2026-07-26
**Classification:** Infrastructure / authentication failure
**Skill evaluation status:** Not reached

The initial smoke attempt failed before successful agent execution because the runner did not have an Anthropic API credential.

The recorded error was:

```text
ANTHROPIC_API_KEY required for model 'claude-sonnet-4-6' but not set.
Pass it explicitly, for example through --agent-env/agent_env,
or define it in .env.
```

### Attempt 1 results

| Item                              | Result             |
| --------------------------------- | ------------------ |
| Authentication                    | Failed             |
| Docker evaluation pipeline        | Not fully reached  |
| Agent execution                   | Not reached        |
| Verifier                          | Not executed       |
| Reward                            | Not available      |
| Skill effectiveness               | Not evaluated      |
| Failure type                      | `environment_auth` |
| Library modified                  | No                 |
| Scored experiment results written | No                 |

The failed result is preserved only as historical evidence that the authentication blocker was correctly identified.

One old result directory contains this authentication failure and must not be included as a successful smoke trial:

```text
citation-check__81ba3aa1
```

---

## Attempt 2 — Authenticated Local Rerun

**Date:** 2026-07-26
**Status:** Completed successfully

Anthropic authentication was supplied locally through the process environment. The API credential was not written into the repository, experiment configuration, Markdown files, JSON files, or committed environment files.

The same frozen task, agent, model, skill conditions, SkillsBench commit, and library hash were retained.

### Preflight checks

| Check                                    | Result |
| ---------------------------------------- | ------ |
| Correct project branch                   | PASS   |
| Library hash matches preregistered value | PASS   |
| SkillsBench pinned commit                | PASS   |
| Python 3.12 environment                  | PASS   |
| BenchFlow 0.6.3                          | PASS   |
| Docker available                         | PASS   |
| `claude-agent-acp` accepted              | PASS   |
| `claude-sonnet-4-6` accepted             | PASS   |
| Anthropic authentication present         | PASS   |
| Authentication accepted by harness       | PASS   |

---

## Control Run

The control condition ran without the custom skill library.

**Condition:** Baseline
**Skill mode:** `no-skill`
**Skill source:** `none`
**Task:** `citation-check`
**Reward:** `0.0`
**Infrastructure error:** None
**Token information:** Present
**Skill invocations:** `0`

Successful control result:

```text
eval/runs/smoke/jobs/control/citation-check/r1/
2026-07-26__20-57-17/
citation-check__1398f575/
```

The control result confirms that:

* the authenticated agent launched;
* the Docker sandbox started;
* the task executed;
* the verifier ran;
* a reward was extracted;
* no repository skill was mounted or activated.

A reward of `0.0` is a task-level outcome, not an infrastructure failure.

---

## Treatment Run

The treatment condition ran with the repository skill library mounted.

**Condition:** Treatment
**Skill mode:** `with-skill`
**Skill source:** `custom_runtime`
**Skills directory:** Repository `skills/` directory
**Task:** `citation-check`
**Reward:** `1.0`
**Infrastructure error:** None
**Token information:** Present
**Skill evidence:** `safe-task-execution` was mentioned in treatment artifacts

Successful treatment result:

```text
eval/runs/smoke/jobs/treatment/citation-check/r1/
2026-07-26__20-57-24/
citation-check__190a3859/
```

The treatment result confirms that:

* the authenticated agent launched;
* the Docker sandbox started;
* the custom skill directory was supplied;
* the treatment condition was distinguishable from the control;
* the agent completed execution;
* the verifier ran;
* a reward was extracted;
* the treatment artifacts contained evidence of `safe-task-execution`.

The treatment reward was `1.0`.

This result demonstrates pipeline functionality only. A single successful treatment run does not prove that the skill generalizes or causes positive lift across the broader benchmark.

---

## Smoke Verification Checklist

| #  | Requirement                                                           | Status |
| -- | --------------------------------------------------------------------- | ------ |
| 1  | Authentication accepted                                               | PASS   |
| 2  | Control job launched                                                  | PASS   |
| 3  | Treatment job launched                                                | PASS   |
| 4  | Both Docker sandboxes started                                         | PASS   |
| 5  | Agent connected and executed                                          | PASS   |
| 6  | Control used no custom skill                                          | PASS   |
| 7  | Treatment used the repository skill directory                         | PASS   |
| 8  | `safe-task-execution` appeared in treatment artifacts                 | PASS   |
| 9  | Verifier executed for both healthy runs                               | PASS   |
| 10 | Rewards were extractable                                              | PASS   |
| 11 | Token information was recorded                                        | PASS   |
| 12 | Infrastructure errors were absent from healthy runs                   | PASS   |
| 13 | Task failure and infrastructure failure remained distinguishable      | PASS   |
| 14 | Results were written only under the smoke-test path                   | PASS   |
| 15 | EXP-001 and EXP-002 remained untouched                                | PASS   |
| 16 | Library hash remained unchanged                                       | PASS   |
| 17 | No API credential was intentionally written into repository artifacts | PASS   |

---

## Trial Record

The latest smoke trial summary is stored at:

```text
eval/runs/smoke/trials.json
```

It records two healthy trials:

1. Baseline control:

   * reward `0.0`;
   * `skill_activated=false`;
   * no infrastructure error.

2. Treatment:

   * reward `1.0`;
   * repository skills mounted;
   * `safe-task-execution` mentioned in artifacts;
   * no infrastructure error.

The smoke trial is marked:

```json
{
  "scored": false,
  "smoke_decision": "PASS"
}
```

---

## Artifact Layout

```text
eval/runs/smoke/
├── SMOKE_REPORT.md
├── trials.json
└── jobs/
    ├── control/
    │   └── citation-check/
    │       └── r1/
    │           └── 2026-07-26__20-57-17/
    │               ├── citation-check__1398f575/
    │               └── citation-check__81ba3aa1/
    └── treatment/
        └── citation-check/
            └── r1/
                └── 2026-07-26__20-57-24/
                    └── citation-check__190a3859/
```

`citation-check__81ba3aa1` is the previous authentication-failure residue and is not counted as a healthy smoke trial.

No scored outputs were written under:

```text
eval/runs/exp-001/
eval/runs/exp-002/
```

---

## Interpretation

The smoke test establishes that the evaluation infrastructure works end to end.

It verifies that BenchFlow can:

* authenticate with the configured model provider;
* initialize the Claude ACP agent;
* launch task-specific Docker sandboxes;
* distinguish no-skill and with-skill conditions;
* make the repository skill library available to the treatment;
* execute the task and verifier;
* extract rewards and token information;
* record structured trial results.

The observed control-to-treatment difference was:

```text
Control reward:   0.0
Treatment reward: 1.0
Observed delta:  +1.0
```

This delta is not a scored result and must not be reported as validated skill lift. The sample contains only one task and one successful repetition per condition.

General conclusions require the preregistered multi-task, repeated EXP-001 and EXP-002 evaluations.

---

## Security Notes

The Anthropic credential was supplied through the local process environment and was removed after the runs using:

```bash
unset ANTHROPIC_API_KEY
```

The credential must never be committed to:

* `.env`;
* YAML configuration;
* JSON trial records;
* Markdown reports;
* shell scripts;
* Git history;
* Cursor chat;
* screenshots or public logs.

The API key should be rotated if it was ever exposed outside the private terminal environment.

---

## Final Decision

**PASS**

The authenticated control and treatment smoke runs completed through the full execution and measurement pipeline.

The previous authentication problem is resolved.

EXP-001 and EXP-002 are now technically unblocked, but they should be launched deliberately because they involve paid model execution and a much larger number of runs.

**Scored experiment status: GO only after an explicit cost and execution decision.**
