from app.models.amenity import Amenity
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository
from app.persistence import db_session

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        """Get Amenity by name"""
        return db_session.query(Amenity).filter(Amenity._name == name).first()
    
    def add(self, amenity_data):
        """Add a amenity with attributes"""
        try:
            if isinstance(amenity_data, dict):
                amenity = Amenity(
                    name = amenity_data['name']
                )
            else:
                amenity = amenity_data

            db_session.add(amenity)
            db_session.commit()
            db_session.refresh(amenity)
            return amenity
        except Exception as e:
            db_session.rollback()
            raise ValueError(f"Error adding amenity: {str(e)}")
        
    def update(self, amenity_id, amenity_data):
        """Update amenity with attributes"""
        amenity = self.get(amenity_id)
        if amenity:
            try:
                if 'name' in amenity_data:
                    amenity.name = amenity_data['name']
                db_session.commit()
                db_session.refresh(amenity)
                return amenity
            except Exception as e:
                db_session.rollback()
                raise ValueError(f"Error updating amenity: {str(e)}")
        return None
    
    def get_amenities_by_place(self, place_id):
        """Get all amenities for a specific place"""
        return (db_session.query(Amenity)
                .join(Amenity.places)
                .filter(Place.id == place_id)
                .all())
    
    def add_to_place(self, amenity_id, place_id):
        """Add this amenity to place"""
        try:
            amenity = self.get(amenity_id)
            place = db_session.query(Place).get(place_id)

            if amenity and place:
                place.amenities.append(amenity)
                db_session.commit()
                return True
        except Exception as e:
            db_session.rollback()
            raise ValueError (f"Error adding amenity to place: {str(e)}")
        return False
    
    def remove_from_place(self, amenity_id, place_id):
        """Remove/delete amenity from a place"""
        try:
            amenity = self.get(amenity_id)
            place = db_session.query(Place).get(place_id)

            if amenity and place and amenity in place.amenities:
                place.amenities.remove(amenity)
                db_session.commit()
                return True
        except Exception as e:
            db_session.rollback()
            raise ValueError(f"Error removing amenity from place: {str(e)}")
        return False
