# NutriScan 

## Overview

NutriScan is a FastAPI-based food product analysis service that helps users evaluate packaged food products based on their ingredients.

The application searches products from Open Food Facts, extracts ingredient information, analyzes ingredient quality using a custom scoring engine, and returns an easy-to-understand health score and verdict.

Additionally, scanned products are cached locally, allowing users to retrieve previously analyzed products without performing another lookup.

---

## Features

* Search food products by name
* Analyze products using Open Food Facts URLs
* Ingredient extraction and normalization
* Ingredient safety scoring engine
* Product grading system
* Health verdict generation
* Local product caching
* Product scan history
* REST API built with FastAPI
* Interactive Swagger API documentation

---

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn

### Data Retrieval

* Requests
* Open Food Facts

### Data Processing

* JSON
* Regular Expressions

### Storage

* Local JSON Cache

### API Documentation

* Swagger UI
* OpenAPI

---

## How It Works

```text
User Input
      │
      ▼
Product Search
(Open Food Facts)
      │
      ▼
Ingredient Extraction
      │
      ▼
Ingredient Scoring Engine
      │
      ▼
Grade & Verdict Generation
      │
      ▼
Cache Storage
      │
      ▼
API Response
```

---

## Scoring System

NutriScan evaluates ingredients using predefined ingredient classifications.

### Green Ingredients

Generally considered beneficial or safe:

* Whole Grains
* Oats
* Natural Spices
* Nuts
* Seeds

### Yellow Ingredients

Ingredients that should be consumed in moderation:

* Refined Flour
* Added Sugar
* Flavor Enhancers

### Red Ingredients

Ingredients considered highly processed or undesirable:

* Artificial Colors
* Artificial Flavors
* Preservatives
* Excessive Sweeteners
* Certain Additives

The final score is calculated based on the overall ingredient composition.

---

## API Endpoints

### Health Check

Returns API status and available endpoints.

```http
GET /
```

Example Response:

```json
{
  "message": "NutriScan API is running"
}
```

---

### Scan Product By Name

Searches Open Food Facts, extracts ingredients, scores the product, and stores it in cache.

```http
GET /scan?product=lays classic chips
```

Example:

```http
GET /scan?product=maggi masala noodles
```

Example Response:

```json
{
  "product": "Maggi Masala Noodles",
  "brand": "Nestle",
  "url": "https://world.openfoodfacts.org/product/8901058005240",
  "score": 72,
  "grade": "B",
  "verdict": "Moderately Processed",
  "summary": {
    "total": 12,
    "red": 2,
    "yellow": 3,
    "green": 5,
    "unknown": 2
  },
  "ingredients": []
}
```

---

### Scan Product By URL

Analyze a product directly using an Open Food Facts product URL.

```http
GET /scan/url?url=<product_url>
```

Example:

```http
GET /scan/url?url=https://world.openfoodfacts.org/product/8901491504951
```

Returns the same response structure as `/scan`.

---

### Retrieve Cached Product

Fetches a previously analyzed product from local cache.

```http
GET /product/{product_id}
```

Example:

```http
GET /product/1
```

Example Response:

```json
{
  "product": "Maggi Masala Noodles",
  "brand": "Nestle",
  "url": "https://world.openfoodfacts.org/product/8901058005240",
  "scraped_at": "2026-05-30T10:15:22",
  "score": 72,
  "grade": "B",
  "verdict": "Moderately Processed",
  "ingredients": []
}
```

---

### Scan History

Returns all products stored in cache.

```http
GET /history
```

Example Response:

```json
{
  "products": [
    {
      "id": 1,
      "name": "Maggi Masala Noodles",
      "brand": "Nestle",
      "scraped_at": "2026-05-30T10:15:22"
    }
  ],
  "total": 1
}
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/nutriscan-api.git

cd nutriscan-api
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running The Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## Project Structure

```text
nutriscan-api/
│
├── app/
│   ├── utils/
│   │   ├── scraper.py
│   │   ├── scorer.py
│   │   └── database.py
│
├── main.py
├── requirements.txt
├── products_cache.json
├── .gitignore
├── README.md
└── .env
```

---

## Example Use Cases

* Food product evaluation
* Consumer awareness tools
* Ingredient transparency platforms
* Health-tech applications
* Nutrition-focused APIs
* Product comparison systems

---

## Future Improvements

* Nutrition label analysis
* Multiple food data providers
* Ingredient risk classification
* Product comparison endpoint
* User authentication
* Dashboard UI
* AI-powered ingredient recommendations

---


## License

This project is intended for educational, learning, and portfolio purposes.
