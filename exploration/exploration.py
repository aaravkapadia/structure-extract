from fastapi import FastAPI
from enum import Enum
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# @app.get("/users/me")
# async def read_user_me():
#     return {"user_id": "the current user"}

# @app.get("/users/me")
# async def read_user_2():
#     return ["Aarav", "Kapadia"]

# @app.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id": user_id}

# class Name(str, Enum):
#     son = "Aarav"
#     daughter = "Mira"
#     mother = "Megha"

# @app.get("/names/{name}")
# async def get_name(name: Name):
#     if name is Name.son:
#         return {"name": name, "msg": "Aarav is the best"}
#     if name is Name.daughter:
#         return {"name": name, "msg": "Mira is second"}
#     return {"name": name, "msg": "Megha is the root"}

# itemsDB = [{"item_name": "car"}, {"item_name": "jacket"}, {"item_name": "computer"}]

# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return itemsDB[skip : skip + limit]

# @app.get("/item/{item_id}/")
# async def read_item(item_id: str, q: Optional[str]= None, p: Optional[str] = None):
#     if q:
#         return {"item": item_id, "q" : q, "p" : p}
#     return {"item": item_id, "q": "q not found", "p" : "p not found"}

# @app.get("/item/{item_id}")
# async def read_item(item_id: str, q: Optional[str], b: bool=False):
#     if b and q:
#         return {"item": item_id, "q": q}
#     return {"item": "not found", "q": "switch off"}

# @app.get("/category/{category}/item/{item_id}/")
# async def read_item(item_id: str, category: str, q: Optional[str]=None):
#     return {"category": category, "item" : item_id, "q" : q}

# class Item(BaseModel):
#     name: str
#     description: str=None
#     price: float
#     tax: Optional[float]= None
    
# @app.post("/items/")
# async def create_item(item: Item):
#     return item

# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.model_dump()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         #item_dict.update({"price_with_tax": price_with_tax})
#         item_dict["price_with_tax"] = price_with_tax
#     return item_dict


        

