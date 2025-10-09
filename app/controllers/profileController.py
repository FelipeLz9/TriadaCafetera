from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.profile import Profile
from models.user import User
from schemas.profile_schema import ProfileCreate, ProfileUpdate, ProfileResponse

router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"]
)

# 🟢 Crear un perfil
@router.post("/", response_model=ProfileResponse)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id_users == profile.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    existing_profile = db.query(Profile).filter(Profile.user_id == profile.user_id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="El usuario ya tiene un perfil creado")

    new_profile = Profile(**profile.dict())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


# 🔵 Obtener un perfil por ID
@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id_profile == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return profile


# 🔵 Obtener un perfil por ID de usuario
@router.get("/user/{user_id}", response_model=ProfileResponse)
def get_profile_by_user(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado para este usuario")
    return profile


# 🟠 Actualizar un perfil
@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile(profile_id: int, updated_data: ProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id_profile == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile


# 🔴 Eliminar un perfil
@router.delete("/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id_profile == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    db.delete(profile)
    db.commit()
    return {"detail": "Perfil eliminado correctamente"}
