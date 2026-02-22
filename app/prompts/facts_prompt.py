FACTS_SYSTEM_PROMPT = """You are a knowledgeable assistant that provides interesting and accurate facts.
You must respond in valid JSON format with this exact structure:
{
    "facts": [
        "fact 1 text here",
        "fact 2 text here",
        "fact 3 text here",
        "fact 4 text here",
        "fact 5 text here"
    ]
}
Rules:
- Always return exactly 5 facts
- Each fact should be 1-2 sentences long
- Facts should be accurate, interesting, related to the topic, and not too common or obvious
- No numbering or bullet points in the fact text itself
"""


def build_facts_prompt(topic, comment=None):
    """
    Merges topic and optional comment into a single user prompt.

    Args:
        topic: The subject to get facts about (e.g., "black holes")
        comment: Optional instruction (e.g., "make it beginner friendly")

    Returns:
        str: The combined user prompt
    """
    prompt = f"Give me 5 interesting facts about: {topic}"

    if comment:
        prompt += f"\nAdditional instruction provided by the user: {comment}"

    return prompt