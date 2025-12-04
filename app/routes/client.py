from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.database import get_db
from app.models.client import Client
from app.models.user import User
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from passlib.context import CryptContext
from typing import List

router = APIRouter(prefix="/clients", tags=["Clients"])

# Configuración para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Endpoint: crear un nuevo cliente
@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(client: ClientCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si el username ya existe
    result = await db.execute(select(User).where(User.username == client.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Verificar si el email ya existe
    result = await db.execute(select(User).where(User.email == client.email))
    existing_email = result.scalar_one_or_none()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Verificar si el teléfono ya existe (si se proporciona)
    if client.phone:
        result = await db.execute(select(User).where(User.phone == client.phone))
        existing_phone = result.scalar_one_or_none()
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone already registered"
            )
    
    try:
        # Crear el usuario base (que será el cliente)
        hashed_password = get_password_hash(client.password)
        db_user = User(
            username=client.username,
            email=client.email,
            full_name=client.full_name,
            phone=client.phone,
            hashed_password=hashed_password,
            is_active=1
        )
        
        db.add(db_user)
        await db.flush()  # Para obtener el ID sin hacer commit
        
        # Crear el cliente (que hereda de User)
        db_client = Client(id_client=db_user.id)
        db.add(db_client)
        await db.commit()
        await db.refresh(db_user)
        await db.refresh(db_client)
        
        return ClientResponse(
            id_client=db_client.id_client,
            username=db_user.username,
            email=db_user.email,
            full_name=db_user.full_name,
            phone=db_user.phone,
            is_active=db_user.is_active
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating client: {str(e)}"
        )

# Endpoint: obtener todos los clientes
@router.get("/", response_model=List[ClientResponse])
async def get_clients(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Como Client hereda de User, podemos hacer join directamente
    # o simplemente seleccionar Client que ya incluye los datos de User
    result = await db.execute(
        select(Client, User)
        .join(User, Client.id_client == User.id)
        .where(User.is_active == 1)  # Solo clientes activos
        .offset(skip)
        .limit(limit)
    )
    clients_data = result.all()
    
    return [
        ClientResponse(
            id_client=client.id_client,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            phone=user.phone,
            is_active=user.is_active
        )
        for client, user in clients_data
    ]

# Endpoint: obtener un cliente por ID
@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(client_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Client, User)
        .join(User, Client.id_client == User.id)
        .where(and_(Client.id_client == client_id, User.is_active == 1))  # Solo si está activo
    )
    client_data = result.first()
    
    if not client_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    client, user = client_data
    return ClientResponse(
        id_client=client.id_client,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        is_active=user.is_active
    )

# Endpoint: actualizar un cliente
@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(client_id: int, client_update: ClientUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Client, User).join(User, Client.id_client == User.id).where(Client.id_client == client_id)
    )
    client_data = result.first()
    
    if not client_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    client, user = client_data
    
    # Actualizar campos si se proporcionan
    update_data = client_update.model_dump(exclude_unset=True)
    
    # Verificar si el username ya existe (si se está actualizando)
    # Excluir al usuario actual de la validación
    if "username" in update_data and update_data["username"] != user.username:
        result = await db.execute(
            select(User).where(and_(User.username == update_data["username"], User.id != user.id))
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
    
    # Verificar si el email ya existe (si se está actualizando)
    # Excluir al usuario actual de la validación
    if "email" in update_data and update_data["email"] != user.email:
        result = await db.execute(
            select(User).where(and_(User.email == update_data["email"], User.id != user.id))
        )
        existing_email = result.scalar_one_or_none()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Verificar si el phone ya existe (si se está actualizando)
    # Excluir al usuario actual de la validación
    if "phone" in update_data and update_data["phone"] is not None and update_data["phone"] != user.phone:
        result = await db.execute(
            select(User).where(and_(User.phone == update_data["phone"], User.id != user.id))
        )
        existing_phone = result.scalar_one_or_none()
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone already registered"
            )
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    # Actualizar solo los campos que existen en el modelo User
    user_fields = ["username", "email", "full_name", "phone", "hashed_password"]
    for field, value in update_data.items():
        if field in user_fields:
            setattr(user, field, value)
    
    try:
        await db.commit()
        await db.refresh(user)
        
        return ClientResponse(
            id_client=client.id_client,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            phone=user.phone,
            is_active=user.is_active
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating client: {str(e)}"
        )

# Endpoint: eliminar un cliente (soft delete)
@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(client_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Client, User)
        .join(User, Client.id_client == User.id)
        .where(Client.id_client == client_id)
    )
    client_data = result.first()
    
    if not client_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    client, user = client_data
    
    # Verificar si ya está inactivo
    if user.is_active == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client is already deleted"
        )
    
    try:
        user.is_active = 0  # Soft delete
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting client: {str(e)}"
        )
