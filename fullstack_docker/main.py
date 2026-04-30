from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Returns all items
@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

# Returns single item by id or 404 if not found
@app.get("/items/{id}")
def read_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Create a new item from JSON body
@app.post("/items/", status_code=201)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Update an existing item
@app.put("/items/{id}")
def update_item(id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

 # Delete an item
@app.delete("/items/{id}")
def delete_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}

# Serve frontend at root after all API routes
app.mount("/", StaticFiles(directory="static", html=True), name="static")
@app.delete("/items/{id}")
def delete_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}

# Run with: uvicorn main:app --reload
