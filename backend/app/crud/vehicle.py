from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


def get_vehicle_by_id(db: Session, vehicle_id: int) -> Vehicle | None:
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()


def get_all_vehicles(db: Session) -> Sequence[Vehicle]:
    return db.query(Vehicle).all()


def create_vehicle(db: Session, vehicle_in: VehicleCreate) -> Vehicle:
    vehicle = Vehicle(
        make=vehicle_in.make,
        model=vehicle_in.model,
        category=vehicle_in.category,
        price=vehicle_in.price,
        quantity_in_stock=vehicle_in.quantity_in_stock,
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def update_vehicle(db: Session, vehicle: Vehicle, vehicle_in: VehicleUpdate) -> Vehicle:
    update_data = vehicle_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vehicle, field, value)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def delete_vehicle(db: Session, vehicle: Vehicle) -> None:
    db.delete(vehicle)
    db.commit()
