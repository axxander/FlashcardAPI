from fastapi import APIRouter
from app.api.routes import admin, authentication, flashcard, register, user

api_router = APIRouter()

api_router.include_router(
  	admin.router
)
api_router.include_router(
  	authentication.router,
)
api_router.include_router(
  	flashcard.router,
)
api_router.include_router(
  	register.router,
)
api_router.include_router(
  	user.router,
)

