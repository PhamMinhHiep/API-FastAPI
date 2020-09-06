from sqlalchemy.orm import Session

import models, schemas

from datetime import datetime
import bcrypt
import logging

import jwt

# get user name
def get_user_by_username(db: Session, username: str):
	result = None
	try:
		result =  db.query(models.UserInfo).filter(models.UserInfo.username == username).first()
	except Exception as e:
		logging.exception('this is an exception')
	return result


# create user using hashing
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.UserInfo(username=user.username, password=hashed_password, fullname=user.fullname)
    # print(db_user._asdict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_username_password(db: Session, user: schemas.UserAuthenticate):
    db_user_info: models.UserInfo = get_user_by_username(db, username = user.username)
    print(user.password.encode('utf-8'))
    print('\n\n\n')
    print(db_user_info.password.encode('utf-8'))
    print('\n\n\n')
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password.encode('utf-8'))
    
    
	 

def create_access_token(*, data: dict, expires_delta: datetime = None):
    secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm = "HS256"
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + datetime.timedelta(minutes = 15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm = algorithm)
    return encoded_jwt