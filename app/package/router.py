from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.package import Package
from app.models.user import User
from app.auth.security import get_current_user
from app.package.schemas import PackageCreate, PackageResponse
from app.tracking.service import TrackingService

router = APIRouter()


@router.post("/packages", response_model=PackageResponse, status_code=status.HTTP_201_CREATED)
def add_package(
    package: PackageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new package to track."""
    try:
        # Get initial tracking status
        status_data = TrackingService.track_package(
            package.carrier_code,
            package.tracking_number
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Create package
    new_package = Package(
        user_id=current_user.id,
        tracking_number=package.tracking_number,
        carrier_code=package.carrier_code,
        nickname=package.nickname,
        status_data=status_data
    )
    
    db.add(new_package)
    db.commit()
    db.refresh(new_package)
    
    return new_package


@router.get("/packages", response_model=List[PackageResponse])
def list_packages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all packages for the authenticated user."""
    packages = db.query(Package).filter(Package.user_id == current_user.id).all()
    return packages


@router.get("/packages/{package_id}/status", response_model=PackageResponse)
def get_package_status(
    package_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the latest status for a package."""
    package = db.query(Package).filter(
        Package.id == package_id,
        Package.user_id == current_user.id
    ).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    # Update status from carrier
    try:
        status_data = TrackingService.track_package(
            package.carrier_code,
            package.tracking_number
        )
        package.status_data = status_data
        db.commit()
        db.refresh(package)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return package
