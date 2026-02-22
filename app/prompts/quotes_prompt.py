QUOTES_SYSTEM_PROMPT = """You are a knowledgeable assistant that provides meaningful and accurate quotes.
You must respond in valid JSON format with this exact structure:
{
    "quotes": [
        {
            "text": "the quote text here",
            "author": "Person's Name"
        },
        {
            "text": "another quote here",
            "author": "Another Person"
        }
    ]
}
Rules:
- Always return exactly 5 quotes
- Each quote must include the actual author (if present, otherwise use "Unknown")
- Quotes should be real and accurately attributed
- If a quote's author is truly unknown, use "Unknown"
- Do not make up fake attributions
"""


def build_quotes_prompt(topic, comment=None):
    """
    Merges topic and optional comment into a single user prompt.

    Args:
        topic: The subject to get quotes about (e.g., "perseverance")
        comment: Optional instruction (e.g., "from athletes only")

    Returns:
        str: The combined user prompt
    """
    prompt = f"Give me 5 meaningful quotes about: {topic}"

    if comment:
        prompt += f"\nAdditional instruction provided by the user: {comment}"

    return prompt