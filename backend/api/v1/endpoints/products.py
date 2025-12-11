from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    image_url: Optional[str] = None
    stock_quantity: int = 0
    size_options: List[str] = []
    color_options: List[str] = []

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    is_available: bool
    visual_description: Optional[str] = None

    class Config:
        orm_mode = True

@router.get("/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # 1. Generate Visual Description if image provided
    visual_desc = ""
    if product.image_url:
        from backend.services.vision_service import vision_service
        # Background task ideally, but doing sync for simplicity per prototype
        print(f"Products Endpoint received image_url: {product.image_url}")
        visual_desc = vision_service.analyze_image(product.image_url)
        print(f"Generated Description: {visual_desc}")
    
    # 2. Create Product
    product_data = product.dict()
    db_product = models.Product(**product_data)
    db_product.visual_description = visual_desc
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
