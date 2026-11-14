'''
CRUD operations for the application.
CRUD Handles Database interactions, providing functions to Create, Read, Update, and Delete records in the database.
'''


from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, schemas

# Step-1 Creating a new user in the database
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        age=user.age
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)  # Refresh to get the generated ID and other fields
        return db_user
    except IntegrityError:
        db.rollback()  # Undo the failed insert (e.g., duplicate username/email)
        return None
    


# Step-2: Read all users from the database
def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Step-3: Read a single user by ID from the database
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Step-3b: Read a single user by username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Step-4: Read a single user by email from the database
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Step-5: Update a user in the database (only updates fields that were sent in the request)
def update_user(db: Session, user_id: int, updates: schemas.UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    # Only update fields that were actually sent
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(db_user)
    return db_user

# Step-6: Delete a user from the database
def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True