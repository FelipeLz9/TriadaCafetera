from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.estate import Estate
from app.models.service import Service
from app.schemas.estate import EstateCreate, EstateUpdate, EstateResponse, ServiceResponse
from typing import List

router = APIRouter(prefix="/estate", tags=["Estate"])

# GET estate/ - Obtener todas las fincas
@router.get("/", response_model=List[EstateResponse])
async def get_estates(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Estate).offset(skip).limit(limit)
    )
    estates = result.scalars().all()
    return estates

# GET estate/{estate_id} - Obtener una finca por ID
@router.get("/{estate_id}", response_model=EstateResponse)
async def get_estate(estate_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Estate).where(Estate.id == estate_id))
    estate = result.scalar_one_or_none()
    
    if not estate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estate not found"
        )
    
    return estate

# POST estate/ - Crear una nueva finca
@router.post("/", response_model=EstateResponse, status_code=status.HTTP_201_CREATED)
async def create_estate(estate: EstateCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si el nombre ya existe
    result = await db.execute(select(Estate).where(Estate.name == estate.name))
    existing_estate = result.scalar_one_or_none()
    if existing_estate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Estate name already exists"
        )
    
    db_estate = Estate(
        name=estate.name,
        location=estate.location,
        size=estate.size,
        price=estate.price,
        owner_id=estate.owner_id
    )
    
    db.add(db_estate)
    await db.commit()
    await db.refresh(db_estate)
    
    return db_estate

# PUT estate/{estate_id} - Actualizar una finca
@router.put("/{estate_id}", response_model=EstateResponse)
async def update_estate(estate_id: int, estate_update: EstateUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Estate).where(Estate.id == estate_id))
    estate = result.scalar_one_or_none()
    
    if not estate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estate not found"
        )
    
    # Actualizar campos si se proporcionan
    update_data = estate_update.dict(exclude_unset=True)
    
    # Verificar si el nuevo nombre ya existe (si se está actualizando)
    if "name" in update_data and update_data["name"] != estate.name:
        result = await db.execute(select(Estate).where(Estate.name == update_data["name"]))
        existing_estate = result.scalar_one_or_none()
        if existing_estate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estate name already exists"
            )
    
    for field, value in update_data.items():
        setattr(estate, field, value)
    
    await db.commit()
    await db.refresh(estate)
    
    return estate

# DELETE estate/{estate_id} - Eliminar una finca
@router.delete("/{estate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_estate(estate_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Estate).where(Estate.id == estate_id))
    estate = result.scalar_one_or_none()
    
    if not estate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estate not found"
        )
    
    await db.delete(estate)
    await db.commit()

# GET estate/{estate_id}/service - Obtener servicios de una finca
@router.get("/{estate_id}/service", response_model=List[ServiceResponse])
async def get_estate_services(estate_id: int, db: AsyncSession = Depends(get_db)):
    # Verificar que la finca existe
    result = await db.execute(select(Estate).where(Estate.id == estate_id))
    estate = result.scalar_one_or_none()
    
    if not estate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estate not found"
        )
    
    # Obtener servicios de la finca
    result = await db.execute(select(Service).where(Service.estate_id == estate_id))
    services = result.scalars().all()
    
    return services
