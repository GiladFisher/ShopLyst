from transformers import pipeline # MIT License (MIT)
import json
from flask_cors import cross_origin
from flask import Flask, request, jsonify
from flask_caching import Cache
import torch
import os
import firebase_admin
from firebase_admin import credentials, db
from sentence_transformers import SentenceTransformer, util
print(torch.cuda.is_available())
device = torch.device('cuda')
# print("CUDA available:", torch.cuda.is_available())
from bidi.algorithm import get_display # LGPL 3.0 license
from googletrans import Translator
# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=-1)
translator = Translator()
# Example shopping items
app = Flask(__name__)

cred = credentials.Certificate("C:/Users/gilad/Documents/GitHub/ShopLyst/server/Python API/shoplyst-584c0-firebase-adminsdk-4ht66-158f67ab1c.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://shoplyst-584c0-default-rtdb.europe-west1.firebasedatabase.app/"
})

# Setup Flask-Caching to use a file-based cache
app.config['CACHE_TYPE'] = 'filesystem'
app.config['CACHE_DIR'] = os.path.join(os.getcwd(), '/data/flask_cache')  # Directory where cache files will be stored
cache = Cache(app)





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
    "Fruits & Vegetables products (onions, apples, potatos, banana, )",  # Fruits and vegetables "#
    "Dairy products (milk, cheese, yogurt, butter, eggs, gauda, parmesan, cotage)",                          # Milk, cheese, yogurt, butter, eggs
    "Bakery products (bread, pastries, cakes, muffins, cookies, buns, pitahs, flatbread)",                    # Bread, pastries, cakes, etc.
    "Meat products (beef, chicken, pork, lamb, sausages)",                           # Fresh and packaged meats
    "Seafood products (fish, shellfish, shrimp, lobster, crab, salmon)",                      # Fresh and frozen fish and shellfish
    "Frozen Foods products (frozen vegetables, ice cream, frozen meals, frozen fruit)",  # Frozen meals, vegetables, ice cream
    "Pantry products (canned goods, pasta, rice, beans, flour, sugar)",       # Canned goods, pasta, rice, dry staples
    "Snacks products (chips, cookies, crackers, candy, nuts, granola bars)",          # Chips, cookies, crackers, etc.
    "Beverages products (soda, juice, bottled water, alcoholic drinks, tea, coffee)",  # Soda, juice, bottled water, alcoholic drinks
    "Health & Beauty products (shampoo, soap, deodorant, toothpaste, makeup, lotion)",  # Personal care products like shampoo, soap, makeup
    "Baby Products (baby food, diapers, wipes, baby formula, baby wipes)",  # Baby food, diapers, wipes, etc.
    "Pet Supplies products (dog food, cat food, pet toys)",  # Pet food, toys, grooming products
    "Pharmacy products (over-the-counter medicine, prescriptions, vitamins, pain relievers, sunscreen)",  # Over-the-counter medicine, prescriptions
    "Spices & Seasonings products (salt, pepper, herbs, paprika)",  # Herbs, spices, condiments
    #"Prepared Foods products (pre-made meals, deli items, rotisserie chicken, salads)",  # Deli items, pre-made salads, ready-to-eat food
    "Electronics products (batteries, small appliances, light bulbs, headphones, heater)",  # Batteries, small appliances, seasonal items
    "Laundry Supplies products (detergents, fabric softeners, stain removers)"  # Detergents, fabric softeners, stain removers
]

# Classify each item
output = {}

@app.route("/classify", methods=["POST"])
@cross_origin()  # Enable CORS for this route only
def classify():
    data = request.json
    title = data.get("title", "")
    if not title:
        return jsonify({"error": "Title is missing"}), 400
    print(f"Original title recieved: {get_display(title)}")
    # Check if the title is cached

    # cached_result = cache.get(title)
    # if cached_result:
    #     print(f"Cache hit for: {title}")
    #     # Increment hit count
    #     cached_result['hit_count'] += 1
    #     cache.set(title, cached_result)  # Update the cache with the new hit count
    #     category = cached_result['category']

    # Check if the title exists in Firebase
    ref = db.reference(f"cache/{title}")
    cached_result = ref.get()

    if cached_result:
        print(f"Cache hit for: {title}")
        # Increment hit count
        cached_result['hit_count'] += 1
        ref.set(cached_result)  # Update the cache with the new hit count
        category = cached_result['category']
    
    else:
        category = classify_item(title, classifier, categories, translator)
        # cache.set(title, {'category': category, 'hit_count': 1})
        cache_data = {'category': category, 'hit_count': 1}
        ref.set(cache_data)
        print(f"Cache set for: {get_display(title)} -> {category}")

    return jsonify({"category": category})

 
# 
if __name__ == "__main__":
    if not os.path.exists('/data/flask_cache'):
        os.makedirs('/data/flask_cache')
    app.run(debug=True)



# # Classify each item and store results
# for item in shopping_list_esp:
#     category = classify_item(item, classifier, categories, translator)
#     output[item] = category
#     print(f"{get_display(item)} -> {category}")

# # Convert the output to JSON format
# output_json = json.dumps(output, indent=4)

# # Return or print the JSON output
# print(output_json)