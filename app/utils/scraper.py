import httpx
import re
from config import Config

def parse_ingredients(raw: str) -> list[str]:
    if not raw:
        return []

    text = raw.replace("&amp;", "&").replace("&nbsp;", " ")

    # remove markdown-style emphasis
    text = re.sub(r'[_*]+([^_*]+)[_*]+', r'\1', text)

    # remove nested brackets/parentheses
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r'[\(\[][^\(\)\[\]]*[\)\]]', '', text)

    # normalize separators
    text = re.sub(r'[;|/]', ',', text)

    cleaned = []

    for part in text.split(','):

        # trim punctuation/spaces
        part = re.sub(r'^[\s\-:\.]+|[\s\-:\.]+$', '', part)

        # remove percentages like 13%, 7.4%, 6 %
        part = re.sub(r'\b\d+(\.\d+)?\s*%', '', part)

        # remove standalone quantities only if entire string is numeric
        if re.fullmatch(r'\d+(\.\d+)?', part.strip()):
            continue

        # cleanup
        part = re.sub(r'[\s\(\)\[\]\.:]+$', '', part).strip()

        # skip tiny junk values
        if len(part) < 2:
            continue

        cleaned.append(part)

    # remove duplicates while preserving order
    seen = set()
    result = []

    for item in cleaned:
        key = item.lower()

        if key not in seen:
            seen.add(key)
            result.append(item)

    return result

def scrape_by_name(product_name: str) -> dict:
    print(f"Searching for: {product_name}")

    response=httpx.get(
        Config.OFF_SEARCH_URL,
        params={
            "search_terms":product_name,
            "search_simple":1,
            "action":"process",
            "json":1,
            "page_size":1,
            "lc":"en",

        },
        timeout=15,
        
    )
    print(response.status_code)
    print(response.text[:500])
    data=response.json()
    products=data.get("products",[])

    if not products:
        return {"error": f"No product found for '{product_name}'"}
    
    p=products[0]

    ingredients_raw=p.get("ingredients_text","") or ""
    ingredients_list = parse_ingredients(ingredients_raw)

    return{
        "name":p.get("product_name","Unknown"),
        "brand":p.get("brands","Unknown"),
        "url":f"{Config.OFF_BASE_URL}/{p.get('code')}",
        "ingredients":ingredients_list,
        "ingredients_raw":ingredients_raw
    }

def scrape_product(url: str) -> dict:
    code=url.rstrip("/").split("/")[-1]

    response=httpx.get(
        f"{Config.OFF_PRODUCT_URL}/{code}.json",
        timeout=15
    )

    data=response.json()
    if data.get("status")!=1:
        return{"error":"Product not found"}
    
    p=data["product"]
    ingredients_raw=p.get("ingredients_text","") or ""
    ingredients_list = parse_ingredients(ingredients_raw)

    return{
        "name": p.get("product_name", "Unknown"),
        "brand": p.get("brands", "Unknown"),
        "url": url,
        "ingredients": ingredients_list,
        "ingredients_raw": ingredients_raw,
    }

if __name__ == "__main__":
    result = scrape_by_name(input("Enter product name: "))

    print("\n========== RESULT ==========")
    print(f"Product : {result.get('name')}")
    print(f"Brand   : {result.get('brand')}")
    print(f"URL     : {result.get('url')}")
    print(f"\nIngredients ({len(result.get('ingredients', []))} found):")
    for i, ing in enumerate(result.get("ingredients", []), 1):
        print(f"  {i}. {ing}")

    if result.get("error"):
        print(f"Error: {result['error']}")