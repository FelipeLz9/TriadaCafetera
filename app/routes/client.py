from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.controllers.clientController import ClientController
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo cliente
    
    - **username**: Nombre de usuario único
    - **email**: Email único del cliente
    - **full_name**: Nombre completo (opcional)
    - **phone**: Teléfono único (opcional)
    - **password**: Contraseña del cliente
    """
    controller = ClientController(db)
    return controller.create_client(client)

@router.get("/", response_model=List[ClientResponse])
def get_clients(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Obtener lista de clientes con paginación
    
    - **skip**: Número de clientes a saltar (para paginación)
    - **limit**: Número máximo de clientes a retornar
    """
    controller = ClientController(db)
    return controller.get_all_clients(skip=skip, limit=limit)

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    """
    Obtener un cliente específico por ID
    
    - **client_id**: ID del cliente a buscar
    """
    controller = ClientController(db)
    client = controller.get_client_by_id(client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    return client

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int, 
    client_update: ClientUpdate, 
    db: Session = Depends(get_db)
):
    """
    Actualizar un cliente existente
    
    - **client_id**: ID del cliente a actualizar
    - **client_update**: Datos del cliente a actualizar (campos opcionales)
    """
    controller = ClientController(db)
    return controller.update_client(client_id, client_update)

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un cliente (soft delete)
    
    - **client_id**: ID del cliente a eliminar
    """
    controller = ClientController(db)
    controller.delete_client(client_id)
    return None
