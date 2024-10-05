# crafty/routers/product.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crafty.crud.product import (create_product, create_product_image,
                                 delete_product, get_product,
                                 get_product_image, get_products,
                                 update_product)
from crafty.db.session import get_db
from crafty.exceptions import (ProductAlreadyExistsError,
                               ProductImageNotFoundError, ProductNotFoundError)
from crafty.schemas.product import (Product, ProductCreate, ProductImage,
                                    ProductUpdate)

router = APIRouter(tags=["products"], prefix="/products")


@router.post("/", response_model=Product)
def create_new_product(
    product: ProductCreate, db: Session = Depends(get_db)
) -> Product:
    """
    Create a new product.

    Args:
        product (ProductCreate): The product data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Product: The created product object.

    Raises:
        HTTPException: If a product with the same name already exists or other internal errors occur.
    """
    try:
        return create_product(db=db, product=product)
    except ProductAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    """
    Retrieve a product by ID.

    Args:
        product_id (int): The ID of the product to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Product: The retrieved product object.

    Raises:
        HTTPException: If the product is not found or other internal errors occur.
    """
    try:
        return get_product(db, product_id=product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[Product])
def read_products(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[Product]:
    """
    Retrieve a list of products with optional pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Product]: List of product objects.
    """
    return get_products(db, skip=skip, limit=limit)


@router.put("/{product_id}", response_model=Product)
def update_existing_product(
    product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)
) -> Product:
    """
    Update an existing product.

    Args:
        product_id (int): The ID of the product to update.
        product_update (ProductUpdate): The updated product data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Product: The updated product object.

    Raises:
        HTTPException: If the product is not found or other internal errors occur.
    """
    try:
        return update_product(db, product_id=product_id, product_update=product_update)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{product_id}", status_code=204)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product.

    Args:
        product_id (int): The ID of the product to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the product is not found or other internal errors occur.
    """
    try:
        delete_product(db, product_id=product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{product_id}/images/", response_model=ProductImage)
def create_new_product_image(
    product_id: int, image_url: str, db: Session = Depends(get_db)
) -> ProductImage:
    """
    Create a new product image.

    Args:
        product_id (int): The ID of the associated product.
        image_url (str): The URL of the product image.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        ProductImage: The created product image object.

    Raises:
        HTTPException: If the product is not found or other internal errors occur.
    """
    try:
        return create_product_image(db, image_url=image_url, product_id=product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/images/{image_id}", response_model=ProductImage)
def read_product_image(image_id: int, db: Session = Depends(get_db)) -> ProductImage:
    """
    Retrieve a product image by ID.

    Args:
        image_id (int): The ID of the image to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        ProductImage: The retrieved product image object.

    Raises:
        HTTPException: If the image is not found or other internal errors occur.
    """
    try:
        return get_product_image(db, image_id=image_id)
    except ProductImageNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
