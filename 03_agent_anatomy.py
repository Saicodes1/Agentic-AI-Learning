"""
03_agent_anatomy.py — DELIVERABLE: design your own agent's blueprint.

Every agent is made of four parts:
  1. GOAL    — what it's trying to accomplish
  2. TOOLS   — the actions it can take in the world
  3. MEMORY  — what it keeps track of across steps
  4. ACTIONS — the concrete step-by-step loop it runs to reach the goal

Fill in `my_agent` below with your own design. This one models the
agent we actually build in 04_agent_loop.py: a small math-solving agent
that must compute (23 * 7) + 19 using tools instead of "mental math".
"""

my_agent = {
    "name": "MathSolverAgent",

    "goal": (
        "Given an arithmetic expression like '(23 * 7) + 19', compute the "
        "exact correct value by breaking it into individual tool calls — "
        "never by guessing or doing the math 'in its head'."
    ),

    "tools": [
        {
            "name": "multiply",
            "description": "Multiply two numbers and return the exact result.",
            "args": ["a: float", "b: float"],
        },
        {
            "name": "add",
            "description": "Add two numbers and return the exact result.",
            "args": ["a: float", "b: float"],
        },
    ],

    "memory": {
        "goal_expression": "(23 * 7) + 19",
        "target_value": 180,
        "steps_taken": [],   # e.g. [{"tool": "multiply", "args": [23, 7], "result": 161}]
        "running_value": None,
    },

    "actions": [
        "1. OBSERVE  — read the goal expression and current memory of steps so far.",
        "2. REASON   — decide the single next arithmetic operation needed "
        "(respecting order of operations) and which tool + args that requires.",
        "3. ACT      — call that tool and record the result in memory.",
        "4. EVALUATE — check whether the running value now equals the "
        "target_value. If yes, stop and report the final answer. If no, "
        "loop back to OBSERVE with the updated memory.",
    ],
}


def print_blueprint(agent: dict):
    print(f"Agent: {agent['name']}")
    print(f"\nGOAL:\n  {agent['goal']}")

    print("\nTOOLS:")
    for tool in agent["tools"]:
        print(f"  - {tool['name']}({', '.join(tool['args'])}): {tool['description']}")

    print("\nMEMORY (initial state):")
    for key, value in agent["memory"].items():
        print(f"  - {key}: {value}")

    print("\nACTIONS (the loop):")
    for step in agent["actions"]:
        print(f"  {step}")


if __name__ == "__main__":
    print_blueprint(my_agent)
