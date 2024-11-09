from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.persistence import db_session

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        """Get user by validated email and handling the underscore prefix"""
        return db_session.query(Review).filter(Review.place_id == place_id).first()
    
    def get_reviews_by_user(self, user_id):
        """Get all the reviews by user id"""
        return db_session.query(Review).filter(Review.user_id == user_id).all()
    
    def add(self, review_data):
        """Add a new review with attributes"""
        try:
            if isinstance(review_data, dict):
                review = Review(
                    text = review_data['text'],
                    rating = review_data['rating'],
                    place_id = review_data['place_id'],
                    user_id = review_data ('user_id')                
                )
            else:
                review = review_data

            db_session.add(review)
            db_session.commit()
            db_session.refresh(review)
            return review
        except Exception as e:
            db_session.rollback()
            raise ValueError(f"Error adding user: {str(e)}")
        
    def update(self, review_id, review_data):
        """Update review with attributes"""
        review = self.get(review_id)
        if review:
            try:
                if 'text' in review_data:
                    review.text = review_data['text']
                if 'rating' in review_data:
                    review.rating = review_data['rating']
                db_session.commit()
                db_session.refresh(review)
                return review
            except Exception as e:
                db_session.rollback()
                raise ValueError(f"Error updating user: {str(e)}")
        return None
    
    def delete(self, review_id):
        """Delete a review"""
        try:
            review = self.get(review_id)
            if review:
                db_session.delete(review)
                db_session.commit()
                return True
            return False
        except Exception as e:
            db_session.rollback()
            raise ValueError(f"Error deleting review: {str(e)}")
