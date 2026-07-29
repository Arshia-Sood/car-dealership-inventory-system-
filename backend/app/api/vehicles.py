from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.core.database import get_db
from app.crud.vehicle import (
    create_vehicle,
    delete_vehicle,
    get_all_vehicles,
    get_vehicle_by_id,
    update_vehicle,
)
from app.models.user import User
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_new_vehicle(
    vehicle_in: VehicleCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> VehicleResponse:
    return create_vehicle(db, vehicle_in)


@router.get("", response_model=list[VehicleResponse])
def list_vehicles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Sequence[VehicleResponse]:
    return get_all_vehicles(db)


@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_existing_vehicle(
    vehicle_id: int,
    vehicle_in: VehicleUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> VehicleResponse:
    vehicle = get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )
    return update_vehicle(db, vehicle, vehicle_in)


@router.delete("/{vehicle_id}", status_code=status.HTTP_200_OK)
def delete_existing_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> dict:
    vehicle = get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )
    delete_vehicle(db, vehicle)
    return {"detail": "Vehicle deleted successfully"}
