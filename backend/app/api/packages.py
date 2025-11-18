from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from app.db.database import get_db
from app.models.user import User
from app.models.package import Package
from app.api.schemas import PackageCreate, PackageResponse, PackageUpdate, TrackingInfo, CarrierInfo
from app.api.deps import get_current_active_user
from app.strategies.factory import TrackingStrategyFactory

router = APIRouter()


@router.get("/carriers", response_model=CarrierInfo)
def get_supported_carriers():
    """Get list of supported carriers."""
    carriers = TrackingStrategyFactory.get_supported_carriers()
    return {"carriers": carriers}


@router.post("/", response_model=PackageResponse, status_code=status.HTTP_201_CREATED)
def create_package(
    package: PackageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Add a new package to track."""
    # Validate carrier is supported
    try:
        strategy = TrackingStrategyFactory.get_strategy(package.carrier)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Validate tracking number format
    if not strategy.validate_tracking_number(package.tracking_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid tracking number format for {package.carrier}"
        )
    
    # Create package
    db_package = Package(
        tracking_number=package.tracking_number,
        carrier=package.carrier.lower(),
        user_id=current_user.id,
        description=package.description
    )
    
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    
    return db_package


@router.get("/", response_model=List[PackageResponse])
def list_packages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """List all packages for the current user."""
    packages = db.query(Package).filter(
        Package.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return packages


@router.get("/{package_id}", response_model=PackageResponse)
def get_package(
    package_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific package."""
    package = db.query(Package).filter(
        Package.id == package_id,
        Package.user_id == current_user.id
    ).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    return package


@router.put("/{package_id}", response_model=PackageResponse)
def update_package(
    package_id: int,
    package_update: PackageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a package."""
    package = db.query(Package).filter(
        Package.id == package_id,
        Package.user_id == current_user.id
    ).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    if package_update.description is not None:
        package.description = package_update.description
    
    db.commit()
    db.refresh(package)
    
    return package


@router.delete("/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_package(
    package_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a package."""
    package = db.query(Package).filter(
        Package.id == package_id,
        Package.user_id == current_user.id
    ).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    db.delete(package)
    db.commit()
    
    return None


@router.get("/{package_id}/track", response_model=TrackingInfo)
def track_package(
    package_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get real-time tracking information for a package."""
    package = db.query(Package).filter(
        Package.id == package_id,
        Package.user_id == current_user.id
    ).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    # Get tracking strategy for the carrier
    try:
        strategy = TrackingStrategyFactory.get_strategy(package.carrier)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    # Track the package
    tracking_info = strategy.track(package.tracking_number)
    
    # Update package with latest info
    if tracking_info.get("error") is None:
        package.status = tracking_info.get("status")
        package.last_location = tracking_info.get("location")
        package.tracking_data = json.dumps(tracking_info)
        db.commit()
    
    return tracking_info
