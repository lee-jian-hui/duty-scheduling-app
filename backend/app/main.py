from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import config
import uvicorn

from .core.routers import staff_router, schedule_router, statistics_router


def create_app() -> FastAPI:
    app = FastAPI(title="Duty Personnel Management API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[config.DEV_FRONTEND_ORIGIN, config.PROD_FRONTEND_ORIGIN],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(staff_router)
    app.include_router(schedule_router)
    app.include_router(statistics_router)
        
    @app.get("/health")
    def health() -> dict:
        return {"ok": True}

    @app.get("/")
    def health() -> dict:
        return {"ok": True}


    return app


app = create_app()
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
