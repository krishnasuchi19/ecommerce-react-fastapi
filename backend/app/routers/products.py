from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.products import Products
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/products",
    tags = ["Product"]
)


@router.post("/", response_model = ProductResponse)
def create_product(
    data:ProductCreate,
    db: Session= Depends(get_db),
    current_user = Depends(get_current_user)
):
    product = Products(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product



@router.get("/", response_model = list[ProductResponse])
def get_product(
    db: Session = Depends(get_db)
):
    all_products  = db.query(Products).filter(Products.is_active == True).all()
    return all_products


@router.get("/{product_id}", response_model = ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        raise HTTPException(status_code = 402, detail = "Product not found")


    return product

@router.patch("/{product_id}")
def update_product(
    product_id:int,
    data: ProductUpdate,
    db: Session= Depends(get_db),
    current_user = Depends(get_current_user)
):
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        raise HTTPException(status_code = 401, detail = "Product not found")


    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    
    return product


@router.delete("/{product_id}")
def product_delete(
    product_id :int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        raise HTTPException(status_code = 404, detail = "Product not found")
    
    product.is_active = False
    db.commit()
    return {"message":"Product Deleted"}

    


