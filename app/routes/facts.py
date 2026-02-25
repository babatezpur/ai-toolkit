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
from app.prompts.facts_prompt import FACTS_SYSTEM_PROMPT, build_facts_prompt
from app.models.searched_item import SearchedItem
from app.errors.exceptions import RateLimitError, OpenAIError

facts_bp = Blueprint('facts', __name__, url_prefix='/facts')

@facts_bp.route('/', methods=['POST'])
@auth_required
def get_facts(current_user):
    # 1. Validate request body
    data = topic_request_schema.load(request.get_json())

    # 2. Check rate limit
    allowed, remaining = check_rate_limit(current_user)
    if not allowed:
        raise RateLimitError('Daily request limit reached')

    # 3. Build prompt and call OpenAI
    topic = data['topic']
    comment = data.get('comment')
    user_prompt = build_facts_prompt(topic, comment)

    try:
        result = call_openai(FACTS_SYSTEM_PROMPT, user_prompt)
    except Exception as e:
        raise OpenAIError(str(e))

    # 4. Increment request count (only after successful call)
    increment_request_count(current_user)

    # 5. Save search to database
    searched_item = SearchedItem(
        user_id=current_user.id,
        topic=topic.lower().strip(),
        feature='facts',
    )
    db.session.add(searched_item)
    db.session.commit()

    # 6. Return response
    return jsonify({
        'message': 'Facts retrieved successfully',
        'facts': result.get('facts', []),
        'remaining_requests': DAILY_LIMIT - current_user.daily_request_count
    }), 200