from FastAPI  import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
   tags=["users"]
)

class User(BaseModel):
    id: int
    name: str
    email: str
    

user_list = [
    User(id=1, name="John Doe", email="john.doe@example.com"),
    User(id=2, name="Jane Smith", email="jane.smith@example.com"),
    User(id=3, name="Alice Johnson", email="alice.johnson@example.com"),
]




@router.get("/users")
async def get_users():
    return user_list

@router.get("/user/{user_id}")
async def get_user(user_id: int):
    return find_user(user_id)



@router.post("/user",response_model=User, status_code=201)
async def create_user(user: User):
    user_list.append(user)
    return {"message": "User created successfully", "user": user}




def find_user(user_id: int):
    users = filter(lambda user: user.id == user_id, user_list)
    try:
        return list(users)[0]
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found"
        )