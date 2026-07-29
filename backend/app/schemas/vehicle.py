from pydantic import BaseModel, ConfigDict, Field


class VehicleCreate(BaseModel):
    make: str = Field(min_length=1)
    model: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: float = Field(gt=0)
    quantity_in_stock: int = Field(ge=0)


class VehicleUpdate(BaseModel):
    make: str | None = Field(default=None, min_length=1)
    model: str | None = Field(default=None, min_length=1)
    category: str | None = Field(default=None, min_length=1)
    price: float | None = Field(default=None, gt=0)
    quantity_in_stock: int | None = Field(default=None, ge=0)


class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    make: str
    model: str
    category: str
    price: float
    quantity_in_stock: int
