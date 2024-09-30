import datetime
import random

from invoke import task
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from crafty.constants import Rating, SubscriptionLevel, UserType
from crafty.db.database import Base, engine
from crafty.db.models.favorite import Favorite
from crafty.db.models.product import Product, ProductImage
from crafty.db.models.review import Review
from crafty.db.models.subscription import Subscription
from crafty.db.models.tag import Tag
from crafty.db.models.user import Buyer, Seller, User
from crafty.db.session import db_session


@task
def create_db(ctx):
    """Create the database schema."""
    Base.metadata.create_all(engine)


@task
def drop_db(ctx):
    """Drop the database schema."""
    Base.metadata.drop_all(engine)


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
        reviews = [
            Review(
                rating=Rating.five,
                comment="Great product!",
                reviewer_id=buyer.id,
                reviewed_user_id=seller.id,
                product_id=products[0].id,
            ),
        ]
        session.add_all(reviews)
        session.commit()

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
