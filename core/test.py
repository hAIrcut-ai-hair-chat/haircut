from .services import HuggingFaceChatService

ai_chat_service = HuggingFaceChatService()

response = ai_chat_service.ask(input="Oi, tudo bem")
print(response)