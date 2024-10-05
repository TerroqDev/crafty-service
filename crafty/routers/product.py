# crafty/routers/product.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crafty.crud.product import (create_product, create_product_image,
                                 delete_product, get_product,
                                 get_product_image, get_products,
                                 get_products_by_seller, update_product)
from crafty.db.session import get_db
from crafty.decorators import handle_http_exceptions
from crafty.exceptions import (NoProductsFoundError, ProductAlreadyExistsError,
                               ProductImageNotFoundError, ProductNotFoundError)
from crafty.schemas.product import (Product, ProductCreate, ProductImage,
                                    ProductUpdate)

router = APIRouter(tags=["products"], prefix="/products")

exception_mapping = {
    ProductAlreadyExistsError: 400,
    ProductNotFoundError: 404,
    ProductImageNotFoundError: 404,
    NoProductsFoundError: 404,
}


@router.post("/", response_model=Product)
@handle_http_exceptions(exception_mapping)
async def create_new_product(
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
        HTTPException: If a product with the same name already exists (400 Bad Request).
    """
    return create_product(db=db, product=product)


@router.get("/{product_id}", response_model=Product)
@handle_http_exceptions(exception_mapping)
async def read_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    """
    Retrieve a product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Product: The retrieved product object.

    Raises:
        HTTPException: If the product is not found (404 Not Found).
    """
    return get_product(db, product_id=product_id)


@router.get("/", response_model=List[Product])
async def read_products(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[Product]:
    """
    Retrieve a list of products with optional pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Product]: A list of product objects.
    """
    return get_products(db, skip=skip, limit=limit)


@router.put("/{product_id}", response_model=Product)
@handle_http_exceptions(exception_mapping)
async def update_existing_product(
    product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)
) -> Product:
    """
    Update an existing product by its ID.

    Args:
        product_id (int): The ID of the product to update.
        product_update (ProductUpdate): The updated product data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Product: The updated product object.

    Raises:
        HTTPException: If the product is not found (404 Not Found).
    """
    return update_product(db, product_id=product_id, product_update=product_update)


@router.delete("/{product_id}", status_code=204)
@handle_http_exceptions(exception_mapping)
async def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product by its ID.

    Args:
        product_id (int): The ID of the product to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the product is not found (404 Not Found).
    """
    await delete_product(db, product_id=product_id)


@router.post("/{product_id}/images/", response_model=ProductImage)
@handle_http_exceptions(exception_mapping)
async def create_new_product_image(
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
        HTTPException: If the product is not found (404 Not Found).
    """
    return create_product_image(db, image_url=image_url, product_id=product_id)


@router.get("/images/{image_id}", response_model=ProductImage)
@handle_http_exceptions(exception_mapping)
async def read_product_image(
    image_id: int, db: Session = Depends(get_db)
) -> ProductImage:
    """
    Retrieve a product image by its ID.

    Args:
        image_id (int): The ID of the image to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        ProductImage: The retrieved product image object.

    Raises:
        HTTPException: If the image is not found (404 Not Found).
    """
    return get_product_image(db, image_id=image_id)


@router.get("/sellers/{seller_id}/products/", response_model=List[Product])
@handle_http_exceptions(exception_mapping)
async def read_products_by_seller(
    seller_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[Product]:
    """
    Retrieve all products associated with a specific seller.

    This endpoint fetches a list of products that belong to a seller specified by their ID.
    It supports pagination through the 'skip' and 'limit' parameters.

    Args:
        seller_id (int): The ID of the seller whose products are to be retrieved.
        skip (int, optional): The number of records to skip (for pagination). Defaults to 0.
        limit (int, optional): The maximum number of records to return. Defaults to 10.
        db (Session, optional): The database session, automatically provided by FastAPI's dependency injection.

    Returns:
        List[Product]: A list of product objects associated with the specified seller.

    Raises:
        NoProductsFoundError: If no products are found for the specified seller.
        HTTPException: If there is an internal server error while processing the request.
    """
    return get_products_by_seller(db, seller_id, skip=skip, limit=limit)
