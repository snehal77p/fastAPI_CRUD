from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

user_db={
    'jack':{'name':'JACK', 'age':23},
    'jill':{'name':'JILL','age':88},
    'jane':{'name':'JANE','age':90}

}

class User(BaseModel):
    name: str= Field(min_length=3, max_length=120) #Filed used for data validation
    age: int = Field(None, gt=5, lt=100) #gt greater than lt lesser than


def ensure_name_in_db(name: str):
    if name in user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'This user doesnt exists')
    
app = FastAPI()

@app.get('/')
def my_first_fastapi():
    return {'Output':'My first Api'}

@app.get('/users')
def get_users():
    user_list = list(user_db.values())
    return user_list

@app.get('/users/{name}')
def get_users(name: str):
    ensure_name_in_db(name)
    return user_db[name]

@app.get('/queryusers')
def get_queryusers(limit:int=20): #2 is default value
    user_list = list(user_db.values())
    return user_list[:limit]

@app.post('/createuser')
def create_user(user: User):
    name = user.name
    if name in user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'This user already exists')
    user_db[name] = user.dict()
    return {'message': f'Successfully created user:{name}'}

@app.delete('/deleteUser/{name}')
def delete_user(name: str):
    del user_db[name]
    return {'message':f'Successfully deleted: {name}'}

@app.put('/updateUser')
def update_user(user: User):
    name = user.name
    ensure_name_in_db(name)
    user_db[name] = user.dict()
    return {'message':f'successfully updated: {name}'}
    
@app.patch('/updateUser')
def partialupdate_user(user: User):
    name = user.name
    ensure_name_in_db(name)
    user_db[name].update(user.dict())
    return {'message':f'successfully updated: {name}'}
      