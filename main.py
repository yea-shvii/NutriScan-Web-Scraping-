from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_by_name, scrape_product
from scorer import score_product
from database import save_product, get_product_with_ingredients

app = FastAPI(
    title="NutriScan API",
    description="Scan packaged food products and check ingredient safety",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "NutriScan API is running",
        "endpoints": {
            "scan_by_name": "/scan?product=lays classic chips",
            "scan_by_url":  "/scan/url?url=https://world.openfoodfacts.org/product/123456",
            "get_product":  "/product/1",
            "history":      "/history",
            "docs":         "/docs"
        }
    }


def _build_response(scraped: dict, product_id: int | None = None) -> dict:
    """Shared helper — scores a scraped product and builds the response dict."""
    score = score_product(scraped.get("ingredients", []))
    response = {
        "product":  scraped["name"],
        "brand":    scraped["brand"],
        "url":      scraped["url"],
        "score":    score["overall_score"],
        "grade":    score["grade"],
        "verdict":  score["verdict"],
        "summary": {
            "total":   score["total_ingredients"],
            "red":     score["red_count"],
            "yellow":  score["yellow_count"],
            "green":   score["green_count"],
            "unknown": score["unknown_count"],
        },
        "ingredients": score["scored_ingredients"],
    }
    if product_id is not None:
        response["db_id"] = product_id
    return response


@app.get("/scan")
def scan_product(product: str = Query(..., min_length=2, description="Product name to search")):
    """
    Search, score and cache a product by name.
    Example: GET /scan?product=lays classic chips
    """
    # Step 1 — scrape
    scraped = scrape_by_name(product)
    if "error" in scraped:
        raise HTTPException(status_code=404, detail=scraped["error"])

    # Step 2 — save to cache (best-effort)
    product_id = None
    try:
        product_id = save_product(scraped)
    except Exception as e:
        print(f"[warn] Cache save failed: {e}")

    # Step 3 — score + return
    return _build_response(scraped, product_id)


@app.get("/scan/url")
def scan_product_by_url(url: str = Query(..., description="Open Food Facts product URL")):
    """
    Scan a product directly by its Open Food Facts URL.
    Example: GET /scan/url?url=https://world.openfoodfacts.org/product/8901491504951
    """
    if "openfoodfacts.org" not in url:
        raise HTTPException(
            status_code=400,
            detail="Only Open Food Facts URLs are supported (world.openfoodfacts.org)"
        )

    # Step 1 — scrape
    scraped = scrape_product(url)
    if "error" in scraped:
        raise HTTPException(status_code=404, detail=scraped["error"])

    # Step 2 — save to cache (best-effort)
    product_id = None
    try:
        product_id = save_product(scraped)
    except Exception as e:
        print(f"[warn] Cache save failed: {e}")

    # Step 3 — score + return
    return _build_response(scraped, product_id)


@app.get("/product/{product_id}")
def get_product(product_id: int):
    """
    Fetch and re-score a previously scanned product from cache.
    Example: GET /product/1
    """
    result = get_product_with_ingredients(product_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    score = score_product(result.get("ingredients", []))

    return {
        "product":    result["name"],
        "brand":      result["brand"],
        "url":        result["url"],
        "scraped_at": result["scraped_at"],
        "score":      score["overall_score"],
        "grade":      score["grade"],
        "verdict":    score["verdict"],
        "summary": {
            "total":   score["total_ingredients"],
            "red":     score["red_count"],
            "yellow":  score["yellow_count"],
            "green":   score["green_count"],
            "unknown": score["unknown_count"],
        },
        "ingredients": score["scored_ingredients"],
    }


@app.get("/history")
def get_history():
    """
    Return all previously scanned products from cache.
    Example: GET /history
    """
    import json
    import os

    cache_file = "products_cache.json"

    if not os.path.exists(cache_file):
        return {"products": [], "total": 0}

    with open(cache_file, "r") as f:
        cache = json.load(f)

    products = [
        {
            "id":         p["id"],
            "name":       p["name"],
            "brand":      p["brand"],
            "scraped_at": p["scraped_at"],
        }
        for p in cache.values()
    ]

    # Sort by id so newest additions appear last
    products.sort(key=lambda x: x["id"])

    return {"products": products, "total": len(products)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)