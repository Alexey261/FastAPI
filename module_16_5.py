from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int = Field(default=1, descriptuon='Номер пользователя', ge=1, le=100)
    username: str = Field(default="UrbanUser", descriptuon='Пользователь Urban', min_length=5, max_length=20)
    age: int = Field(default=24, descriptuon='Возраст пользователя', ge=18, le=120)

@app.get('/')
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get('/user/{id}')
async def get_user(request: Request, id: int) -> HTMLResponse:
    user = [user for user in users if user.id == id]
    if len(user) == 1:
        return templates.TemplateResponse("users.html", {"request": request, "user": user[0]})
    else:
        raise HTTPException(status_code=404, detail='User was not found')



@app.post('/user/{username}/{age}')
async def add_user(user: User):
    user.id = 1 if not len(users) else users[len(users)-1].id+1
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example='1')],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", example='24')]):
    try:
        users[user_id-1].username = username
        users[user_id-1].age = age
        return users[user_id-1]
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

@app.delete('/user/{user_id}')
async def delete_user(user_id: int = Path(ge=1, le=100, description="Enter User ID", example='1')):
    try:
        return users.pop(user_id-1)
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')



