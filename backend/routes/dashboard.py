from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/stats")
def get_dashboard_stats():
    return {
        "success": True,
        "data": {
            "total_uploads": 18,
            "total_predictions": 18,
            "last_prediction": "Pneumonia",
            "average_confidence": 91.26
        }
    }