from app.persistence import db_session
from abc import ABC, abstractmethod
from app.models.user import User
#from app.models.place import Place

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        try:
            db_session.add(obj)
            db_session.commit()
            db_session.refresh(obj)
            return obj
        except Exception as e:
            db_session.rollback()
            raise ValueError(f"Error adding object: {str(e)}")

    def get(self, obj_id):
        return db_session.query(self.model).get(obj_id)

    def get_all(self):
        return db_session.query(self.model).all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            try:
                for key, value in data.items():
                    if key == 'email':
                        obj.email = value
                    elif key == 'password':
                        obj.password = value
                    elif key == 'first_name':
                        obj.first_name = value
                    elif key == 'last_name':
                        obj.last_name = value
                    else:
                        setattr(obj, key, value)
                db_session.commit()
                db_session.refresh(obj)
                return obj
            except Exception as e:
                db_session.rollback()
                raise ValueError(f"Error updating object: {str(e)}")
        return None

    def delete(self, obj_id):
        try:
            obj = db_session.query(self.model).get(obj_id)
            if obj:
                db_session.delete(obj)
                db_session.commit()
                return True
            return False
        except Exception as e:
            db_session.rollback()
            raise ValueError(f"Error deleting object: {str(e)}")

    def get_by_attribute(self, attr_name, attr_value):
        return db_session.query(self.model).filter(getattr(self.model, attr_name) == attr_value).first()