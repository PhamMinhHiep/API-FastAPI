from typing import List

import uvicorn
import logging

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

import models, schemas, crud
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

from datetime import datetime

app = FastAPI()

# Dependency


def get_db():
    db = None
    try:
        db = SessionLocal()

        #yield used to generate function
        yield db
    finally:
        db.close()


@app.post("/user", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# response_model: return type
@app.post("/authenticate", response_model=schemas.UserInfo)
def authenticate_user(user: schemas.UserAuthenticate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username not existed")
    else:
        try:
            is_password_correct = crud.check_username_password(db, user)
            if is_password_correct is False:
                raise HTTPException(status_code=400, detail="Password is not correct")
            else:
                from datetime import timedelta
                access_token_expires = timedelta(minutes=15)
                from crud import create_access_token
                access_token = create_access_token(
                    data={"sub": user.username}, expires_delta=access_token_expires)
            return_value = {"access_token": access_token, "token_type": "Bearer"}
            return crud.create_user(db= db, user = user)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=501, detail="Error here")
            #return {"access_token": access_token, "token_type": "Bearer"} 

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)