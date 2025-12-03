from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
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
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    result = db.execute(select(User).where(User.username == client.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    result = db.execute(select(User).where(User.email == client.email))
    existing_email = result.scalar_one_or_none()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Crear el usuario base
    hashed_password = get_password_hash(client.password)
    db_user = User(
        username=client.username,
        email=client.email,
        full_name=client.full_name,
        phone=client.phone,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Crear el cliente
    db_client = Client(id_client=db_user.id)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    
    return ClientResponse(
        id_client=db_client.id_client,
        username=db_user.username,
        email=db_user.email,
        full_name=db_user.full_name,
        phone=db_user.phone,
        is_active=db_user.is_active
    )

# Endpoint: obtener todos los clientes
@router.get("/", response_model=List[ClientResponse])
def get_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = db.execute(
        select(Client, User).join(User, Client.id_client == User.id).offset(skip).limit(limit)
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
def get_client(client_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        select(Client, User).join(User, Client.id_client == User.id).where(Client.id_client == client_id)
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
def update_client(client_id: int, client_update: ClientUpdate, db: Session = Depends(get_db)):
    result = db.execute(
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
    update_data = client_update.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return ClientResponse(
        id_client=client.id_client,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        is_active=user.is_active
    )

# Endpoint: eliminar un cliente (soft delete)
@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        select(Client, User).join(User, Client.id_client == User.id).where(Client.id_client == client_id)
    )
    client_data = result.first()
    
    if not client_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    client, user = client_data
    user.is_active = False  # Soft delete
    db.commit()
