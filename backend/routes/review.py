from fastapi import APIRouter, Depends

from controllers.review_controller import ReviewController
from middleware.role_middleware import require_doctor
from controllers.review_detail_controller import ReviewDetailController
from schemas.review import ReviewRequest
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
@router.put("/{prediction_id}")
def review_prediction(

    prediction_id: str,

    review_data: ReviewRequest,

    current_user=Depends(require_doctor)

):

    return ReviewController.review_prediction(

        prediction_id,

        review_data,

        current_user

    )