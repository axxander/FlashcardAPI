from pydantic import BaseModel

class JWTUser(BaseModel):
    username: str

class JWT(BaseModel):
    access_token: str
    token_type: str