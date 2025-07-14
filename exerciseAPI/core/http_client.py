from contextlib import asynccontextmanager

import httpx

from exerciseAPI.core.config import settings

client = httpx.AsyncClient(base_url=settings.INTERNAL_SERVICE_URL)


@asynccontextmanager
async def get_http_client():
    """
    Context manager para el cliente HTTP. Se asegura de que el cliente
    se cierre correctamente al apagar la aplicación.
    """
    yield client
    await client.aclose()
