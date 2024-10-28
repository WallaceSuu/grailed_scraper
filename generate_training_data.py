from pymongo import MongoClient
import random

# Storing the data in mongodb using pymongo
client = MongoClient('localhost', 27017)
db = client.grailed_data
collection = db.category_training_data

#creating a randomizer for training data with predefined generic categories and names

training_entries = 400 #CHANGE THIS NUMBER TO HOW MANY ENTRIES NEEDED

# Define categories
categories = ['tops', 'bottoms', 'outerwear', 'footwear', 'accessories']

# Sample listing names for each category
tops_names = [
    "Graphic T-Shirt", "Cotton Polo", "Silk Blouse", "Chiffon Tank", "Linen Long Sleeve",
    "Flannel Shirt", "Hooded Sweatshirt", "Casual Button-Up", "Cropped Hoodie", "Knitted Sweater",
    "Denim Jacket", "Bandeau Top", "V-Neck T-Shirt", "Ribbed Tank Top", "Crew Neck Tee",
    "Puffer Vest", "Athletic Tank", "Plaid Shirt", "Wrap Top", "Off-Shoulder Blouse",
    "Turtleneck Sweater", "Cable Knit Sweater", "Fleece Pullover", "Camouflage Tee",
    "Embroidered Blouse", "Muscle Tee", "Oversized Sweater", "Sweater Dress", "Knit Tunic",
    "Lace Camisole", "Graphic Hoodie", "Polo Shirt", "Mesh Tank Top", "Sleeveless Blouse",
    "Button-Down Shirt", "Cotton Sweater", "Ribbed Cardigan", "Knit T-Shirt", "Belted Blouse",
    "Long Sleeve Tee", "Stretch Tank", "Bamboo Top", "Mock Neck Sweater", "Boho Tunic",
    "Graphic Crop Top", "Fitted Bodysuit", "Plaid Flannel", "Lightweight Pullover", "Thermal Top",
    "Vibrant Sweater", "Racerback Tank", "Vintage Tee", "Sheer Blouse", "Peplum Top",
    "Chunky Knit Sweater", "Cowl Neck Sweater", "Tie-Dye Tee", "Ruffled Tank", "Asymmetrical Top",
    "Bell Sleeve Blouse", "Off-Shoulder Sweatshirt", "Graphic Long Sleeve", "Breezy Tank",
    "Color Block Sweater", "Sleeveless Hoodie", "Pleated Blouse", "Sporty Tank", "Strappy Camisole", "Casual Henley",
    "Graphic Crew Neck", "Luxe Knit Top", "Classic Sweatshirt", "Frill Sleeve Top", "Tie Front Tee",
    "Satin Blouse", "Ruffled Sweater", "Chunky Cardigan", "Fitted Long Sleeve", "Vintage Graphic Tee",
    "Waffle Knit Top", "Puff Sleeve Blouse", "Drop Shoulder Sweater", "Silk Cami", "Kimono Sleeve Top",
    "Boat Neck Tee", "Scoop Neck Tank", "Textured Sweater", "Linen Wrap Top", "Embroidered Tank",
    "Rugby Shirt", "Crossover Top", "Layered Blouse", "Flare Sleeve Sweater", "Cold Shoulder Top",
    "Pocket Tee", "Gathered Tunic", "Padded Shoulder Top", "Colorful Raglan", "Bodysuit with Ruffles"
]

bottoms_names = [
    "Denim Jeans", "Chinos", "Cargo Pants", "Leggings", "Shorts",
    "Sweatpants", "Skirts", "Tailored Trousers", "Palazzo Pants", "Track Pants",
    "Skorts", "Bermuda Shorts", "Wide-Leg Pants", "Joggers", "Culottes",
    "Mini Skirt", "Maxi Skirt", "High-Waisted Jeans", "Capris", "Pleated Trousers",
    "Overalls", "Leather Pants", "Linen Trousers", "Formal Trousers", "Running Shorts",
    "Beach Shorts", "Printed Leggings", "Jogging Bottoms", "Sport Shorts", "Velvet Pants",
    "Track Shorts", "Cargo Shorts", "Fitted Skirt", "Biker Shorts", "Drawstring Pants",
    "Wide-Leg Culottes", "Leather Leggings", "Chino Shorts", "Skirted Leggings", "Sweat Shorts",
    "Seamless Leggings", "Tapered Pants", "Knitted Joggers", "Pleated Skirt", "Paperbag Trousers",
    "High-Waisted Shorts", "Straight Leg Jeans", "Slouchy Pants", "Capri Leggings", "Flare Jeans",
    "Athletic Capris", "Cuffed Pants", "Wide-Leg Shorts", "Tailored Shorts", "Linen Culottes",
    "Button-Fly Jeans", "Straight Cut Trousers", "Skorts with Pockets", "Fit and Flare Skirt",
    "Floral Print Leggings", "Bamboo Joggers",  "Pleather Leggings", "Wide-Leg Culottes", "Distressed Jeans", "Chino Trousers", "Drawstring Shorts",
    "A-Line Skirt", "Leather Midi Skirt", "Pleated Wide-Leg Pants", "High-Waisted Trousers", "Knit Joggers",
    "Slouchy Shorts", "Tailored Shorts", "Fitted Cargo Pants", "Printed Culottes", "Soft Jogging Pants",
    "Relaxed Fit Jeans", "Knitted Midi Skirt", "Palazzo Culottes", "Fleece Joggers", "Seamless Shorts",
    "Skater Skirt", "Printed Shorts", "Flannel Joggers", "Corduroy Trousers", "Sporty Capris",
    "Luxe Wide-Leg Pants", "Relaxed Fit Chinos", "Belted Cargo Shorts", "Stretchy Jeggings", "Elegant Pencil Skirt",
    "Utility Shorts", "Rugged Work Pants", "Luxe Tailored Trousers", "Layered Midi Skirt"
]

outerwear_names = [
    "Denim Jacket", "Leather Jacket", "Windbreaker", "Trench Coat", "Puffer Coat",
    "Peacoat", "Bomber Jacket", "Rain Jacket", "Cardigan", "Chore Coat",
    "Fleece Jacket", "Parka", "Lightweight Jacket", "Duster Coat", "Utility Jacket",
    "Biker Jacket", "Varsity Jacket", "Field Jacket", "Cape", "Overcoat",
    "Sports Coat", "Harrington Jacket", "Sherpa Jacket", "Anorak", "Faux Fur Coat",
    "Ski Jacket", "Hooded Coat", "Quilted Jacket", "Wool Coat", "Trucker Jacket",
    "Belted Trench", "Hooded Windbreaker", "Insulated Jacket", "Chalk Stripe Blazer", "Utility Vest",
    "Fringe Jacket", "Heavyweight Coat", "Quilted Vest", "Sporty Windbreaker", "Over-Sized Parka",
    "Faux Leather Biker", "Stylish Kimono", "Waterproof Raincoat", "Longline Cardigan", "Shearling Coat",
    "Checkered Overshirt", "Classic Peacoat", "Graphic Anorak", "Fleece-Lined Jacket", "Patched Denim Jacket",
    "Sleek Bomber", "Double-Breasted Coat", "Short Puffer", "Canvas Jacket", "M-65 Field Jacket",
    "Puff Sleeve Coat", "Modern Duster", "Long Quilted Jacket", "Chore Jacket", "Vintage Denim Coat",
    "Padded Vest", "Sherpa Fleece Jacket", "Belted Overcoat", "Double-Layered Jacket", "Classic Trench",
    "Chalk Stripe Coat", "Shearling Jacket", "Teddy Coat", "Layered Windbreaker", "Hooded Fleece Coat",
    "Utility Shirt Jacket", "Long Cardigan Coat", "Retro Windbreaker", "Asymmetric Duster", "Heavyweight Parka",
    "Classic Blazer", "Cropped Puffer", "Water-Resistant Jacket", "Stylish Anorak", "Comfy Cardigan",
    "Luxe Faux Fur Coat", "Military Jacket", "Longline Blazer", "Casual Denim Jacket", "Wool Blend Coat",
    "Graphic Rain Jacket", "Vintage Bomber", "Classic Fleece", "Warm Puffer Jacket", "Oversized Wool Coat",
    "Lightweight Down Jacket", "Corduroy Overshirt", "Modern Utility Coat", "Puff-Sleeve Overcoat"
]

footwear_names = [
    "Running Shoes", "Sneakers", "Loafers", "Sandals", "Boots",
    "High Heels", "Ankle Boots", "Flip Flops", "Ballet Flats", "Combat Boots",
    "Chelsea Boots", "Dress Shoes", "Slides", "Hiking Boots", "Wedges",
    "Athletic Sandals", "Platform Shoes", "Oxfords", "Espadrilles", "Clogs",
    "Slip-On Sneakers", "Gum Boots", "Water Shoes", "Knee-High Boots", "Moccasins",
    "Sock Sneakers", "Thigh-High Boots", "Mary Janes", "Trail Shoes", "Court Sneakers",
    "Fashion Sneakers", "Casual Slip-Ons", "Strappy Sandals", "Chunky Heeled Boots", "Elegant Pumps",
    "Knee-Length Sneakers", "Wedge Sandals", "Retro High Tops", "Pointed-Toe Flats", "Dressy Ankle Boots",
    "Classic Oxfords", "Open-Toe Mules", "Platform Sandals", "Ankle Strap Heels", "Sporty Loafers",
    "Fuzzy Slippers", "Stylish Clogs", "Vintage Sneakers", "Trendy Combat Boots", "Bold Platform Sneakers",
    "Summer Slides", "Soft Slip-Ons", "Classic Ballerinas", "Designer Loafers", "Leather Flip Flops",
    "Woven Espadrilles", "Athletic Boots", "Fashionable Court Shoes", "Textured Sneakers", "Studded Heels",
    "Ankle Strap Sandals", "Casual Canvas Sneakers", "Trendy Platform Sneakers", "Sporty Slip-Ons", "Lace-Up Boots",
    "Classic Leather Sneakers", "Casual Moccasins", "Stylish Espadrilles", "Rubber Rain Boots", "Metallic Sandals",
    "Hiking Sneakers", "Chic Slingbacks", "Fashionable Heeled Sandals", "Suede Loafers", "Retro Running Shoes",
    "Fashion-forward Ankle Boots", "Chunky Heel Pumps", "Tactical Boots", "Classic Derby Shoes", "Cozy Indoor Slippers",
    "Sleek Slip-Ons", "Pointed Mules", "Casual Slip-Ons", "Comfy Slide Sandals", "Waterproof Hiking Boots",
    "Vintage Platform Shoes", "Street Style Sneakers", "Crossover Sneakers", "Cool Combat Boots", "Chic Block Heels",
    "Padded Running Shoes", "Elastic Ankle Boots", "Sleek Dress Boots"
]

accessories_names = [
    "Sunglasses", "Baseball Cap", "Beanie", "Scarf", "Watch",
    "Belt", "Backpack", "Handbag", "Crossbody Bag", "Clutch",
    "Bracelet", "Necklace", "Earrings", "Headphones", "Hat",
    "Gloves", "Umbrella", "Wallet", "Keychain", "Brooch",
    "Hair Clip", "Anklet", "Sunglass Chain", "Hairband", "Tote Bag",
    "Fanny Pack", "Card Holder", "Cosmetic Bag", "Laptop Sleeve", "Beach Bag",
    "Crossbody Purse", "Canvas Tote", "Fashionable Scarf", "Stylish Bucket Hat", "Colorful Beanie",
    "Elegant Watch", "Leather Belt", "Silk Headscarf", "Trendy Choker", "Pearl Earrings",
    "Minimalist Wallet", "Retro Sunglasses", "Sporty Cap", "Leather Backpack", "Casual Wristwatch",
    "Fuzzy Mittens", "Colorful Hair Tie", "Novelty Socks", "Charming Brooch", "Travel Passport Holder",
    "Elegant Ring", "Tropical Beach Bag", "Faux Fur Stole", "Knitted Beanie", "Leather Keychain",
    "Stylish Hair Clip", "Multi-Purpose Pouch", "Fashionable Umbrella", "Decorative Pin", "Luxury Handbag",
    "Vintage Shoulder Bag", "Colorful Infinity Scarf", "Stylish Bucket Hat", "Trendy Cardholder", "Sleek Crossbody Wallet",
    "Casual Baseball Cap", "Soft Cashmere Scarf", "Knit Beanie Hat", "Fashionable Fanny Pack", "Chic Tote Bag",
    "Luxe Leather Gloves", "Graphic Beanie", "Woven Clutch", "Double Layered Necklace", "Funky Hair Scrunchie",
    "Bold Statement Ring", "Classic Fedora Hat", "Charming Ankle Bracelet", "Unique Hairband", "Designer Handbag",
    "Retro Sunglasses", "Elegant Evening Clutch", "Stylish Fingerless Gloves", "Woolen Scarf", "Faux Leather Belt",
    "Knot Headband", "Cool Beaded Bracelet", "Personalized Keychain", "Colorful Hair Clip", "Decorative Wall Organizer",
    "Leather Travel Bag", "Printed Tote", "Double Stranded Necklace", "Adventurous Key Fob"
]

# Create training data

training_data = []

num_tops, num_bottoms, num_outerwear, num_footwear, num_accessories, currTotal = 0, 0, 0, 0, 0, 0

for _ in range(training_entries):
    currTotal += 1
    category = random.choice(categories)  #randomly select a category
    #the and statement is to make sure a somewhat-even distribution is being made accross all categories
    #this makes it so that the training data is not overly biased
    if category == 'tops' and num_tops <= currTotal/len(categories):
        name = random.choice(tops_names)
        num_tops += 1
    elif category == 'bottoms' and num_bottoms <= currTotal/len(categories):
        name = random.choice(bottoms_names)
        num_bottoms += 1
    elif category == 'outerwear' and num_outerwear <= currTotal/len(categories):
        name = random.choice(outerwear_names)
        num_outerwear += 1
    elif category == 'footwear' and num_footwear <= currTotal/len(categories):
        name = random.choice(footwear_names)
        num_footwear += 1
    elif category == 'accessories' and num_accessories <= currTotal/len(categories):
        name = random.choice(accessories_names)
        num_accessories += 1
    # Append the entry to the training_data list
    training_data.append({"name": name.lower(), "category": category.lower()})

def insert_in_batches(collection, data, batchsize):
    for i in range(0, len(data), batchsize):
        batch = data[i: i + batchsize] #creating the batch from data[i] to data[i+batchsize]
        collection.insert_many(batch)
        print(f"Inserted batch from {i} to {i + len(batch) - 1}")

insert_in_batches(collection, training_data, 100)

client.close()

