# --- Pydantic Models (models.py) ---
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int = Field(ge=0)

# --- In-memory Database (database.py) ---
db_products = {
    1: Product(id=1, name="Laptop", price=1200.0, stock=50),
    2: Product(id=2, name="Keyboard", price=75.0, stock=100),
}

# --- Existing Endpoint (main.py) ---
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/api/v1/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = db_products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product