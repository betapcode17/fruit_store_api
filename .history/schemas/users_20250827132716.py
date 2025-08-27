
class UserCreate(BaseModel):
    email:str
    password:str
    name: str
    phone: str
    address: str
    birth:date
    gender:bool
    username: str
    role: bool
    valid:bool


class UserUpdate(BaseModel):
    email:Optional[str] = None
    password:Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birth:Optional[date] = None
    gender:Optional[bool] = None
    username: Optional[str] = None
    role: Optional[bool] = None
    valid:Optional[bool] = None



class UserCreate(BaseModel):
    email:str
    password:str
    name: str
    phone: str
    address: str
    birth:date
    gender:bool
    username: str
    role: bool
    valid:bool

    class  Config:
        orm_mode = True