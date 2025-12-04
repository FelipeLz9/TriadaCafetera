from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.client import Client
from app.models.user import User
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from app.utils.auth import get_password_hash

class ClientController:
    def __init__(self, db: Session):
        self.db = db

    def create_client(self, client_data: ClientCreate) -> ClientResponse:
        """Crear un nuevo cliente"""
        try:
            # Verificar si el usuario ya existe
            result = self.db.execute(select(User).where(User.username == client_data.username))
            existing_user = result.scalar_one_or_none()
            if existing_user:
                # Verificar si ese User es un Client
                result_client = self.db.execute(select(Client).where(Client.id_client == existing_user.id))
                existing_client = result_client.scalar_one_or_none()
                if existing_client:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El nombre de usuario ya existe como cliente"
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El nombre de usuario ya existe"
                    )
            
            # Verificar si el email ya existe
            result = self.db.execute(select(User).where(User.email == client_data.email))
            existing_email = result.scalar_one_or_none()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )

            # Crear el cliente directamente (Client hereda de User, así que tiene todos los campos)
            hashed_password = get_password_hash(client_data.password)
            db_client = Client(
                username=client_data.username,
                email=client_data.email,
                full_name=client_data.full_name,
                phone=client_data.phone,
                hashed_password=hashed_password,
                is_active=True
            )
            
            self.db.add(db_client)
            self.db.commit()
            self.db.refresh(db_client)
            
            return ClientResponse(
                id_client=db_client.id_client,
                username=db_client.username,
                email=db_client.email,
                full_name=db_client.full_name,
                phone=db_client.phone,
                is_active=db_client.is_active
            )
            
        except IntegrityError as e:
            self.db.rollback()
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de integridad en la base de datos: {error_msg}"
            )

    def get_client_by_id(self, client_id: int) -> Optional[ClientResponse]:
        """Obtener cliente por ID"""
        result = self.db.execute(
            select(Client).where(Client.id_client == client_id)
        )
        client = result.scalar_one_or_none()
        
        if not client:
            return None
        
        return ClientResponse(
            id_client=client.id_client,
            username=client.username,
            email=client.email,
            full_name=client.full_name,
            phone=client.phone,
            is_active=client.is_active
        )

    def get_all_clients(self, skip: int = 0, limit: int = 100) -> List[ClientResponse]:
        """Obtener todos los clientes con paginación"""
        result = self.db.execute(
            select(Client).offset(skip).limit(limit)
        )
        clients = result.scalars().all()
        
        return [
            ClientResponse(
                id_client=client.id_client,
                username=client.username,
                email=client.email,
                full_name=client.full_name,
                phone=client.phone,
                is_active=client.is_active
            )
            for client in clients
        ]

    def update_client(self, client_id: int, client_data: ClientUpdate) -> Optional[ClientResponse]:
        """Actualizar cliente"""
        # Verificar si el cliente existe
        result = self.db.execute(
            select(Client).where(Client.id_client == client_id)
        )
        client = result.scalar_one_or_none()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        # Actualizar campos si se proporcionan
        update_data = client_data.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(client, field, value)
        
        self.db.commit()
        self.db.refresh(client)
        
        return ClientResponse(
            id_client=client.id_client,
            username=client.username,
            email=client.email,
            full_name=client.full_name,
            phone=client.phone,
            is_active=client.is_active
        )

    def delete_client(self, client_id: int) -> bool:
        """Eliminar cliente (soft delete - marcar como inactivo)"""
        result = self.db.execute(
            select(Client).where(Client.id_client == client_id)
        )
        client = result.scalar_one_or_none()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        # Soft delete - marcar como inactivo
        client.is_active = False
        self.db.commit()
        return True
