from guided_chatbot import build_bot, reply

engine = build_bot()
assert "it_help.txt" in reply(engine, "How do I reset my password?")
assert "fee_policy.txt" in reply(
    engine, "Can I get a tuition fee refund after week two?"
)
assert "network_guide.txt" in reply(
    engine, "How do I connect to campus Wi-Fi?"
)
assert reply(engine, "") == "Please enter a question."
assert "No matching FAQ" in reply(engine, "volcano geology")
assert "Possible matches" in reply(engine, "password recovery")
print("FAQ behaviour checks passed")
