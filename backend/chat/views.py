from rest_framework.response import Response
from rest_framework.views import APIView

from knowledge.ollama_client import chat as ollama_chat
from knowledge.retrieval import get_relevant_chunks

from .models import Conversation, Message
from .serializers import ChatRequestSerializer, ChatResponseSerializer

SYSTEM_PROMPT_TEMPLATE = """You are the portfolio assistant for {name}. Answer visitor \
questions about {name} using ONLY the context below. If the context doesn't contain the \
answer, say you don't have that information instead of guessing. Be concise and friendly.

Context:
{context}
"""

PORTFOLIO_OWNER_NAME = "Plamen"


class ChatView(APIView):
    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        session_id = data.get("session_id")
        conversation = (
            Conversation.objects.filter(session_id=session_id).first()
            if session_id
            else None
        )
        if conversation is None:
            conversation = Conversation.objects.create()

        user_message = data["message"]
        Message.objects.create(conversation=conversation, role=Message.Role.USER, content=user_message)

        relevant_chunks = get_relevant_chunks(user_message)
        context = "\n\n".join(
            f"[{chunk.document.title}] {chunk.text}" for chunk in relevant_chunks
        )
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(name=PORTFOLIO_OWNER_NAME, context=context)

        history = conversation.messages.order_by("created_at")
        messages = [{"role": "system", "content": system_prompt}] + [
            {"role": message.role, "content": message.content} for message in history
        ]

        reply = ollama_chat(messages)
        Message.objects.create(conversation=conversation, role=Message.Role.ASSISTANT, content=reply)

        sources = [
            {"title": chunk.document.title, "snippet": chunk.text[:200]}
            for chunk in relevant_chunks
        ]
        response = ChatResponseSerializer(
            {"session_id": conversation.session_id, "reply": reply, "sources": sources}
        )
        return Response(response.data)
