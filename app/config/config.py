from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    OFF_SEARCH_URL  = os.getenv("OFF_SEARCH_URL",  "https://world.openfoodfacts.org/cgi/search.pl")
    OFF_PRODUCT_URL = os.getenv("OFF_PRODUCT_URL", "https://world.openfoodfacts.org/api/v0/product")
    OFF_BASE_URL    = os.getenv("OFF_BASE_URL",     "https://world.openfoodfacts.org/product")
