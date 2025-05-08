import uvicorn
from config import settings

uvicorn.run(
    "server:app",
    host=settings.SERVER_HOST,
    port=settings.SERVER_PORT,
    reload=True,
)
