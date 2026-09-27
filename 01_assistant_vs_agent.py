"""
01_assistant_vs_agent.py — an ASSISTANT can only talk. An AGENT can act
(call a tool, use its output, and act again). This file shows the
difference on the same question.
"""

from llm_client import get_client, chat, SetupError


# A tiny fake "tool" the agent has access to. A real tool might hit a
# weather API; here we just return canned data so the demo needs no
# extra API key.
def get_weather(city: str) -> str:
    fake_data = {
        "dubai": "41°C, clear skies, humidity 38%",
        "mumbai": "31°C, monsoon showers, humidity 88%",
        "london": "14°C, light rain, humidity 76%",
    }
    return fake_data.get(city.lower(), f"No data available for {city}")


# ---------------------------------------------------------------------
# TODO 1: Implement call_assistant
# An assistant only has words — it must answer from what it already
# "knows" (or admit it doesn't know). It cannot check anything live.
# ---------------------------------------------------------------------
def call_assistant(question: str) -> str:
    client, model = get_client()
    return chat(
        client,
        model,
        prompt=question,
        system=(
            "You are a plain assistant. You have no tools and no way to look "
            "anything up live. If asked about real-time data (like current "
            "weather), say clearly that you cannot know that right now."
        ),
    )


# ---------------------------------------------------------------------
# TODO 2: Implement call_agent
# An agent notices it needs live data, calls the get_weather tool, and
# uses the *real* tool output to answer — this is the "act" step an
# assistant cannot do.
# ---------------------------------------------------------------------
def call_agent(question: str, city: str) -> str:
    tool_result = get_weather(city)  # the agent ACTS by calling a tool

    client, model = get_client()
    return chat(
        client,
        model,
        prompt=f"Question: {question}\n\nLive tool result — get_weather({city!r}) = {tool_result!r}\n\n"
        f"Using the tool result above, answer the question.",
        system="You are an agent. You were just given real tool output — use it directly, don't guess.",
    )


def main():
    question = "What's the weather in Dubai right now?"

    print("=== ASSISTANT (words only) ===")
    try:
        print(call_assistant(question))
    except SetupError as e:
        print(f"[Skipped — {e}]")

    print("\n=== AGENT (uses a tool to act) ===")
    try:
        print(call_agent(question, city="Dubai"))
    except SetupError as e:
        print(f"[Skipped — {e}]")

    print(
        "\nNotice: the assistant can only speculate or refuse. The agent "
        "actually called get_weather() and grounded its answer in real data."
    )


if __name__ == "__main__":
    main()
