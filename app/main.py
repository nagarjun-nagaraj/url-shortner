from fastapi import FastAPI
from app.routers import urls
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")

app.include_router(urls.router)