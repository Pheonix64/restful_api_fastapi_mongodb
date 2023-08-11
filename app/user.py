from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.schemas import UserSchema, UserLoginSchema
from app.auth.auth_handler import hash_password, signJWT, verify_password
from app.database import connect_db

routerUser = APIRouter()

global collection
global client

@routerUser.on_event("startup")
async def startup():
    global collection
    global client
    client = connect_db()
    db = client["userdb"]
    collection = db["user"]

@routerUser.on_event("shutdown")
async def shutdown():
    client.close()

async def check_user(data: UserLoginSchema):
    user = await collection.find({'email': data.email}).to_list(length=None)
    if len(user)!=1:
        return False
    if user[0]['email'] != data.email:
        return False
    if not verify_password(data.password, user[0]['password']):
        return False
    return True


@routerUser.post("/user/signup")
async def create_user(user: UserSchema):
    """
    Create a new user by registering their account.

    This endpoint allows users to sign up by providing their information in the request body.
    The provided password is securely hashed before storing it in the database.
    If the registration is successful, a signed JWT token is returned.

    Parameters:
    - user (UserSchema): The user information provided in the request body.

    Returns:
    - dict: A dictionary containing a JWT token upon successful registration.

    Raises:
    - HTTPException: If the provided email address already exists in the database (status code 409 Conflict).

    """
    result = await collection.find_one({'email': user.email})
    if result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="user already exists!")
    try:
        user.password = hash_password(user.password) #hash the password first
        result = await collection.insert_one(user.model_dump(exclude_none=True))
        return signJWT(user.email)
    
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_CONFLICT,
                            detail="Bad request!")

@routerUser.post("/user/login")
async def user_login(user: UserLoginSchema):
    """
    Authenticate a user by processing login credentials.

    This endpoint allows users to log in by providing their login credentials in the request body.
    The provided credentials are checked against the database records to verify the user's identity.
    If the credentials are correct, a signed JWT token is returned. Otherwise, an error message is returned.

    Parameters:
    - user (UserLoginSchema): The user's login credentials provided in the request body.

    Returns:
    - Union[dict, JSONResponse]: A dictionary containing a JWT token upon successful authentication,
    or a JSONResponse with an error message if the login details are incorrect.

    """
    if await check_user(user):
        return signJWT(user.email)
    return JSONResponse({
        "error": "Wrong login details!"
    }, 404)