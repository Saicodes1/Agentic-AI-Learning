"""
00_setup_check.py — run this first. It just verifies your environment and
makes one real LLM call. Nothing to fill in here.
"""

from llm_client import get_client, chat, SetupError


def main():
    print("Checking setup...")
    try:
        client, model = get_client()
        print(f"  -> Provider configured. Using model: {model}")
        reply = chat(client, model, "Say hello in exactly 5 words.")
        print(f"  -> LLM replied: {reply}")
        print("\n✅ Setup check PASSED — you're ready for Week 1.")
    except SetupError as e:
        print(f"\n❌ Setup check FAILED: {e}")
        print("   Check your .env file (copy .env.example -> .env and fill it in).")
    except Exception as e:
        print(f"\n❌ Setup check FAILED with an unexpected error: {e}")


if __name__ == "__main__":
    main()
