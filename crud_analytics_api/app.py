from fastapi import FastAPI

from crud_analytics_api.routers import sales

app = FastAPI()
app.include_router(sales.router)
