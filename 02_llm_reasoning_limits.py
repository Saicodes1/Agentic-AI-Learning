"""
02_llm_reasoning_limits.py — shows two LLM limits agents exist to fix:

1. Hallucination: confidently making up facts it doesn't actually know.
2. Reasoning drift: getting lost in a multi-step problem it tries to
   solve purely "in its head" instead of using a tool.
"""

from llm_client import get_client, chat, SetupError


def show_hallucination():
    print("=== 1. HALLUCINATION ===")
    client, model = get_client()
    # A specific, obscure, made-up-sounding request invites the model to
    # confidently fabricate details rather than say "I don't know".
    prompt = "What was the exact attendance figure at the 1994 BITS Pilani Dubai Robotics Fair opening ceremony?"
    reply = chat(client, model, prompt)
    print(f"Prompt: {prompt}")
    print(f"LLM answer: {reply}")
    print("-> There was no such event with a recorded 'attendance figure' — "
          "any specific number here is invented, not retrieved.\n")


# ---------------------------------------------------------------------
# TODO: Implement show_reasoning_drift
# Ask the LLM to solve a multi-step arithmetic problem WITHOUT a tool
# (pure mental math), then compare it against the real answer computed
# in Python. This demonstrates reasoning drift on longer chains.
# ---------------------------------------------------------------------
def show_reasoning_drift():
    print("=== 2. REASONING DRIFT ===")
    client, model = get_client()

    # A longer chain is more likely to trip up pure "in your head" reasoning
    # than the Week-1 goal problem, so the drift is easier to observe.
    a, b, c, d = 47, 83, 19, 6
    true_answer = ((a * b) - c) // d  # Python is always correct here

    prompt = (
        f"Without using a calculator or writing code, solve this in your head "
        f"and give me ONLY the final number: (({a} * {b}) - {c}) // {d}"
    )
    reply = chat(client, model, prompt)

    print(f"Prompt: {prompt}")
    print(f"LLM answer: {reply}")
    print(f"True answer (computed in Python): {true_answer}")

    if str(true_answer) in reply:
        print("-> The LLM happened to get this one right, but it was still "
              "guessing/estimating rather than reliably computing — a tool "
              "call would guarantee correctness every time.\n")
    else:
        print("-> Reasoning drift: the LLM's mental-math answer diverged from "
              "the true answer. This is exactly why agents hand arithmetic "
              "off to a tool instead of trusting the model's 'head math'.\n")


def main():
    try:
        show_hallucination()
    except SetupError as e:
        print(f"[Skipped hallucination demo — {e}]\n")

    try:
        show_reasoning_drift()
    except SetupError as e:
        print(f"[Skipped reasoning drift demo — {e}]\n")


if __name__ == "__main__":
    main()
