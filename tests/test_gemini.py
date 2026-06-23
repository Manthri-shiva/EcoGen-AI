from chatbot.sustainability_advisor import get_gemini_response

try:
    response = get_gemini_response("Say hello in one sentence.")
    print("\nGEMINI RESPONSE:\n")
    print(response)

except Exception as e:
    print(f"\nERROR:\n{e}")