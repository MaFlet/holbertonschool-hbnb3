from app.persistence import Base
from app.models.user import User
import uuid
from datetime import datetime
from flask_bcrypt import Bcrypt
from sqlalchemy import Column, String, Float, DateTime, Float, ForeignKey, Text, Table
from sqlalchemy.orm import relationship

bcrypt = Bcrypt()

place_amenity = Table('place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True)
)

class Place(Base):
    """ Place class"""
    __tablename__ = 'places'

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    _title = Column("title", String(100), nullable=False)
    _description = Column("description", Text, nullable=False)
    _price = Column("price", Float, nullable=False)
    _latitude = Column("latitude", Float, nullable=False)
    _longitude = Column("longitude", Float, default=False)
    _owner_id = Column("owner_id", String(36), ForeignKey('users.id'), nullable=False)
    owner_r = relationship("User", back_populates="places_r")
    reviews_r = relationship("Review", back_populates="user_r", cascade="delete, delete-orphan")
    properties_r = relationship("Place", back_populates="owner_r", cascade="delete, delete-orphan")
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="places")

    def __init__(self, title, description, price, latitude, longitude, owner_id):
            if not all([ptitle, description, price is not None,
                       latitude is not None, longitude is not None, owner_id]):
                raise ValueError("Required attributes not specified!")

            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.title = title
            self.description = description
            self.price = price
            self.latitude = latitude
            self.longitude = longitude
            self._owner_id = owner_id
            self.reviews = []  # relationship - List to store related reviews
            self.amenities = []  # relationship - List to store related amenities

    # --- Getters and Setters ---
    @property
    def title(self):
        """ Returns value of property title """
        return self._title

    @title.setter
    def title(self, value):
        """Setter for prop title"""
        # ensure that the value is up to 100 alphabets only after removing excess white-space
        if not value or not isinstance(value, str) or not (0 < len(value.strip()) <= 100):
            raise ValueError("Title should be 100 characters long")
        self._title = value.strip()

    @property
    def description(self):
        """ Returns value of property description """
        return self._description

    @description.setter
    def description(self, value):
        """Setter for prop description"""
        # Can't think of any special checks to perform here tbh
        if not value or not isinstance(value, str):
            raise ValueError("Description should be not empty")
        self._description = value.strip()

    @property
    def price(self):
        """ Returns value of property price """
        return self._price

    @price.setter
    def price(self, value):
        """Setter for prop price"""
        try:
            float_value = float(value)
            if float_value <= 0:
                raise ValueError
            self._price = float_value
        except (TypeError, ValueError):
            raise ValueError("Price must be a positive number")

    @property
    def latitude(self):
        """ Returns value of property latitude """
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Setter for prop latitude"""
        if isinstance(value, (float, int)) or not -90.0 <= float(value) <= 90.0:
            raise ValueError("Invalid value specified for Latitude")
        self._latitude = float(value)

    @property
    def longitude(self):
        """ Returns value of property longitude """
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Setter for prop longitude"""
        if isinstance(value, (float, int)) or not -180.0 <= float(value) <= 180.0:
            raise ValueError("Invalid value specified for Longitude")
        self._longitude = float(value)

    @property
    def owner(self):
        """ Returns value of property owner """
        return self._owner

    @owner.setter
    def owner(self, value):
        """Setter for prop owner"""
        if isinstance(value, User):
            self._owner = value
        else:
            raise ValueError("Invalid object type passed in for owner!")

    # --- Methods ---
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    @staticmethod
    def place_exists(place_id):
        """ Search through all Places to ensure the specified place_id exists """
        # Unused - the facade get_place method will handle this
