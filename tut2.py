from fastapi import FastAPI 
from fastapi import status
from fastapi import HTTPException
from fastapi import BackgroundTasks
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Header 
from fastapi import Depends 
from pydantic import BaseModel
app = FastAPI() 

@app.get("/")
def root(): 
    return {"message": "Hello FastAPI"}

# Path param 
# {item_id} is required 
# item_id: int - means validation happens (non-int -> 422 error)
@app.get("/items/{item_id}")
def get_item(item_id: int): 
    return {"item_id": item_id}

# Query params 
@app.get("/items")
def list_items(page: int = 1, limit: int = 10): 
    return {"page": page, "limit": limit} 

# page and limit comes from ?page=...&limit=...
# default values make them optional 

""""
Rule: 
* If it's in the path -> it's a path parameter 
* If it's not in the path and appears in function signature -> query parameter (for GET-like usage)
"""

# Request body + Pydantic models 
"""
When you send JSON to an API, you need: 
* parsing 
* validation 
* clear schema 
For these, FastAPI uses Pydantic models. 
"""

class ItemCreate(BaseModel): 
    name: str 
    price: float 
    in_stock: bool = True 

@app.post("/items")
def create_item(item: ItemCreate): 
    return {"received": item}

"""
If client sends: {"name": "Mouse", "price": "cheap}
FastAPI responds with 422 and explains what failed. 

This matters bcoz: 
* You don't write manual validation code 
* The schema becomes docs automatically 
* You get typed item.name, item.price 
"""

# Response models (control what you return) 
class ItemOut(BaseModel): 
    name: str 
    price: str 

@app.post("/items", response_model=ItemOut)
def create_item(item: ItemCreate): 
    # pretend DB adds internal things 
    stored = {"name": item.name, "price": item.price, "secret": "dont expose"}
    return stored 

# Response will only include name and price 

# Status codes 
# FastAPI defaults: 
# * ssuccessful GET -> 200 
# * successful POST -> 200 (better is 201) 

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate): 
    return item 

"""
Common status codes: 
* 201 Created 
* 204 No Content (delete success without body)
* 400 Bad Request (client mistake) 
* 401 Unauthorized (not authenticated) 
* 403 Forbidden (authenticated but not allowed) 
* 404 Not Found 
* 4022 Unprocessable Entity (validation errors - FastAPI uses this a lot) 
* 500 Server Error (bug) 
"""

# Raising errors properly (HTTPException)
@app.get("/items/{item_id}")
def get_item(item_id: int): 
    if item_id != 1: 
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}

# Used for: Validated business logic, Throw HTTPException with meaningful details 

# Headers, cookies, and request object 
# Headers 
@app.get("/whoami")
def whoami(user_agent: str | None = Header(default=None)): 
    return {"user_agent": user_agent}

# Full request object 
@app.get("/debug") 
def debug(request: Request): 
    return {"url": str(request.url)}

# Dependency Injection  
"""
Dependencies are reusable "mini functions" that: 
* run before your endpoint 
* can return values injected into endpoint 
* can do auth, DB session creation, config, etc.
"""
def get_token(): 
    return "fake-token"

@app.get("/secure") 
def secure(token: str = Depends(get_token)): 
    return {"token": token}

"""
Why it matters 
It keeps your endpoints clean and testable 

Real uses: 
* database session per request 
* authentication/authorization 
* rate limiting (custom)
* feature flags 
* shared validation logic 
"""

# Async vs sync 
@app.get("/sync")
def sync_route(): 
    return {"ok": True}

@app.get("/async")
async def async_route(): 
    return {"ok": True}
"""
Use async when: 
* you call async libraries (async DB driver, async HTTP calls) 
* you want concurrency for I/O-bound tasks 

If blocking code is used inside async def (like normal requests / blocking DB calls), you lose benefits 

Rule: 
* If your stack is async end-to-end -> use async 
* If using classic SQLAlchemy sync engine -> sync endpoints are fine 
"""

# Background tasks (do work after response) 
def send_email(email: str): 
    # pretend to send 
    pass 

@app.post("/signup")
def signup(email:str, background: BackgroundTasks):
    background.add_task(send_email, email) 
    return {"message": "User created email sending..."}

# Middleware (request/response pipeline) 
"""
Middleware wraps every request 
Use cases: 
* logging 
* timing 
* CORS 
* authentication layers 
* response headers 

FastAPI uses Starlette middleware under the hood. 
"""

# CORS (imp for frontend + backend) 
# If React frontend hits FastAPI backend, CORS is needed

app.app_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8000'],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

