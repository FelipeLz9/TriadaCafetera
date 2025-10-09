from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.review import Review
from models.user import User
from schemas.review_schema import ReviewCreate, ReviewResponse
from typing import List

router = APIRouter(
    prefix="/review",
    tags=["Review"]
)

#  Crear una reseña
@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id_users == review.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    new_review = Review(**review.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


#  Obtener todas las reseñas
@router.get("/", response_model=List[ReviewResponse])
def get_all_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).all()
    return reviews


#  Obtener una reseña por ID
@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id_review == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    return review


#  Eliminar una reseña
@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id_review == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    db.delete(review)
    db.commit()
    return {"detail": "Reseña eliminada correctamente"}
