import re

HARMFUL = {
    "red 40", "allura red", "sunset yellow", "tartrazine",
    "brilliant blue", "sodium benzoate", "potassium sorbate",
    "bha", "bht", "tbhq", "sodium nitrite", "sodium nitrate",
    "aspartame", "saccharin", "sucralose", "acesulfame",
    "high fructose corn syrup", "hfcs", "monosodium glutamate",
    "msg", "disodium inosinate", "disodium guanylate",
    "carrageenan", "partially hydrogenated",
    "hydrogenated vegetable oil", "potassium bromate",
}

CAUTION = {
    "maltodextrin", "modified starch", "corn syrup", "soy lecithin",
    "canola oil", "palm oil", "natural flavour", "natural flavor",
    "artificial flavor", "caramel color", "caramel colour",
    "sodium phosphate", "carnauba wax", "shellac",
}

SAFE = {
    "water", "salt", "wheat", "rice", "oat", "milk", "egg",
    "flour", "oil", "butter", "cream", "cheese", "spice",
    "turmeric", "pepper", "cumin", "coriander", "cardamom",
    "onion", "garlic", "tomato", "ginger", "vinegar",
}

SUGAR_TERMS = ["sugar", "syrup", "dextrose", "fructose", "glucose", "sucrose", "lactose"]

GRADES = [
    (85, "A", "Very safe — minimal concerns"),
    (70, "B", "Mostly safe — a few ingredients to watch"),
    (50, "C", "Moderate concern — consume occasionally"),
    (30, "D", "High concern — several harmful ingredients"),
    (0,  "F", "Avoid — multiple harmful ingredients found"),
]


def score_ingredient(name: str) -> dict:
    lower = name.lower().strip()

    for h in HARMFUL:
        if h in lower:
            return {"name": name, "flag": "red", "reason": f"'{h}' — linked to health concerns"}

    for c in CAUTION:
        if c in lower:
            return {"name": name, "flag": "yellow", "reason": f"'{c}' — consume in moderation"}

    if re.search(r'\be[1-9]\d{2,3}\b', lower):
        return {"name": name, "flag": "yellow", "reason": "E-number additive — check before consuming"}

    for s in SUGAR_TERMS:
        if s in lower:
            return {"name": name, "flag": "yellow", "reason": "Added sugar — limit intake"}

    for s in SAFE:
        if s in lower:
            return {"name": name, "flag": "green", "reason": "Common natural ingredient"}

    return {"name": name, "flag": "unknown", "reason": "Not in our database yet"}


def score_product(ingredients: list) -> dict:
    if not ingredients:
        return {
            "total_ingredients": 0, "red_count": 0, "yellow_count": 0,
            "green_count": 0, "unknown_count": 0, "overall_score": 0,
            "grade": "N/A", "verdict": "No ingredients found", "scored_ingredients": [],
        }

    scored  = [score_ingredient(i) for i in ingredients]
    counts  = {f: sum(1 for s in scored if s["flag"] == f) for f in ("red", "yellow", "green", "unknown")}
    penalty = counts["red"] * 10 + counts["yellow"] * 4 + counts["unknown"] * 1
    score   = max(0, 100 - penalty)
    grade, verdict = next((g, v) for threshold, g, v in GRADES if score >= threshold)

    return {
        "total_ingredients": len(scored),
        "red_count":         counts["red"],
        "yellow_count":      counts["yellow"],
        "green_count":       counts["green"],
        "unknown_count":     counts["unknown"],
        "overall_score":     score,
        "grade":             grade,
        "verdict":           verdict,
        "scored_ingredients": scored,
    }


if __name__ == "__main__":
    test = ["Wheat Flour", "Salt", "MSG", "Tartrazine", "Palm Oil", "Sugar", "E102"]
    r = score_product(test)
    print(f"Score: {r['overall_score']}/100  Grade: {r['grade']}  — {r['verdict']}")
    for s in r["scored_ingredients"]:
        icon = {"red": "RED", "yellow": "YLW", "green": "GRN", "unknown": "???"}[s["flag"]]
        print(f"  [{icon}] {s['name']} — {s['reason']}")