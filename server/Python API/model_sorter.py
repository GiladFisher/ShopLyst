from transformers import pipeline
# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Example shopping items
shopping_list = [
    "apples",
    "milk",
    "bread",
    "chicken",
    "detergent",
    "chips",
    "shampoo",
    "dog food",
]

# Categories to classify items into
categories = [
    "Produce (fruits, vegetables, apples, bananas, carrots, leafy greens)",  # Fruits and vegetables
    "Dairy (milk, cheese, yogurt, butter, eggs)",                          # Milk, cheese, yogurt, butter, eggs
    "Bakery (bread, pastries, cakes, muffins, cookies)",                    # Bread, pastries, cakes, etc.
    "Meat (beef, chicken, pork, lamb, sausages)",                           # Fresh and packaged meats
    "Seafood (fish, shellfish, shrimp, lobster, crab)",                      # Fresh and frozen fish and shellfish
    "Frozen Foods (frozen vegetables, ice cream, frozen meals, frozen fruit)",  # Frozen meals, vegetables, ice cream
    "Pantry (canned goods, pasta, rice, beans, flour, sugar, spices)",       # Canned goods, pasta, rice, dry staples
    "Snacks (chips, cookies, crackers, candy, nuts, granola bars)",          # Chips, cookies, crackers, etc.
    "Beverages (soda, juice, milk, bottled water, alcoholic drinks, tea, coffee)",  # Soda, juice, bottled water, alcoholic drinks
    "Health & Beauty (shampoo, soap, deodorant, toothpaste, makeup, lotion)",  # Personal care products like shampoo, soap, makeup
    "Baby Products (baby food, diapers, wipes, baby formula, baby wipes)",  # Baby food, diapers, wipes, etc.
    "Pet Supplies (dog food, cat food, pet toys, pet grooming products, pet medications)",  # Pet food, toys, grooming products
    "Pharmacy (over-the-counter medicine, prescriptions, vitamins, pain relievers)",  # Over-the-counter medicine, prescriptions
    "Spices & Seasonings (salt, pepper, herbs, mustard, hot sauce, ketchup)",  # Herbs, spices, condiments
    "Prepared Foods (pre-made meals, deli items, rotisserie chicken, salads)",  # Deli items, pre-made salads, ready-to-eat food
    "Electronics (batteries, small appliances, light bulbs, headphones, seasonal items)",  # Batteries, small appliances, seasonal items
    "Laundry Supplies (detergents, fabric softeners, stain removers, dryer sheets, washing pods)",  # Laundry detergents, fabric softeners
]
# Classify each item
for item in shopping_list:
    result = classifier(item, candidate_labels=categories)
    print(f"{item}: {result['labels'][0]} (confidence: {result['scores'][0]:.2f})")