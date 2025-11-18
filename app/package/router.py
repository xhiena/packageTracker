from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.models.package import Package
from app.auth.security import get_current_user
from app.package.schemas import PackageCreate, PackageResponse, PackageStatusResponse
from app.tracking.service import tracking_service

router = APIRouter(prefix="/packages", tags=["packages"])

@router.post("", response_model=PackageResponse, status_code=status.HTTP_201_CREATED)
async def create_package(
    package_data: PackageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a new package for the authenticated user.
    
    - **tracking_number**: The tracking number from the carrier
    - **carrier_code**: The carrier code (e.g., CORREOS, GLS, SEUR)
    - **nickname**: Optional nickname for the package
    
    Calls the Tracking Service to get initial status and saves to database.
    """
    # Get initial tracking status from the carrier
    try:
        initial_status = tracking_service.get_status(
            package_data.carrier_code, 
            package_data.tracking_number
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch tracking information: {str(e)}"
        )
    
    # Create package in database
    db_package = Package(
        user_id=current_user.id,
        tracking_number=package_data.tracking_number,
        carrier_code=package_data.carrier_code.upper(),
        nickname=package_data.nickname,
        status_data=initial_status
    )
    
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    
    return db_package

@router.get("", response_model=List[PackageResponse])
async def list_packages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all packages for the authenticated user.
    
    Returns all packages that belong to the current user.
    """
    packages = db.query(Package).filter(Package.user_id == current_user.id).all()
    return packages

@router.get("/{package_id}/status", response_model=PackageStatusResponse)
async def get_package_status(
    package_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetch the latest status for a specific package.
    
    Calls the Tracking Service to check the external API and updates 
    the status_data in the database.
    """
    # Get package from database
    package = db.query(Package).filter(
        Package.id == package_id,
        Package.user_id == current_user.id
    ).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    # Fetch latest status from carrier
    try:
        current_status = tracking_service.get_status(
            package.carrier_code,
            package.tracking_number
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch tracking information: {str(e)}"
        )
    
    # Update status in database
    package.status_data = current_status
    db.commit()
    db.refresh(package)
    
    return {
        "package": package,
        "current_status": current_status
    }
