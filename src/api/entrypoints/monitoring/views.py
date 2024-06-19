from fastapi import APIRouter

router = APIRouter()


@router.get("/health-check", status_code=200, tags=["Monitoring"])
async def health_check() -> dict:
    """
    Checks the health of the project.

    It returns 200 if the project is healthy.
    """
    return {"status": "alive"}
