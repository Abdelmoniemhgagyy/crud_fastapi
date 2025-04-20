from fastapi import FastAPI
from pydantic import BaseModel
from app import SessionLocal,Users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class UserCreate(BaseModel):
    name:str

class UserUpdate(BaseModel):
    id: int
    name: str
@app.get("/")
def root():
    return {"Msg":"hello app"}

@app.post("/add_user")
def add_user(user: UserCreate):
    db = SessionLocal()
    new_user = Users(name=user.name)
    db.add(new_user)
    db.commit()
    db.close()
    return {"message": f"تم إضافة المستخدم {user.name} بنجاح!"}


@app.post("/edit_user")
def edit_user(u: UserUpdate):
    db = SessionLocal()
    user = db.query(Users).filter(Users.id == u.id).first()
    if not user:
        return {"error": "المستخدم غير موجود!"}
    user.name = u.name
    db.commit()
    db.refresh(user)
    db.close()
    return {"message": f"تم تعديل المستخدم بنجاح!", "user": {"id": user.id, "name": user.name}}

@app.post("/delete_user")
def delete_user(u: UserUpdate):
    db = SessionLocal()
    user = db.query(Users).filter(Users.id == u.id).first()
    if not user:
        return {"error": "المستخدم غير موجود!"}
    db.delete(user)
    db.commit()
    db.close()
    return {"message": f"تم حذف المستخدم بنجاح!", "user": {"id": user.id, "name": user.name}}


@app.get("/users")
def get_users():
    db=SessionLocal()
    users = db.query(Users).all()
    db.close()
    return {"users":[{"user_id":user.id,"user_name":user.name} for user in users]}

@app.get("/users/{id}")
def get_user_by_id(id:int=None):
    db=SessionLocal()
    user = db.query(Users).filter(Users.id==id).first()
    db.close()
    return {"users":[{"user_id":user.id,"user_name":user.name}]}

@app.get("/users/")
def get_user_by_search_name(name:str=None):
    db=SessionLocal()
    user = db.query(Users).filter(Users.name==name).first()
    db.close()
    if user:
        return {"users":[{"user_id":user.id,"user_name":user.name}]}
    else:
        return "user not found"