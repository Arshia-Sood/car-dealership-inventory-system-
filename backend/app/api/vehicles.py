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
    purchase_vehicle,
    restock_vehicle,
    search_vehicles,
    update_vehicle,
)
from app.models.user import User
from app.schemas.vehicle import InventoryAction, VehicleCreate, VehicleResponse, VehicleUpdate

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


@router.get("/search", response_model=list[VehicleResponse])
def search_vehicles_endpoint(
    make: str | None = None,
    model: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Sequence[VehicleResponse]:
    return search_vehicles(db, make=make, model=model, category=category)


@router.post("/{vehicle_id}/purchase", response_model=VehicleResponse)
def purchase_existing_vehicle(
    vehicle_id: int,
    action: InventoryAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> VehicleResponse:
    vehicle = get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )
    if action.quantity > vehicle.quantity_in_stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Purchase quantity exceeds available stock",
        )
    return purchase_vehicle(db, vehicle, action.quantity)


@router.post("/{vehicle_id}/restock", response_model=VehicleResponse)
def restock_existing_vehicle(
    vehicle_id: int,
    action: InventoryAction,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> VehicleResponse:
    vehicle = get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )
    return restock_vehicle(db, vehicle, action.quantity)


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
