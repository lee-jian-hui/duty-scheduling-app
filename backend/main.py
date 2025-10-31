from fastapi import FastAPI

try:
    # Import routers if available
    from app.routers import staff_router, schedule_router, statistics_router
except Exception:  # pragma: no cover - allows skeleton import during early scaffolding
    staff_router = schedule_router = statistics_router = None  # type: ignore


def create_app() -> FastAPI:
    app = FastAPI(title="Duty Personnel Management API", version="0.1.0")

    if staff_router is not None:
        app.include_router(staff_router)
    if schedule_router is not None:
        app.include_router(schedule_router)
    if statistics_router is not None:
        app.include_router(statistics_router)
        
    @app.get("/")
    def root() -> dict:
        return {"ok": True}

    @app.get("/health")
    def health() -> dict:
        return {"ok": True}


    return app


app = create_app()
