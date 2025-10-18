"""Image upload API endpoints."""
import logging
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_image_repository, get_storage_service
from app.application.interfaces.image_repository import IImageRepository
from app.application.interfaces.storage_service import IStorageService
from app.application.use_cases.upload_image import UploadImageUseCase
from app.schemas.image import ImageResponseDTO, ImageUploadResponseDTO
from app.domain.exceptions import ImageValidationError, StorageError


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/images", tags=["images"])


@router.post(
    "/upload",
    response_model=ImageUploadResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a card image",
    description="Upload an image file for OCR processing. Accepts JPG and PNG formats."
)
async def upload_image(
    file: UploadFile = File(..., description="Image file to upload"),
    db: Session = Depends(get_db),
    storage_service: IStorageService = Depends(get_storage_service)
) -> ImageUploadResponseDTO:
    """
    Upload a card image endpoint.
    
    This endpoint:
    1. Validates file type
    2. Saves file to storage
    3. Creates database record
    4. Returns upload confirmation
    
    Args:
        file: Uploaded file
        db: Database session (injected)
        storage_service: Storage service (injected)
        
    Returns:
        Upload response with image ID and status
        
    Raises:
        HTTPException: 400 for validation errors, 500 for server errors
    """
    logger.info(f"Receiving image upload: {file.filename}")
    
    try:
        # Get repository from database session
        image_repository = get_image_repository(db)
        
        # Instantiate use case with injected dependencies
        use_case = UploadImageUseCase(
            image_repository=image_repository,
            storage_service=storage_service
        )
        
        # Execute use case
        card_image = await use_case.execute(
            file_content=file.file,
            filename=file.filename,
            content_type=file.content_type
        )
        
        logger.info(f"Image uploaded successfully: ID={card_image.id}")
        
        return ImageUploadResponseDTO(
            image_id=card_image.id,
            status=card_image.status
        )
    
    except ImageValidationError as e:
        logger.warning(f"Image validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except StorageError as e:
        logger.error(f"Storage error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store image file"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error during upload: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get(
    "/{image_id}",
    response_model=ImageResponseDTO,
    summary="Get image details",
    description="Retrieve details of an uploaded image by ID"
)
async def get_image(
    image_id: int,
    db: Session = Depends(get_db)
) -> ImageResponseDTO:
    """
    Get image details by ID.
    
    Args:
        image_id: Image ID
        db: Database session (injected)
        
    Returns:
        Image details
        
    Raises:
        HTTPException: 404 if image not found
    """
    image_repository = get_image_repository(db)
    card_image = await image_repository.get_by_id(image_id)
    
    if not card_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with ID {image_id} not found"
        )
    
    return ImageResponseDTO.from_entity(card_image)
