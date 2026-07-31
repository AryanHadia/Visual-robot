from models import User
from DataBase import session



class DataBaseManager():
    def __init__(self):
        self.session = session
        self.user = User


    def add_emb(self , Name , Face_embedding):
        '''
        Add the user to the database
        :param Name: Name of the user
        :param Face_embedding: Face embedding of the user
        :return: User object
        '''

        try:
            # check if it already exists
            user = self.session.query(self.user).filter_by(Name=Name).first()
            if user:
                print(f"Add {Name} to database error: User already exists")
                return None
            new_emb = self.user(Name=Name , Face_embedding=Face_embedding)
            self.session.add(new_emb)
            self.session.commit()
            print(f"Add {Name} to database")
            return new_emb
        except Exception as e:
            print(f"Add {Name} to database error: {e}")
            self.session.rollback()
            return None
        
    
    def remove_emb(self , Name):
        '''
        Remove the user from the database
        :param Name: Name of the user
        :return: True if the user is removed, False otherwise
        '''
        try:
            user = self.session.query(self.user).filter_by(Name=Name).first()
            if user:
                self.session.delete(user)
                self.session.commit()
                print(f"Remove {Name} from database")
                return True
            else:
                print(f"Remove {Name} from database error: User not found")
                return False
        except Exception as e:
            print(f"Remove {Name} from database error: {e}")
            self.session.rollback()
            return False


    def get_emb(self , ID):
        '''
        Get the user from the database
        :param ID: ID of the user
        :return: User object
        '''
        try:
            user = self.session.query(self.user).filter_by(Face_id=ID).first()
            if user:
                return user
            else:
                print(f"Get {ID} from database error: User not found")
                return None
        except Exception as e:
            print(f"Get {ID} from database error: {e}")
            self.session.rollback()
            return None

        
    def get_emb_by_name(self , Name):
        '''
        Get the user from the database
        :param Name: Name of the user
        :return: User object
        '''
        try:
            user = self.session.query(self.user).filter_by(Name=Name).first()
            if user:
                return user
            else:
                print(f"Get {Name} from database error: User not found")
                return None
        except Exception as e:
            self.session.rollback()
            print(f"Get {Name} from database error: {e}")
            return None


    def get_all_emb(self):
        '''
        Get all users from the database
        :return: List of User objects
        '''
        try:
            users = self.session.query(self.user).all()
            return users
        except Exception as e:
            self.session.rollback()
            print(f"Get all users from database error: {e}")
            return None
    


    def edit_emb(self , ID , Name , Face_embedding):
        '''
        Edit the user in the database
        :param ID: ID of the user
        :param Name: Name of the user
        :param Face_embedding: Face embedding of the user
        :return: User object
        '''
        try:
            user = self.session.query(self.user).filter(self.user.Face_id==ID).first()
            if user:
                user.Name = Name
                user.Face_embedding = Face_embedding
                self.session.commit()
                print(f"Edit {ID} in database")
                return user
            else:
                print(f"Edit {ID} in database error: User not found")
                return None
        except Exception as e:
            print(f"Edit {ID} in database error: {e}")
            self.session.rollback()
            return None

    
    def close(self): # close the database session
        self.session.close()