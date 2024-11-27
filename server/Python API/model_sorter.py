from transformers import pipeline # MIT License (MIT)
import json
import requests
import torch
print("CUDA available:", torch.cuda.is_available())
from bidi.algorithm import get_display # LGPL 3.0 license
from googletrans import Translator
# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
translator = Translator()
# Example shopping items
# Function to classify items with exception handling and translation
def classify_item(item, classifier, categories, translator):
    # Translate the item to English (if necessary)
    try:
        translated_item = translator.translate(item, dest='en').text
        print(f"Translated item: {get_display(translated_item)}")
    except Exception as e:
        print(f"Error translating item: {get_display(item)}")
        print(f"Error: {e}")
        return None

    # Otherwise, use the classifier with translated text
    result = classifier(translated_item, candidate_labels=categories)
    top_category = result["labels"][0]
    return top_category

def translate_text(text, target_lang='en'):
    # URL for the LibreTranslate API
    url = "https://libretranslate.com/translate"
    
    # Define the body of the POST request
    data = {
        'q': text,  # The text you want to translate
        'source': 'auto',  # Auto-detect the source language
        'target': target_lang,  # Target language (English in this case)
        'alternatives': 3 # Optional: Return 3 alternative translations (default is 1)\
    }
    
    # Set headers to indicate we're sending JSON data
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Make the POST request
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        
        # Parse the response JSON
        if response.status_code == 200:
            result = response.json()  # Get the translated text
            translated_text = result['translatedText']
            return translated_text
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
# Example shopping list
shopping_list_esp = [
    "חלב",  # Spanish for milk
    "בירה",  
    "לחם",  # Spanish for bread
    "צ'יפס", 
    "נוזל כביסה",  # Spanish for detergent
    " שמפו", 
    "dog food", 
    "לחמניות",  
    "משחת שיניים",
    "בשר טחון",  # hebrew for ground beef
    "גלידה", # hebrew for ice cream
    "קוטג'", # 
    "פרמז'ן",  # 
    "מוצרלה" 
]
shopping_list = [
    # Produce
    "apples", "bananas", "carrots", "spinach", "potatoes", "tomatoes", "cucumbers", "grapes", "peppers", "onions", "lettuce", "avocados", 

    # Dairy
    "milk", "cheese", "yogurt", "butter", "eggs", "cream", "ice cream", "sour cream", "cottage cheese", "mozzarella", "parmesan", 

    # Bakery
    "bread", "bagels", "croissants", "muffins", "cookies", "pastries", "pizza dough", "cakes", "tortillas", "buns", "donuts",

    # Meat
    "chicken", "beef", "pork chops", "lamb", "sausage", "turkey", "bacon", "steak", "ground beef", "chicken breasts", "roast beef", 

    # Seafood
    "salmon", "tuna", "shrimp", "crab", "lobster", "tilapia", "cod", "scallops", "sardines", "mussels", "fish sticks", 

    # Frozen Foods
    "frozen peas", "frozen corn", "frozen pizza", "ice cream", "frozen berries", "frozen fries", "frozen vegetables", "frozen waffles", "frozen chicken nuggets", 

    # Pantry
    "pasta", "rice", "canned beans", "canned tomatoes", "canned soup", "spaghetti", "flour", "sugar", "olive oil", "vinegar", "salt", "pepper", "cereal", "peanut butter", "honey", 

    # Snacks
    "chips", "cookies", "crackers", "granola bars", "nuts", "candy", "popcorn", "chocolate bars", "pretzels", "trail mix", "fruit snacks", 

    # Beverages
    "soda", "juice", "water", "coffee", "tea", "lemonade", "beer", "wine", "milk", "sports drinks", "iced tea", "seltzer", 

    # Health & Beauty
    "shampoo", "conditioner", "soap", "toothpaste", "toothbrush", "deodorant", "body wash", "razor", "lotion", "face wash", "makeup", "nail polish", "moisturizer", 

    # Baby Products
    "diapers", "baby wipes", "baby formula", "baby lotion", "baby shampoo", "pacifiers", "baby food", "baby clothes", 

    # Pet Supplies
    "dog food", "cat food", "dog treats", "cat litter", "pet toys", "pet grooming products", "pet shampoo", "dog leash", 

    # Pharmacy
    "pain relievers", "vitamins", "cough medicine", "band-aids", "allergy medicine", "toothache relief", "antiseptic", "cough drops", "medicated cream", "prescriptions", 

    # Spices & Seasonings
    "salt", "pepper", "oregano", "cumin", "chili powder", "garlic powder", "paprika", "bay leaves", "mustard", "hot sauce", "vinegar", 

    # Prepared Foods
    "pre-made salad", "rotisserie chicken", "deli sandwiches", "microwavable meals", "sushi", "frozen burritos", "pre-cooked bacon", "frozen breakfast sandwiches", 

    # Electronics
    "batteries", "light bulbs", "headphones", "phone charger", "laptop", "smartphone", "USB cables", "printer ink", "batteries", "flashlight", 

    # Laundry Supplies
    "detergent", "fabric softener", "stain remover", "dryer sheets", "laundry pods", "bleach", "washing powder", "ironing spray", 
]

# Categories to classify items into
categories = [
    "Produce products (fruits, vegetables, apples, bananas, carrots, leafy greens)",  # Fruits and vegetables
    "Dairy products (milk, cheese, yogurt, butter, eggs)",                          # Milk, cheese, yogurt, butter, eggs
    "Bakery products (bread, pastries, cakes, muffins, cookies)",                    # Bread, pastries, cakes, etc.
    "Meat products (beef, chicken, pork, lamb, sausages)",                           # Fresh and packaged meats
    "Seafood products (fish, shellfish, shrimp, lobster, crab)",                      # Fresh and frozen fish and shellfish
    "Frozen Foods products (frozen vegetables, ice cream, frozen meals, frozen fruit)",  # Frozen meals, vegetables, ice cream
    "Pantry products (canned goods, pasta, rice, beans, flour, sugar, spices)",       # Canned goods, pasta, rice, dry staples
    "Snacks products (chips, cookies, crackers, candy, nuts, granola bars)",          # Chips, cookies, crackers, etc.
    "Beverages products (soda, juice, bottled water, alcoholic drinks, tea, coffee)",  # Soda, juice, bottled water, alcoholic drinks
    "Health & Beauty products (shampoo, soap, deodorant, toothpaste, makeup, lotion)",  # Personal care products like shampoo, soap, makeup
    "Baby Products (baby food, diapers, wipes, baby formula, baby wipes)",  # Baby food, diapers, wipes, etc.
    "Pet Supplies products (dog food, cat food, pet toys)",  # Pet food, toys, grooming products
    "Pharmacy products (over-the-counter medicine, prescriptions, vitamins, pain relievers)",  # Over-the-counter medicine, prescriptions
    "Spices & Seasonings products (salt, pepper, herbs, mustard, hot sauce, ketchup)",  # Herbs, spices, condiments
    "Prepared Foods products (pre-made meals, deli items, rotisserie chicken, salads)",  # Deli items, pre-made salads, ready-to-eat food
    "Electronics products (batteries, small appliances, light bulbs, headphones, seasonal items)",  # Batteries, small appliances, seasonal items
    "Laundry Supplies products (detergents, fabric softeners, stain removers)"  # Detergents, fabric softeners, stain removers
]

# Classify each item
output = {}

# Classify each item and store results
for item in shopping_list_esp:
    category = classify_item(item, classifier, categories, translator)
    output[item] = category
    print(f"{get_display(item)} -> {category}")

# # Convert the output to JSON format
# output_json = json.dumps(output, indent=4)

# # Return or print the JSON output
# print(output_json)