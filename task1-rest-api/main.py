from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

'''
2. The Optional Type Hint (Type Annotations):
If you are using type hints to document your code 
for static analyzers (like Mypy), 
Optional[X] indicates that a value can either be of 
    1- type X 
    2- or it can be None.
Case-1: Modern Python (3.10+): 
    - Use the cleaner pipe operator X | None.
Case-2: Older Python (3.9 and below): 
    - Import Optional from the built-in Python typing 
    documentation module.



  ```python Code Example:

  # Python 3.10+ (Recommended):
    def process_data(name: str | None = None) -> None:
        if name is None:
            print("No name provided")
        else:
            print(f"Processing {name}")

  # Python 3.9 and below:
    from typing import Optional
    def process_data_old(name: Optional[str] = None) -> None:
    ...

  ```

'''

# Step-1: creating an Instance of server
app = FastAPI(
    title = "DecodeLabs REST API — Project 1",
    description = "A stateless REST API serving structured JSON data.",
    version = "1.0.0",
)

# Step-2: creating an In-Memory Data: (list of Dictionaries)
products = [
    {"id": 1, "name": "Mechanical Keyboard", "price": 2999, "in_stock": True},
    {"id": 2, "name": "Monitor Stand", "price": 899,  "in_stock": True},
    {"id": 3, "name": "USB-C Hub", "price": 1499, "in_stock": False},
]

# Step-3: Defining a Pydantic Model for Product
class Product(BaseModel):
    name: str
    price: float
    #in_stock: bool | None = True  # Optional field with a default value of True
    in_stock: Optional[bool] = True  # Alternative using Optional

                    # Step-4: Creating API Endpoints

# Case-1: Checking health of server
@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Welcome to DecodeLabs REST API!",
        "project": "REST API Fundamentals — Project 1"
    }


# Case-2: Get all products
# defining the endpoint to get all products (GET /products)
@app.get("/products")
def get_all_products():
    return {
        "status" : "ok",
        "count" : len(products),
        "data": products 
    }
   

# Case-3: get a Single Product by ID
# GET /products/{id}
@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    # Search for the Product given it's ID
    #Case-1: Product Found
    for  product in products:
        if product["id"] == product_id:
            return {
                "status" : "success",
                "data" : product
            }
    # Case-2: Product Not Found
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")


# Case-4: Create a New Product (Inserting into the in-memory list)
# Upon Successful Creation, return the newly created product with a 201 status code
@app.post("/products" , status_code=201)
def create_product(product: Product):
    # Generate a new unique ID for the new product
    new_id = max(p["id"] for p in products) + 1
    # creates the new product dictionary from the Pydantic model
    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "in_stock": product.in_stock    
    }
    # Add the new product to the in-memory list
    products.append(new_product)
    return {
        "status": "success",
        "message": f"Product '{product.name}' created successfully",
        "data": new_product
    }
