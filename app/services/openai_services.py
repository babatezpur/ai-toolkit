import json
from openai import OpenAI
from flask import current_app

from app.errors.exceptions import OpenAIError


def get_client():
    """Create OpenAI client using API key from config."""
    return OpenAI(api_key=current_app.config['OPENAI_API_KEY'])


def call_openai(system_prompt, user_prompt):
    """
    Makes a call to OpenAI's API with JSON mode enabled - works for facts and quotes.

    Args:
        system_prompt: Instructions for the AI (e.g., "Return 5 facts as JSON")
        user_prompt: The user's actual input (e.g., "black holes, beginner friendly")

    Returns:
        dict: Parsed JSON response from OpenAI

    Raises:
        Exception: If API call fails or response isn't valid JSON
    """
    client = get_client()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        # Parse the JSON string from OpenAI's response
        result = json.loads(response.choices[0].message.content)
        return result

    except json.JSONDecodeError:
        raise OpenAIError("OpenAI returned invalid JSON")
    except Exception as e:
        raise OpenAIError(str(e))


def call_openai_conversation(messages):
    """
    Makes a call to OpenAI with full conversation history.
    Used for Q&A feature where context from previous messages matters.

    Args:
        messages: List of message dicts with 'role' and 'content'
                  e.g., [{"role": "system", "content": "..."},
                         {"role": "user", "content": "..."},
                         {"role": "assistant", "content": "..."},
                         {"role": "user", "content": "..."}]

    Returns:
        str: The assistant's reply as plain text
    """
    client = get_client()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        raise OpenAIError(str(e))