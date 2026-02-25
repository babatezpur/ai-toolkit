from flask import Blueprint, request, jsonify
from app import db
from app.middlewares.auth import auth_required
from app.schemas.request_schemas import topic_request_schema
from app.services.openai_services import call_openai
from app.services.rate_limiter import (
    check_rate_limit,
    increment_request_count,
    DAILY_LIMIT,
)
from app.prompts.quotes_prompt import QUOTES_SYSTEM_PROMPT, build_quotes_prompt
from app.models.searched_item import SearchedItem
from app.errors.exceptions import RateLimitError, OpenAIError


quotes_bp = Blueprint('quotes', __name__, url_prefix='/quotes')

@quotes_bp.route('/', methods=['POST'])
@auth_required
def get_quotes(current_user):
    # 1. Validate request body
    data = topic_request_schema.load(request.get_json())

    # 2. Check rate limit
    allowed, remaining = check_rate_limit(current_user)
    if not allowed:
        raise RateLimitError('Daily request limit reached')

    # 3. Build prompt and call OpenAI
    topic = data['topic']
    comment = data.get('comment')
    user_prompt = build_quotes_prompt(topic, comment)

    try:
        result = call_openai(QUOTES_SYSTEM_PROMPT, user_prompt)
    except Exception as e:
        raise OpenAIError(str(e))

    # 4. Increment request count (only after successful call)
    increment_request_count(current_user)

    # 5. Save search to database
    searched_item = SearchedItem(
        user_id=current_user.id,
        topic=topic.lower().strip(),
        feature='quotes',
    )
    db.session.add(searched_item)
    db.session.commit()

    # 6. Return response
    return jsonify({
        'message': 'Quotes retrieved successfully',
        'quotes': result.get('quotes', []),
        'remaining_requests': DAILY_LIMIT - current_user.daily_request_count
    }), 200