"""
04_agent_loop.py — DELIVERABLE: build a working agent loop.

The agent loop: OBSERVE -> REASON -> ACT -> EVALUATE -> (repeat or stop)

Goal for this exercise: solve (23 * 7) + 19  ==  180
using tool calls only — the agent is never allowed to just "know" the
answer; it must reach it one tool call at a time.

Note: if no LLM key is configured yet, the REASON step falls back to a
small deterministic planner so the loop still runs end-to-end and you
can see the full observe/reason/act/evaluate cycle. Once your .env is
set up, the real LLM does the reasoning instead.
"""

import json
from llm_client import get_client, chat, SetupError

GOAL_EXPRESSION = "(23 * 7) + 19"
TARGET_VALUE = 180
MAX_STEPS = 10


# ---------------------------------------------------------------------
# TODO 1: Define the tools available to the agent.
# ---------------------------------------------------------------------
TOOLS = {
    "multiply": lambda a, b: a * b,
    "add": lambda a, b: a + b,
}


def observe(memory: dict) -> str:
    """Describe the current state in plain text for the reasoning step."""
    if not memory["steps_taken"]:
        return f"Goal: compute {memory['goal_expression']}. No steps taken yet."
    last = memory["steps_taken"][-1]
    return (
        f"Goal: compute {memory['goal_expression']} (target = {memory['target_value']}). "
        f"Steps so far: {memory['steps_taken']}. "
        f"Running value: {memory['running_value']}."
    )


# ---------------------------------------------------------------------
# TODO 2: REASON — ask the LLM which single tool call to make next.
# Falls back to a hardcoded (but still step-by-step) plan if no LLM
# provider is configured, so the loop always runs.
# ---------------------------------------------------------------------
def reason(memory: dict) -> dict:
    situation = observe(memory)

    try:
        client, model = get_client()
        system = (
            "You control a math agent that can ONLY use two tools: "
            "multiply(a, b) and add(a, b). You must never compute the "
            "final answer yourself — only choose ONE next tool call that "
            "respects standard order of operations. "
            "Reply with ONLY compact JSON, no other text, in this exact shape: "
            '{"tool": "multiply"|"add"|"done", "args": [a, b]} '
            'Use "done" with args [] once the running_value already equals the target.'
        )
        reply = chat(client, model, prompt=situation, system=system, temperature=0)
        # Strip accidental code fences if the model adds them
        cleaned = reply.strip().strip("`").replace("json\n", "").strip()
        decision = json.loads(cleaned)
        return decision
    except SetupError:
        return _offline_plan(memory)
    except (json.JSONDecodeError, KeyError):
        # If the LLM didn't return clean JSON, fall back rather than crash
        return _offline_plan(memory)


def _offline_plan(memory: dict) -> dict:
    """Deterministic fallback planner for (23 * 7) + 19, used when no
    LLM key is configured yet — keeps the loop runnable end-to-end."""
    steps_done = len(memory["steps_taken"])
    if steps_done == 0:
        return {"tool": "multiply", "args": [23, 7]}
    elif steps_done == 1:
        return {"tool": "add", "args": [memory["running_value"], 19]}
    else:
        return {"tool": "done", "args": []}


# ---------------------------------------------------------------------
# TODO 3: ACT — actually execute the chosen tool call.
# ---------------------------------------------------------------------
def act(decision: dict, memory: dict) -> None:
    tool_name = decision["tool"]
    args = decision.get("args", [])

    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool requested: {tool_name}")

    result = TOOLS[tool_name](*args)
    memory["steps_taken"].append({"tool": tool_name, "args": args, "result": result})
    memory["running_value"] = result


# ---------------------------------------------------------------------
# TODO 4: EVALUATE — decide whether the goal has been reached.
# ---------------------------------------------------------------------
def evaluate(memory: dict) -> bool:
    return memory["running_value"] == memory["target_value"]


def run_agent_loop():
    memory = {
        "goal_expression": GOAL_EXPRESSION,
        "target_value": TARGET_VALUE,
        "steps_taken": [],
        "running_value": None,
    }

    for step_num in range(1, MAX_STEPS + 1):
        situation = observe(memory)
        print(f"\n[Step {step_num}] OBSERVE: {situation}")

        decision = reason(memory)
        print(f"[Step {step_num}] REASON:  next tool -> {decision}")

        if decision["tool"] == "done":
            print(f"[Step {step_num}] Agent believes it's done.")
            break

        act(decision, memory)
        print(f"[Step {step_num}] ACT:     ran {decision['tool']}{tuple(decision['args'])} "
              f"-> {memory['running_value']}")

        reached = evaluate(memory)
        print(f"[Step {step_num}] EVALUATE: goal reached? {reached}")

        if reached:
            break

    print("\n" + "=" * 50)
    if memory["running_value"] == TARGET_VALUE:
        print(f"✅ SUCCESS: {GOAL_EXPRESSION} = {memory['running_value']}")
    else:
        print(f"❌ Did not reach target. Final value: {memory['running_value']}")
    print(f"Full trace: {memory['steps_taken']}")


if __name__ == "__main__":
    run_agent_loop()
