# crafty/crud/product.py

import logging

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from crafty.db.models.product import Product, ProductImage
from crafty.exceptions import (NoProductsFoundError, ProductAlreadyExistsError,
                               ProductImageNotFoundError, ProductNotFoundError)
from crafty.schemas.product import ProductCreate, ProductUpdate

logger = logging.getLogger(__name__)


def create_product(db: Session, product: ProductCreate) -> Product:
    """
    Create a new product in the database.

    Args:
        db (Session): The database session.
        product (ProductCreate): The product data to create.

    Returns:
        Product: The created product object.

    Raises:
        ProductAlreadyExistsError: If a product with the same name already exists.
    """
    try:
        if db.query(Product).filter(Product.name == product.name).first():
            raise ProductAlreadyExistsError(product.name)

        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        db.rollback()
        raise
    except AttributeError as e:
        logger.error(f"AttributeError while creating product: {e}")
        raise
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise


def get_product(db: Session, product_id: int) -> Product:
    """
    Retrieve a product by ID.

    Args:
        db (Session): The database session.
        product_id (int): The ID of the product to retrieve.

    Returns:
        Product: The retrieved product object.

    Raises:
        ProductNotFoundError: If no product with the given ID exists.
    """
    product = db.query(Product).filter(Product.id == product_id).one_or_none()
    if not product:
        logger.warning(f"Product with ID {product_id} not found")
        raise ProductNotFoundError(product_id)
    return product


def get_products(db: Session, skip: int = 0, limit: int = 10) -> list[Product]:
    """
    Retrieve a list of products with optional pagination.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        list[Product]: List of product objects.
    """
    return db.query(Product).offset(skip).limit(limit).all()


def update_product(
    db: Session, product_id: int, product_update: ProductUpdate
) -> Product:
    """
    Update a product in the database.

    Args:
        db (Session): The database session.
        product_id (int): The ID of the product to update.
        product_update (ProductUpdate): The updated product data.

    Returns:
        Product: The updated product object.

    Raises:
        ProductNotFoundError: If the product with the given ID does not exist.
    """
    db_product = db.query(Product).filter(Product.id == product_id).one_or_none()
    if db_product is None:
        raise ProductNotFoundError(product_id)

    for field, value in product_update.dict(exclude_unset=True).items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    """
    Delete a product from the database.

    Args:
        db (Session): The database session.
        product_id (int): The ID of the product to delete.

    Raises:
        ProductNotFoundError: If no product with the given ID exists.
    """
    db_product = db.query(Product).filter(Product.id == product_id).one_or_none()
    if db_product is None:
        raise ProductNotFoundError(product_id)

    db.delete(db_product)
    db.commit()


def create_product_image(db: Session, image_url: str, product_id: int) -> ProductImage:
    """
    Create a new product image in the database.

    Args:
        db (Session): The database session.
        image_url (str): The URL of the product image.
        product_id (int): The ID of the associated product.

    Returns:
        ProductImage: The created product image object.

    Raises:
        ProductNotFoundError: If no product with the given ID exists.
    """
    if not db.query(Product).filter(Product.id == product_id).one_or_none():
        raise ProductNotFoundError(product_id)

    db_product_image = ProductImage(image_url=image_url, product_id=product_id)
    db.add(db_product_image)
    db.commit()
    db.refresh(db_product_image)
    return db_product_image


def get_product_image(db: Session, image_id: int) -> ProductImage:
    """
    Retrieve a product image by ID.

    Args:
        db (Session): The database session.
        image_id (int): The ID of the image to retrieve.

    Returns:
        ProductImage: The retrieved product image object.

    Raises:
        ProductImageNotFoundError: If no image with the given ID exists.
    """
    product_image = (
        db.query(ProductImage).filter(ProductImage.id == image_id).one_or_none()
    )
    if not product_image:
        raise ProductImageNotFoundError(image_id)
    return product_image


def get_products_by_seller(db: Session, seller_id: int, skip: int = 0, limit: int = 10):
    """
    Retrieve all products associated with a specific seller.

    Args:
        db (Session): The database session.
        seller_id (int): The ID of the seller whose products to retrieve.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        List[Product]: A list of products associated with the specified seller.

    Raises:
        NoProductsFoundError: If no products are found for the seller.
    """
    try:
        products = (
            db.query(Product)
            .filter(Product.seller_id == seller_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        if not products:
            raise NoProductsFoundError(seller_id)
        return products
    except AttributeError as e:
        logger.error(
            f"AttributeError while retrieving products for seller {seller_id}: {e}"
        )
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error while retrieving products for seller {seller_id}: {e}"
        )
        raise
