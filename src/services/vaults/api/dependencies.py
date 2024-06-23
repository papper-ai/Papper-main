from ..service.vaults import VaultsService


async def get_vaults_service() -> VaultsService:
    return VaultsService()
