from scraper import scrape_by_name
from database import save_product, get_product_with_ingredients
from scorer import score_product

product_name = input("Enter product name: ")

print("\nScraping...")
result = scrape_by_name(product_name)

if "error" in result:
    print(f"Error: {result['error']}")
else:
    print(f"Found: {result['name']}")
    print(f"Ingredients: {len(result['ingredients'])} found")

    print("\nSaving...")
    product_id = save_product(result)

    print("\nFetching from storage...")
    saved = get_product_with_ingredients(product_id)

    ingredient_names = [ing for ing in saved["ingredients"]]  # already a list of strings
    score = score_product(ingredient_names)

    print(f"Name    : {saved['name']}")
    print(f"Brand   : {saved['brand']}")
    print(f"Saved at: {saved['scraped_at']}")
    print(f"\nIngredients:")
    for ing in saved['ingredients']:
        print(f"  - {ing}")
    print(f"Score   : {score['overall_score']}/100  Grade: {score['grade']}")