import json 
import os
from datetime import datetime

CACHE_FILE="products_cache.json"

def load_cache() -> dict:
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE,"r") as f:
        return json.load(f)

def save_product(product: dict) -> int:
    cache=load_cache()

    key=product["name"].lower().strip()

    if key in cache:
        print("Already in cache. Skipping.")
        return cache[key]["id"]
    
    product_id=len(cache)+1
    cache[key]={
        "id": product_id,
        "name": product["name"],
        "brand": product["brand"],
        "url": product["url"],
        "ingredients": product.get("ingredients", []),
        "ingredients_raw": product.get("ingredients_raw", ""),
        "scraped_at": str(datetime.now())
    }

    with open(CACHE_FILE,"w") as f:
        json.dump(cache,f,indent=2)

    print(f"Saved to cache with ID: {product_id}")
    return product_id

def get_product_with_ingredients(product_id: int) -> dict:
    cache=load_cache()

    for key,product in cache.items():
        if product["id"]==product_id:
            return product
        
    return {"error":"Product not found"}

def create_tables():
    print("Using JSON file cache")