import json
import unittest

from hermes_workflow import build_agent_plan


class PlannerTests(unittest.TestCase):
    def test_build_agent_plan_normalizes_objective(self):
        plan = build_agent_plan("  triage new issues  ", backend="ollama")

        self.assertEqual(plan.objective, "triage new issues")
        self.assertEqual(plan.backend, "ollama")
        self.assertIn("Clarify the objective", plan.steps[0])

    def test_prompt_packet_is_openai_compatible(self):
        plan = build_agent_plan("draft release notes")
        messages = plan.prompt_packet.to_messages()

        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")
        self.assertIn("draft release notes", messages[1]["content"])

    def test_extra_context_is_included(self):
        plan = build_agent_plan(
            "review pull request",
            extra_context=["repo: ponzgpt/test-repo-hermes", "risk: low"],
        )

        self.assertIn("repo: ponzgpt/test-repo-hermes", plan.prompt_packet.user)
        self.assertIn("risk: low", plan.prompt_packet.user)

    def test_empty_objective_is_rejected(self):
        with self.assertRaises(ValueError):
            build_agent_plan("   ")

    def test_json_output_is_stable(self):
        plan = build_agent_plan("summarize issues")
        payload = json.loads(plan.to_json())

        self.assertEqual(payload["objective"], "summarize issues")
        self.assertIn("prompt_packet", payload)


if __name__ == "__main__":
    unittest.main()
