from app.persistence import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

class Amenity(Base):
    """Amenity model"""
    __tablename__ = 'amenities'

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    _name = Column("name", String(50), nullable=False)
    places = relationship("Place", secondary="place_amenity", back_populates="amenities")

    def __init__(self, name):
        if not name:
            raise ValueError("Required attributes not specified!")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name

    # --- Getters and Setters ---
    @property
    def name(self):
        """ Returns value of property name """
        return self._name

    @name.setter
    def name(self, value):
        """Setter for prop name"""
        # ensure that the value is up to 50 characters after removing excess white-space
        if not value or not isinstance(value, str) or not (0 < len(value.strip()) <= 50):
            raise ValueError("Name must be up to 50 characters in length")
        self._name = value.strip()


    # --- Methods ---
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'name': self.name
        }
