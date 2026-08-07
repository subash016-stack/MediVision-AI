from fastapi import APIRouter, Depends

from controllers.review_controller import ReviewController
from middleware.role_middleware import require_doctor

router = APIRouter(
    prefix="/review",
    tags=["Doctor Review"]
)


@router.get("/pending")
def pending(
    current_user=Depends(require_doctor)
):

    return ReviewController.get_pending()