# Geetorus — Agent Evaluation & Quality Feedback

## 1. Continuous Evaluation Architecture

Agent performance and reliability in Geetorus are measured systematically through automated regression test harnesses, benchmark tasks, and operator feedback loops.

```
+-----------------------------------------------------------------------------------+
|                           GEETORUS EVALUATION KERNEL                              |
+-----------------------------------------------------------------------------------+
|  1. Promptfoo Harness       | Prompt regression, refusal testing, token drift.    |
|  2. Workflow Runner Evals   | End-to-end task completion rates in sandboxes.      |
|  3. Operator Feedback Votes | Upvote/downvote scoring stored in feedback_votes.   |
|  4. Decision Training Ex.   | Approved vs rejected turns for policy fine-tuning.  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Evaluation Suites & Metrics

- **Promptfoo Smoke Tests (`evals/promptfoo`)**: Runs prompt evaluations validating schema compliance and tool-calling accuracy.
  ```bash
  pnpm evals:smoke
  ```
- **Runner Acceptance Evals (`tests/runner-acceptance`)**: Measures execution reliability across multiple cloud sandbox backends.
  ```bash
  pnpm test:runner-acceptance
  ```
- **Decision Training Ledger (`packages/db/src/schema/decision_training_examples.ts`)**: Collects real human approvals and rejections to train custom routing and planning models.
