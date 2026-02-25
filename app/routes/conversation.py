from flask import Blueprint, request, jsonify
from app import db
from app.middlewares.auth import auth_required
from app.schemas.conversation_schema import (
    start_conversation_schema,
    send_message_schema,
    conversation_list_schema,
    conversation_detail_schema,
)
from app.services.openai_services import call_openai_conversation
from app.services.rate_limiter import (
    check_rate_limit,
    increment_request_count,
    DAILY_LIMIT,
)
from app.prompts.qa_prompt import QA_SYSTEM_PROMPT
from app.models.conversation import Conversation
from app.models.conversation_message import ConversationMessage
from app.errors.exceptions import (
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    OpenAIError,
)

conversation_bp = Blueprint('conversation', __name__, url_prefix='/conversation')

MAX_MESSAGES_PER_CONVERSATION = 5


@conversation_bp.route('/start', methods=['POST'])
@auth_required
def start_conversation(current_user):
    # 1. Validate request
    data = start_conversation_schema.load(request.get_json())

    # 2. Check rate limit
    allowed, remaining = check_rate_limit(current_user)
    if not allowed:
        raise RateLimitError('Daily request limit reached')

    # 3. Create conversation
    title = data['message'][:100]
    conversation = Conversation(user_id=current_user.id, title=title)
    db.session.add(conversation)
    db.session.commit()

    # 4. Save user message
    user_msg = ConversationMessage(
        conversation_id=conversation.id,
        role='user',
        content=data['message']
    )
    db.session.add(user_msg)
    db.session.commit()

    # 5. Build messages list and call OpenAI
    messages = [
        {"role": "system", "content": QA_SYSTEM_PROMPT},
        {"role": "user", "content": data['message']}
    ]

    try:
        reply = call_openai_conversation(messages)
    except Exception as e:
        # Wrap OpenAI / network errors in a consistent app error
        raise OpenAIError(str(e))

    # 6. Save assistant reply
    assistant_msg = ConversationMessage(
        conversation_id=conversation.id,
        role='assistant',
        content=reply
    )
    db.session.add(assistant_msg)
    db.session.commit()

    # 7. Increment rate limit
    increment_request_count(current_user)

    return jsonify({
        'conversation_id': conversation.id,
        'reply': reply,
        'messages_remaining': MAX_MESSAGES_PER_CONVERSATION - 1
    }), 201


@conversation_bp.route('/message', methods=['POST'])
@auth_required
def send_message(current_user):
    # 1. Validate request
    data = send_message_schema.load(request.get_json())

    # 2. Find conversation and verify ownership
    conversation = Conversation.query.get(data['conversation_id'])
    if not conversation:
        raise NotFoundError('Conversation not found')

    if conversation.user_id != current_user.id:
        raise ForbiddenError('Not your conversation')

    # 3. Check message limit (count only user messages)
    user_message_count = ConversationMessage.query.filter_by(
        conversation_id=conversation.id,
        role='user'
    ).count()

    if user_message_count >= MAX_MESSAGES_PER_CONVERSATION:
        raise BadRequestError('Conversation message limit reached')

    # 4. Check rate limit
    allowed, remaining = check_rate_limit(current_user)
    if not allowed:
        raise RateLimitError('Daily request limit reached')

    # 5. Save user message
    user_msg = ConversationMessage(
        conversation_id=conversation.id,
        role='user',
        content=data['message']
    )
    db.session.add(user_msg)
    db.session.commit()

    # 6. Build full message history for OpenAI
    messages = [{"role": "system", "content": QA_SYSTEM_PROMPT}]
    for msg in conversation.messages:
        messages.append({"role": msg.role, "content": msg.content})

    try:
        reply = call_openai_conversation(messages)
    except Exception as e:
        raise OpenAIError(str(e))

    # 7. Save assistant reply
    assistant_msg = ConversationMessage(
        conversation_id=conversation.id,
        role='assistant',
        content=reply
    )
    db.session.add(assistant_msg)
    db.session.commit()

    # 8. Increment rate limit
    increment_request_count(current_user)

    return jsonify({
        'conversation_id': conversation.id,
        'reply': reply,
        'messages_remaining': MAX_MESSAGES_PER_CONVERSATION - (user_message_count + 1)
    }), 200


@conversation_bp.route('/conversations', methods=['GET'])
@auth_required
def list_conversations(current_user):
    conversations = Conversation.query.filter_by(
        user_id=current_user.id
    ).order_by(Conversation.created_at.desc()).all()

    return jsonify({
        'conversations': conversation_list_schema.dump(conversations)
    }), 200


@conversation_bp.route('/conversations/<int:conversation_id>', methods=['GET'])
@auth_required
def get_conversation(current_user, conversation_id):
    conversation = Conversation.query.get(conversation_id)

    if not conversation:
        raise NotFoundError('Conversation not found')

    if conversation.user_id != current_user.id:
        raise ForbiddenError('Not your conversation')

    return jsonify({
        'conversation': conversation_detail_schema.dump(conversation)
    }), 200