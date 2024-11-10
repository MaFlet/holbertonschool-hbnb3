from app.models.amenity import Amenity
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository
from app.persistence import db_session
from sqlalchemy import text 

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
    
    def delete(self, amenity_id):
        """Delete an amenity"""
        try:
            amenity = db_session.query(Amenity).get(amenity_id)
            if not amenity:
                print(f"Amenity {amenity_id} not found")
                return False
            db_session.execute(
                text('DELETE FROM place_amenity WHERE amenity_id = :aid'),
                {'aid': amenity_id}
            )
            db_session.flush()
            amenity.places = []
            db_session.flush()

            db_session.delete(amenity)
            db_session.flush()

            db_session.commit()
            print(f"Successfully deleted amenity {amenity_id}")
            return True
        
        except Exception as e:
            db_session.rollback()
            raise ValueError(f"Error deleting amenity: {str(e)}")


# Use these CURL commands for testing
#curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" -H "Content-Type: application/json" -d '{"name": "Wifi"}'
#curl -X GET "http://127.0.0.1:5000/api/v1/amenities/<amenity_id>""
# curl -X PUT "http://127.0.0.1:5000/api/v1/amenities/<amenity_id>" -H "Content-Type: application/json" -d '{"name": " Air conditioning"}'
# curl -X DELETE "http://127.0.0.1:5000/api/v1/amenities/<amenity_id>" and confirm deletion with curl -X GET "http://127.0.0.1:5000/api/v1/amenities/<amenity_id>""
# if the DELETE curl command won't work, use these commands via MySQL:
# mysql -u hbnb_evo_2 -p
# USE hbnb_evo_2_db;
# SELECT * FROM amenities WHERE id = '<amenity_id>
# DELETE FROM place_amenity WHERE amenity_id = 'd8ac4ba0-ae01-4bcd-951a-268883470c28';
# DELETE FROM amenities WHERE id = 'd8ac4ba0-ae01-4bcd-951a-268883470c28';
# OR PLEASE REFRESH SERVER