from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.controllers.estateController import EstateController
from app.schemas.estate import EstateCreate, EstateUpdate, EstateResponse

router = APIRouter(prefix="/estates", tags=["estates"])

@router.post("/", response_model=EstateResponse, status_code=status.HTTP_201_CREATED)
def create_estate(estate_data: EstateCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva finca
    
    - **name**: Nombre único de la finca
    - **location**: Ubicación de la finca
    - **size**: Tamaño en hectáreas (debe ser mayor a 0)
    - **price**: Precio de la finca (debe ser mayor a 0)
    - **owner_id**: ID del propietario (usuario)
    """
    controller = EstateController(db)
    return controller.create_estate(estate_data)

@router.get("/", response_model=List[EstateResponse])
def get_estates(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros"),
    owner_id: Optional[int] = Query(None, description="Filtrar por ID del propietario"),
    min_price: Optional[int] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[int] = Query(None, ge=0, description="Precio máximo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de fincas con paginación y filtros opcionales
    
    Filtros disponibles:
    - **owner_id**: Mostrar solo fincas de un propietario específico
    - **min_price**: Precio mínimo
    - **max_price**: Precio máximo
    """
    controller = EstateController(db)
    return controller.get_all_estates(
        skip=skip,
        limit=limit,
        owner_id=owner_id,
        min_price=min_price,
        max_price=max_price
    )

@router.get("/{estate_id}", response_model=EstateResponse)
def get_estate(estate_id: int, db: Session = Depends(get_db)):
    """
    Obtener una finca específica por ID
    
    - **estate_id**: ID de la finca a buscar
    """
    controller = EstateController(db)
    estate = controller.get_estate_by_id(estate_id)
    if not estate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Finca no encontrada"
        )
    return estate

@router.put("/{estate_id}", response_model=EstateResponse)
def update_estate(
    estate_id: int,
    estate_data: EstateUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una finca existente
    
    - **estate_id**: ID de la finca a actualizar
    - **estate_data**: Datos de la finca a actualizar (campos opcionales)
    
    Solo se actualizarán los campos que se envíen en el request.
    """
    controller = EstateController(db)
    return controller.update_estate(estate_id, estate_data)

@router.delete("/{estate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_estate(estate_id: int, db: Session = Depends(get_db)):
    """
    Eliminar una finca
    
    - **estate_id**: ID de la finca a eliminar
    """
    controller = EstateController(db)
    controller.delete_estate(estate_id)
    return None

@router.get("/owner/{owner_id}", response_model=List[EstateResponse])
def get_estates_by_owner(owner_id: int, db: Session = Depends(get_db)):
    """
    Obtener todas las fincas de un propietario específico
    
    - **owner_id**: ID del propietario
    """
    controller = EstateController(db)
    return controller.get_estates_by_owner(owner_id)

