from fastapi import APIRouter, UploadFile, File, Depends

from controllers.upload_controller import UploadController
from middleware.role_middleware import require_patient

router = APIRouter(
    prefix="/upload",
    tags=["Image Upload"]
)


@router.post("/xray")
def upload_xray(

    file: UploadFile = File(...),

    current_user=Depends(require_patient)

):

    return UploadController.upload(
        file,
        current_user
    )

@router.get("/history")
def history(
    current_user=Depends(require_patient)
):
    return UploadController.history(current_user)
@router.delete("/{image_id}")

def delete_image(
    image_id: str,
    current_user=Depends(require_patient)
):
    return UploadController.delete(
        image_id,
        current_user
    )