from ..service.messaging import MessagingService


async def get_messaging_service() -> MessagingService:
    return MessagingService()
