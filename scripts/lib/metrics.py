"""Paired lift metrics for baseline vs treatment trials."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Any, Iterable, Literal


Condition = Literal["baseline", "treatment"]


@dataclass(frozen=True)
class Trial:
    task: str
    condition: Condition
    reward: float
    repeat: int = 1
    healthy: bool = True
    safety_violation: bool = False
    over_refusal: bool = False


@dataclass(frozen=True)
class PairedMetrics:
    n_tasks: int
    n_baseline_trials: int
    n_treatment_trials: int
    baseline_success_rate: float
    treatment_success_rate: float
    absolute_lift: float
    relative_improvement: float | None
    regression_rate: float
    safety_violation_rate_baseline: float
    safety_violation_rate_treatment: float
    over_refusal_rate_baseline: float
    over_refusal_rate_treatment: float
    reward_stddev_baseline: float | None
    reward_stddev_treatment: float | None
    per_task: list[dict[str, Any]]
    regressions: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "n_tasks": self.n_tasks,
            "n_baseline_trials": self.n_baseline_trials,
            "n_treatment_trials": self.n_treatment_trials,
            "baseline_success_rate": self.baseline_success_rate,
            "treatment_success_rate": self.treatment_success_rate,
            "absolute_lift": self.absolute_lift,
            "relative_improvement": self.relative_improvement,
            "regression_rate": self.regression_rate,
            "safety_violation_rate_baseline": self.safety_violation_rate_baseline,
            "safety_violation_rate_treatment": self.safety_violation_rate_treatment,
            "over_refusal_rate_baseline": self.over_refusal_rate_baseline,
            "over_refusal_rate_treatment": self.over_refusal_rate_treatment,
            "reward_stddev_baseline": self.reward_stddev_baseline,
            "reward_stddev_treatment": self.reward_stddev_treatment,
            "per_task": self.per_task,
            "regressions": self.regressions,
        }


def trials_from_records(records: Iterable[dict[str, Any]]) -> list[Trial]:
    trials: list[Trial] = []
    for row in records:
        condition = row["condition"]
        if condition not in {"baseline", "treatment"}:
            raise ValueError(f"invalid condition: {condition!r}")
        trials.append(
            Trial(
                task=str(row["task"]),
                condition=condition,  # type: ignore[arg-type]
                reward=float(row["reward"]),
                repeat=int(row.get("repeat", 1)),
                healthy=bool(row.get("healthy", True)),
                safety_violation=bool(row.get("safety_violation", False)),
                over_refusal=bool(row.get("over_refusal", False)),
            )
        )
    return trials


def compute_paired_metrics(
    trials: Iterable[Trial],
    *,
    success_threshold: float = 1.0,
    regression_tolerance: float = 0.0,
) -> PairedMetrics:
    """Compute protocol metrics from paired baseline/treatment trials."""
    healthy = [t for t in trials if t.healthy]
    by_task: dict[str, dict[str, list[Trial]]] = defaultdict(lambda: defaultdict(list))
    for trial in healthy:
        by_task[trial.task][trial.condition].append(trial)

    paired_tasks = sorted(
        task
        for task, conds in by_task.items()
        if conds.get("baseline") and conds.get("treatment")
    )
    if not paired_tasks:
        raise ValueError("no paired tasks with both baseline and treatment healthy trials")

    per_task: list[dict[str, Any]] = []
    regressions: list[dict[str, Any]] = []
    baseline_success_flags: list[float] = []
    treatment_success_flags: list[float] = []
    lifts: list[float] = []
    base_rewards_all: list[float] = []
    treat_rewards_all: list[float] = []
    base_viol = treat_viol = base_ref = treat_ref = 0
    base_n = treat_n = 0

    for task in paired_tasks:
        b_trials = by_task[task]["baseline"]
        t_trials = by_task[task]["treatment"]
        b_mean = mean(t.reward for t in b_trials)
        t_mean = mean(t.reward for t in t_trials)
        lift = t_mean - b_mean
        b_ok = 1.0 if b_mean >= success_threshold else 0.0
        t_ok = 1.0 if t_mean >= success_threshold else 0.0
        baseline_success_flags.append(b_ok)
        treatment_success_flags.append(t_ok)
        lifts.append(lift)
        base_rewards_all.extend(t.reward for t in b_trials)
        treat_rewards_all.extend(t.reward for t in t_trials)
        base_n += len(b_trials)
        treat_n += len(t_trials)
        base_viol += sum(1 for t in b_trials if t.safety_violation)
        treat_viol += sum(1 for t in t_trials if t.safety_violation)
        base_ref += sum(1 for t in b_trials if t.over_refusal)
        treat_ref += sum(1 for t in t_trials if t.over_refusal)

        row = {
            "task": task,
            "baseline_mean_reward": b_mean,
            "treatment_mean_reward": t_mean,
            "lift": lift,
            "baseline_success": bool(b_ok),
            "treatment_success": bool(t_ok),
            "n_baseline": len(b_trials),
            "n_treatment": len(t_trials),
        }
        per_task.append(row)
        if t_mean < b_mean - regression_tolerance:
            regressions.append(row)

    n = len(paired_tasks)
    b_rate = mean(baseline_success_flags)
    t_rate = mean(treatment_success_flags)
    abs_lift = mean(lifts)
    headroom = 1.0 - b_rate
    rel = ((t_rate - b_rate) / headroom) if headroom > 1e-12 else None

    return PairedMetrics(
        n_tasks=n,
        n_baseline_trials=base_n,
        n_treatment_trials=treat_n,
        baseline_success_rate=b_rate,
        treatment_success_rate=t_rate,
        absolute_lift=abs_lift,
        relative_improvement=rel,
        regression_rate=len(regressions) / n,
        safety_violation_rate_baseline=(base_viol / base_n) if base_n else 0.0,
        safety_violation_rate_treatment=(treat_viol / treat_n) if treat_n else 0.0,
        over_refusal_rate_baseline=(base_ref / base_n) if base_n else 0.0,
        over_refusal_rate_treatment=(treat_ref / treat_n) if treat_n else 0.0,
        reward_stddev_baseline=pstdev(base_rewards_all) if len(base_rewards_all) > 1 else None,
        reward_stddev_treatment=pstdev(treat_rewards_all) if len(treat_rewards_all) > 1 else None,
        per_task=per_task,
        regressions=regressions,
    )
