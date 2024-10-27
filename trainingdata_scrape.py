from pymongo import MongoClient
import random

# Storing the data in mongodb using pymongo
client = MongoClient('localhost', 27017)
db = client.grailed_data
collection = db.category_training_data

#creating a randomizer for training data with predefined generic categories and names

training_entries = 1000 #CHANGE THIS NUMBER TO HOW MANY ENTRIES NEEDED

# Define categories
categories = ['tops', 'bottoms', 'outerwear', 'footwear', 'accessories']

# Sample listing names for each category
tops_names = [
    "Graphic T-Shirt", "Cotton Polo", "Silk Blouse", "Chiffon Tank", "Linen Long Sleeve",
    "Flannel Shirt", "Hooded Sweatshirt", "Casual Button-Up", "Cropped Hoodie", "Knitted Sweater",
    "Denim Jacket", "Bandeau Top", "V-Neck T-Shirt", "Ribbed Tank Top", "Crew Neck Tee",
    "Puffer Vest", "Athletic Tank", "Plaid Shirt", "Wrap Top", "Off-Shoulder Blouse",
    "Turtleneck Sweater", "Cable Knit Sweater", "Fleece Pullover", "Camouflage Tee",
    "Embroidered Blouse", "Muscle Tee", "Oversized Sweater", "Sweater Dress", "Knit Tunic"
]

bottoms_names = [
    "Denim Jeans", "Chinos", "Cargo Pants", "Leggings", "Shorts",
    "Sweatpants", "Skirts", "Tailored Trousers", "Palazzo Pants", "Track Pants",
    "Skorts", "Bermuda Shorts", "Wide-Leg Pants", "Joggers", "Culottes",
    "Mini Skirt", "Maxi Skirt", "High-Waisted Jeans", "Capris", "Pleated Trousers",
    "Overalls", "Leather Pants", "Linen Trousers", "Formal Trousers", "Running Shorts",
    "Beach Shorts", "Printed Leggings", "Jogging Bottoms", "Sport Shorts", "Velvet Pants"
]

outerwear_names = [
    "Denim Jacket", "Leather Jacket", "Windbreaker", "Trench Coat", "Puffer Coat",
    "Peacoat", "Bomber Jacket", "Rain Jacket", "Cardigan", "Chore Coat",
    "Fleece Jacket", "Parka", "Lightweight Jacket", "Duster Coat", "Utility Jacket",
    "Biker Jacket", "Varsity Jacket", "Field Jacket", "Cape", "Overcoat",
    "Sports Coat", "Harrington Jacket", "Sherpa Jacket", "Anorak", "Faux Fur Coat",
    "Ski Jacket", "Hooded Coat", "Quilted Jacket", "Wool Coat", "Trucker Jacket"
]

footwear_names = [
    "Running Shoes", "Sneakers", "Loafers", "Sandals", "Boots",
    "High Heels", "Ankle Boots", "Flip Flops", "Ballet Flats", "Combat Boots",
    "Chelsea Boots", "Dress Shoes", "Slides", "Hiking Boots", "Wedges",
    "Athletic Sandals", "Platform Shoes", "Oxfords", "Espadrilles", "Clogs",
    "Slip-On Sneakers", "Gum Boots", "Water Shoes", "Knee-High Boots", "Moccasins",
    "Sock Sneakers", "Thigh-High Boots", "Mary Janes", "Trail Shoes", "Court Sneakers"
]

accessories_names = [
    "Sunglasses", "Baseball Cap", "Beanie", "Scarf", "Watch",
    "Belt", "Backpack", "Handbag", "Crossbody Bag", "Clutch",
    "Bracelet", "Necklace", "Earrings", "Headphones", "Hat",
    "Gloves", "Umbrella", "Wallet", "Keychain", "Brooch",
    "Hair Clip", "Anklet", "Sunglass Chain", "Hairband", "Tote Bag",
    "Fanny Pack", "Card Holder", "Cosmetic Bag", "Laptop Sleeve", "Beach Bag"
]

# Create training data

training_data = []

for _ in range(training_entries):
    category = random.choice(categories)  # Randomly select a category
    if category == 'tops':
        name = random.choice(tops_names)
    elif category == 'bottoms':
        name = random.choice(bottoms_names)
    elif category == 'outerwear':
        name = random.choice(outerwear_names)
    elif category == 'footwear':
        name = random.choice(footwear_names)
    elif category == 'accessories':
        name = random.choice(accessories_names)
    # Append the entry to the training_data list
    training_data.append({"name": name.lower(), "category": category.lower()})

rslt = collection.data.insert_many(training_data)

print(f"Inserted {len(rslt.inserted_ids)} training records into MongoDB.")

client.close()

