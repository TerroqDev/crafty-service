import datetime
import random

from alembic import command
from alembic.config import Config
from invoke import task
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from crafty.config import get_settings
from crafty.constants import Rating, SubscriptionLevel, UserType
from crafty.db.database import Base, engine
from crafty.db.models.favorite import Favorite
from crafty.db.models.product import Product, ProductImage
from crafty.db.models.review import Review
from crafty.db.models.subscription import Subscription
from crafty.db.models.tag import Tag
from crafty.db.models.user import Buyer, Seller
from crafty.db.session import db_session


@task
def create_db(ctx):
    """Create the database schema."""
    if not database_exists(get_settings().database_url):
        create_database(get_settings().database_url)
        command.upgrade(Config("alembic.ini"), "head")


@task
def drop_db(ctx):
    """Drop the database schema."""
    if database_exists(get_settings().database_url):
        drop_database(get_settings().database_url)


@task
def populate_db(ctx):
    """Populate the database with sample data."""
    with db_session() as session:
        # Create sample users
        buyer = Buyer(
            username="john_doee",
            email="john@example.com",
            password_hash="hashed_password",
        )
        seller = Seller(
            username="jane_doe",
            email="jane@example.com",
            password_hash="hashed_password",
            subscription_level="basic",
        )

        session.add(buyer)
        session.add(seller)
        session.commit()

        # Create sample products
        products = [
            Product(
                name="Laptop",
                description="A high-performance laptop",
                price=999,
                seller_id=seller.id,
            ),
            Product(
                name="Smartphone",
                description="A new generation smartphone",
                price=499,
                seller_id=seller.id,
            ),
        ]
        session.add_all(products)
        session.commit()

        # Create sample product images
        product_images = [
            ProductImage(
                image_url="http://example.com/laptop.jpg", product_id=products[0].id
            ),
            ProductImage(
                image_url="http://example.com/smartphone.jpg", product_id=products[1].id
            ),
        ]
        session.add_all(product_images)
        session.commit()

        # Create sample tags
        tags = [
            Tag(name="Electronics"),
            Tag(name="Gadgets"),
        ]
        session.add_all(tags)
        session.commit()

        # Associate tags with products
        products_tags = [
            (products[0].id, tags[0].id),
            (products[1].id, tags[1].id),
        ]
        for product_id, tag_id in products_tags:
            stmt = text(
                f"INSERT INTO products_tags (product_id, tag_id) VALUES ({product_id}, {tag_id})"
            )
            session.execute(stmt)
        session.commit()

        # Create sample reviews
        reviews_data = [
            (Rating.five, "Great product!", buyer.id, seller.id, products[0].id),
            (Rating.four, "Very useful!", buyer.id, seller.id, products[1].id),
        ]

        for rating, comment, reviewer_id, reviewed_user_id, product_id in reviews_data:
            review = Review(
                rating=rating,
                comment=comment,
                reviewer_id=reviewer_id,
                reviewed_user_id=reviewed_user_id,
                product_id=product_id,
            )
            try:
                session.add(review)
                session.commit()
            except IntegrityError:
                session.rollback()
                print(
                    f"Could not add review for product ID {product_id}. Review already exists."
                )

        # Create sample favorites
        favorites = [
            Favorite(buyer_id=buyer.id, product_id=products[0].id),
        ]
        session.add_all(favorites)
        session.commit()

        # Create sample subscriptions
        subscriptions = [
            Subscription(
                seller_id=seller.id,
                subscription_level=SubscriptionLevel.basic,
                start_date=datetime.date(2024, 1, 1),
                end_date=datetime.date(2024, 12, 31),
            ),
        ]
        session.add_all(subscriptions)
        session.commit()

        print("Database populated with sample data.")


@task
def reset_db(ctx):
    """Drop and recreate the database schema, then populate with sample data."""
    drop_db(ctx)
    create_db(ctx)
    populate_db(ctx)
