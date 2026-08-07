from fastapi import APIRouter, Depends

from controllers.review_controller import ReviewController
from middleware.role_middleware import require_doctor
from controllers.review_detail_controller import ReviewDetailController
router = APIRouter(
    prefix="/review",
    tags=["Doctor Review"]
)


@router.get("/pending")
def pending(
    current_user=Depends(require_doctor)
):

    return ReviewController.get_pending()
@router.get("/{prediction_id}")
def prediction_details(
    prediction_id: str,
    current_user=Depends(require_doctor)
):

    return ReviewDetailController.get_prediction(
        prediction_id
    )