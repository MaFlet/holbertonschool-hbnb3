from app.persistence import Base
from app.models.user import User
import uuid
import json
from datetime import datetime
from flask_bcrypt import Bcrypt
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, Table, JSON
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
    _longitude = Column("longitude", Float, nullable=False)
    image_paths = Column(JSON)
    _owner_id = Column("owner_id", String(60), ForeignKey('users.id'), nullable=False)
    owner_r = relationship("User", back_populates="places_r")
    reviews_r = relationship("Review", back_populates="place_r")
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="places")

    def __init__(self, title, description, price, latitude, longitude, owner_id, image_paths=None):
            if not all([title, description, price is not None,
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
            self.image_paths = image_paths or []

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
        try:
            float_value = float(value)
            if not -90.0 <= float_value <= 90.0:
                raise ValueError
            self._latitude = float_value
        except (TypeError, ValueError):
            raise ValueError("Invalid value specified for Latitude")

    @property
    def longitude(self):
        """ Returns value of property longitude """
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Setter for prop longitude"""
        try:
            float_value = float(value)
            if not -180.0 <= float_value <= 180.0:
                raise ValueError
            self._longitude = float_value
        except (TypeError, ValueError):
            raise ValueError("Invalid value specified for Longitude")

    @property
    def owner_id(self):
        """ Returns value of property owner """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        """Setter for prop owner"""
        if not value or not isinstance(value, str):
            raise ValueError("Invalid object type passed in for owner!")
        
        from app.persistence import db_session
        from app.models.user import User

        existing_user = db_session.query(User).filter(User.id == value).first()
        if not existing_user:
            raise ValueError("Owner does not exist")
        
        self._owner_id = value


    # --- Methods ---
    @property
    def owner(self):
        """Convinience property to access owner relationship"""
        return self.owner_r
    
    def set_image_paths(self, paths):
        """Set image paths, ensuring proper JSON format"""
        self.image_paths = paths if isinstance(paths, list) else []

    def get_image_paths(self):
        """Return the image paths as a list"""
        return self.image_paths if self.image_paths else []

    # --- Methods ---
    # def save(self):
    #     """Update the updated_at timestamp whenever the object is modified"""
    #     self.updated_at = datetime.now()

    # def add_review(self, review):
    #     """Add a review to the place."""
    #     self.reviews.append(review)

    # def add_amenity(self, amenity):
    #     """Add an amenity to the place."""
    #     self.amenities.append(amenity)

    # @staticmethod
    # def place_exists(place_id):
    #     """ Search through all Places to ensure the specified place_id exists """
    #     # Unused - the facade get_place method will handle this
