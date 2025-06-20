
import csv
import random
import json
import datetime

# --- Configuration ---
NUM_SKUS = 300000  # 10 lakh SKUs
OUTPUT_FILE = 'home_decor_products_complete.csv'

# --- Data Pools (Expanded and Refined) ---

manufacturers = [
    {"name": "CozyFurnish Co.", "focus": ["Furniture", "Textiles"]},
    {"name": "Artify Studios", "focus": ["Art", "Decor"]},
    {"name": "LumaLite Inc.", "focus": ["Lighting"]},
    {"name": "TimberTouch Design", "focus": ["Furniture", "Decor"]},
    {"name": "LuxeWeave Textiles", "focus": ["Textiles", "Decor"]},
    {"name": "UrbanCradle Collective", "focus": ["Furniture", "Storage"]},
    {"name": "TimeCraft Essentials", "focus": ["Decor", "Office"]},
    {"name": "WoodAge Originals", "focus": ["Furniture", "Decor"]},
    {"name": "Drapia Drapery", "focus": ["Textiles", "Bedding"]},
    {"name": "ReflectArt Mirrors", "focus": ["Decor"]},
    {"name": "SleepWise Solutions", "focus": ["Bedding", "Textiles"]},
    {"name": "FineWood Crafts", "focus": ["Furniture", "Kitchen"]},
    {"name": "Modulo Living Concepts", "focus": ["Furniture", "Storage", "Office"]},
    {"name": "WildHue Decor", "focus": ["Art", "Decor"]},
    {"name": "GlowHaus Lighting", "focus": ["Lighting"]},
    {"name": "EarthBloom Pottery", "focus": ["Decor", "Kitchen"]},
    {"name": "SoftNest Seating", "focus": ["Furniture"]},
    {"name": "Scentra Wellness", "focus": ["Decor"]},
    {"name": "Lumora Illumination", "focus": ["Lighting"]},
    {"name": "CloudWeave Comfort", "focus": ["Bedding", "Textiles"]},
    {"name": "DecoDen Interiors", "focus": ["Decor", "Storage"]},
    {"name": "AquaStone Fountains", "focus": ["Decor"]},
    {"name": "ColorChord Accents", "focus": ["Decor", "Textiles"]},
    {"name": "WarmThread Co.", "focus": ["Textiles", "Bedding"]},
    {"name": "DreamSpace Innovations", "focus": ["Kids Room", "Lighting"]},
    {"name": "TaskBuddy Organizers", "focus": ["Office", "Storage"]},
    {"name": "ErgoLine Designs", "focus": ["Office", "Furniture"]},
    {"name": "Playful Minds Kids", "focus": ["Kids Room"]},
    {"name": "GrowLuxe Planters", "focus": ["Decor"]},
    {"name": "GreenAura Plants", "focus": ["Decor"]},
    {"name": "UrbanRoots Furniture", "focus": ["Furniture"]},
    {"name": "HookNest Solutions", "focus": ["Decor", "Storage"]},
    {"name": "ReadGlow Innovations", "focus": ["Lighting", "Office"]},
    {"name": "ClayArt Ceramics", "focus": ["Kitchen", "Decor"]},
    {"name": "KitchenNest Organics", "focus": ["Kitchen", "Storage"]},
    {"name": "FabricFantasy Home", "focus": ["Textiles", "Decor"]},
    {"name": "EcoForm Woodworks", "focus": ["Furniture", "Storage"]},
    {"name": "GlowNite Decor", "focus": ["Lighting", "Kids Room"]},
    {"name": "WorkNest Solutions", "focus": ["Office", "Furniture"]},
    {"name": "PaperTrail Co. Designs", "focus": ["Office", "Decor"]},
    {"name": "BohoVibe Creations", "focus": ["Art", "Decor", "Textiles"]},
    {"name": "WickMuse Aromas", "focus": ["Decor"]},
    {"name": "Serenity Home Goods", "focus": ["Decor", "Textiles"]},
    {"name": "ModernLines Furniture", "focus": ["Furniture"]},
    {"name": "RusticCharm Collections", "focus": ["Furniture", "Decor"]},
    {"name": "ElegantSpaces Decor", "focus": ["Art", "Decor", "Lighting"]},
    {"name": "ChicDecor Boutique", "focus": ["Decor", "Textiles"]},
]

colors = [
    "Navy Blue", "Charcoal Gray", "Pure White", "Emerald Green", "Terracotta Orange",
    "Warm Beige", "Dusty Pink", "Mustard Yellow", "Olive Green", "Matte Black",
    "Brushed Gold", "Silver Chrome", "Natural Wood", "Multicolor Abstract", "Ivory",
    "Sky Blue", "Blush Pink", "Deep Red", "Sunshine Yellow", "Royal Purple",
    "Mint Green", "Bronze", "Copper", "Transparent", "Walnut Brown", "Oak", "Mahogany"
]

materials = [
    "Wood", "Metal", "Ceramic", "Glass", "Fabric", "Marble", "Rattan", "Jute", "Linen",
    "Velvet", "Leather", "Terracotta", "Concrete", "Bamboo", "Steel", "Acrylic", "Woven Cane",
    "Crystal", "Resin", "Teak", "Oak", "Pine", "Walnut", "Mahogany", "Brass", "Copper", "Iron",
    "Polyester", "Cotton", "Wool", "Stone", "Faux Fur", "Reclaimed Wood"
]

# **FIXED**: All `warranty_years` values are now integers to prevent errors with `random.randint`.
categories_subcategories_weighted = {
    "Furniture": {"sub_categories": ["Chair", "Sofa", "Table", "Bed", "Storage", "Desk", "Shelving", "Vanity"], "weights": [0.15, 0.12, 0.18, 0.1, 0.15, 0.1, 0.1, 0.05], "base_price_range": (100, 1500), "markup_range": (1.4, 2.5), "warranty_years": (1, 10)},
    "Art": {"sub_categories": ["Wall Decor", "Sculpture", "Prints", "Painting", "Tapestry", "Framed Art"], "weights": [0.3, 0.1, 0.2, 0.2, 0.1, 0.1], "base_price_range": (20, 500), "markup_range": (1.8, 3.5), "warranty_years": (1, 3)},
    "Lighting": {"sub_categories": ["Ceiling Lamp", "Table Lamp", "Floor Lamp", "Wall Sconce", "Ambient Light", "Pendant Light"], "weights": [0.2, 0.3, 0.2, 0.15, 0.05, 0.1], "base_price_range": (30, 800), "markup_range": (1.6, 3.0), "warranty_years": (1, 5)},
    "Decor": {"sub_categories": ["Vase", "Mirror", "Clock", "Candle Holder", "Figurine", "Planter", "Fountain", "Decorative Accent", "Tray", "Coaster", "Rug", "Curtains"], "weights": [0.1, 0.1, 0.08, 0.07, 0.05, 0.1, 0.03, 0.12, 0.05, 0.05, 0.15, 0.1], "base_price_range": (10, 300), "markup_range": (1.9, 4.0), "warranty_years": (1, 2)},
    "Textiles": {"sub_categories": ["Rug", "Curtains", "Cushion", "Throw Blanket", "Bedding", "Sheets", "Pillowcase", "Table Linen"], "weights": [0.2, 0.15, 0.15, 0.15, 0.15, 0.1, 0.05, 0.05], "base_price_range": (15, 600), "markup_range": (1.7, 3.5), "warranty_years": (1, 3)},
    "Kitchen": {"sub_categories": ["Tableware", "Cookware", "Utensils", "Storage", "Appliances", "Serveware", "Glassware"], "weights": [0.25, 0.15, 0.1, 0.2, 0.1, 0.1, 0.1], "base_price_range": (20, 500), "markup_range": (1.5, 3.0), "warranty_years": (1, 5)},
    "Bathroom": {"sub_categories": ["Bath Mat", "Shower Curtain", "Towel Set", "Storage Rack", "Accessory Set", "Vanity Mirror"], "weights": [0.15, 0.1, 0.2, 0.2, 0.2, 0.15], "base_price_range": (10, 250), "markup_range": (1.7, 3.5), "warranty_years": (1, 2)},
    "Storage": {"sub_categories": ["Basket", "Bin", "Shelf", "Cabinet", "Drawer Organizer", "Utility Cart", "Wall Organizer"], "weights": [0.2, 0.15, 0.15, 0.15, 0.1, 0.1, 0.15], "base_price_range": (15, 400), "markup_range": (1.6, 3.0), "warranty_years": (1, 3)},
    "Office": {"sub_categories": ["Desk Accessory", "Chair", "Organizer", "Notice Board", "Filing Cabinet", "Bookshelf"], "weights": [0.15, 0.25, 0.15, 0.1, 0.1, 0.25], "base_price_range": (20, 700), "markup_range": (1.5, 2.8), "warranty_years": (1, 7)},
    "Kids Room": {"sub_categories": ["Toy Storage", "Decor", "Furniture", "Lighting", "Play Mat", "Crib Bedding"], "weights": [0.2, 0.2, 0.2, 0.15, 0.15, 0.1], "base_price_range": (15, 300), "markup_range": (1.8, 3.5), "warranty_years": (1, 2)},
    "Outdoor Decor": {"sub_categories": ["Patio Furniture", "Garden Lighting", "Planter", "Outdoor Rug", "Garden Statue", "Fire Pit"], "weights": [0.2, 0.2, 0.2, 0.15, 0.1, 0.15], "base_price_range": (50, 1000), "markup_range": (1.6, 2.7), "warranty_years": (1, 5)}
}
category_names = list(categories_subcategories_weighted.keys())
category_weights = [1.5, 1.2, 1.3, 2.0, 1.8, 1.0, 0.8, 1.0, 0.7, 0.5, 0.6] # Relative popularity

adjectives = [
    "Modern", "Classic", "Rustic", "Elegant", "Minimalist", "Cozy", "Functional", "Stylish",
    "Spacious", "Compact", "Durable", "Soft", "Plush", "Vibrant", "Tranquil", "Chic",
    "Handcrafted", "Unique", "Vintage", "Industrial", "Bohemian", "Scandinavian", "Geometric",
    "Abstract", "Textured", "Luxurious", "Breezy", "Smart", "Ergonomic", "Art Deco", "Coastal",
    "Contemporary", "Transitional", "Farmhouse", "Mid-Century", "Glam", "Zen", "Distressed", "Carved"
]

# --- Helper Functions ---

def get_random_manufacturer(category):
    eligible_manufacturers = [m["name"] for m in manufacturers if category in m["focus"]]
    if not eligible_manufacturers:
        return random.choice([m["name"] for m in manufacturers])
    return random.choice(eligible_manufacturers)

def generate_product_name(category, sub_category, material, adj):
    prod_name_templates = {
        "Furniture": {
            "Chair": ["{} {} Chair", "{} Accent Chair", "{} Dining Chair (Set of {num})", "{} Swivel Chair"],
            "Sofa": ["{} {} Sofa", "{} Loveseat", "{} Sectional Sofa ({seat_count}-seater)"],
            "Table": ["{} {} Coffee Table", "{} Dining Table", "{} Side Table", "{} Console Table"],
            "Bed": ["{} {} Bed Frame (Standard)", "{} Platform Bed ({bed_size})", "{} Storage Bed"],
            "Storage": ["{} {} Drawer Cabinet", "{} Storage Unit", "{} Entryway Bench with Storage", "{} Bookshelf with {num} Shelves"],
            "Desk": ["{} {} Office Desk", "{} Writing Desk", "{} Standing Desk"],
            "Shelving": ["{} {} Bookshelf", "{} Wall Shelf (Set of {num_small})", "{} Display Shelf"],
            "Vanity": ["{} {} Vanity Table", "{} Bathroom Vanity"]
        },
        "Art": {
            "Wall Decor": ["{} {} Canvas Print", "{} Botanical Wall Art", "{} Geometric Metal Wall Decor"],
            "Sculpture": ["{} {} Figurine", "{} Tabletop Sculpture"],
            "Prints": ["Set of {num_small} {} Art Prints", "Tropical Leaf Print (Framed)"],
            "Painting": ["{} {} Oil Painting ({dim_size} cm)", "Sunset Landscape Painting"],
            "Tapestry": ["{} {} Wall Tapestry", "Large Bohemian Tapestry"],
            "Framed Art": ["{} {} Framed Art Print", "Gallery Wall Set of {num_small} (Framed)"]
        },
        "Lighting": {
            "Ceiling Lamp": ["{} {} Chandelier", "{} {} Pendant Light", "{} Flush Mount Light"],
            "Table Lamp": ["{} {} Table Lamp", "{} Bedside Lamp", "{} Desk Lamp"],
            "Floor Lamp": ["{} {} Floor Lamp", "{} Arc Floor Lamp", "{} Task Floor Lamp"],
            "Wall Sconce": ["{} {} Wall Sconce", "LED Wall Sconce"],
            "Ambient Light": ["{} Mood Light", "Smart LED Strip Light ({dim_long}m)", "Solar Pathway Lights (Set of {num_small})"],
            "Pendant Light": ["{} {} Pendant Light (Single)"]
        },
        "Decor": {
            "Vase": ["{} {} Ceramic Vase", "{} Glass Vase Set of {num_small}", "{} Terracotta Planter"],
            "Mirror": ["{} {} Wall Mirror", "{} Full Length Mirror", "{} Vanity Mirror"],
            "Clock": ["{} {} Wall Clock", "{} Desk Clock"],
            "Candle Holder": ["{} {} Candle Holder", "Set of {num_small} Taper Candle Holders", "{} Votive Holder"],
            "Figurine": ["{} {} Decorative Figurine", "{} Animal Figurine"],
            "Planter": ["{} {} Ceramic Planter", "Hanging Macrame Planter", "Set of {num_small} Indoor Planters"],
            "Fountain": ["{} Indoor Water Fountain", "Desktop Zen Fountain"],
            "Decorative Accent": ["{} {} Decorative Bowl", "{} Abstract Decor Piece", "{} Decorative Orb Set of {num_small}"],
            "Tray": ["{} {} Serving Tray", "{} Ottoman Tray"],
            "Coaster": ["Set of {num_small} {} Coasters", "{} Drink Coaster"],
            "Rug": ["{} {} Area Rug", "{} Runner Rug", "{} Round Rug"],
            "Curtains": ["{} {} Sheer Curtains", "{} Blackout Curtains"]
        },
        "Textiles": {
            "Rug": ["{} {} Area Rug", "{} Shag Rug", "{} Runner Rug"],
            "Curtains": ["{} {} Blackout Curtains", "{} Sheer Linen Curtains"],
            "Cushion": ["{} {} Throw Pillow", "Set of {num_small} Floor Cushions", "{} Lumbar Pillow"],
            "Throw Blanket": ["{} {} Knit Throw Blanket", "{} Faux Fur Throw", "{} Fleece Blanket"],
            "Bedding": ["{} {} Duvet Cover Set ({bed_size})", "Luxury Comforter ({bed_size})", "{} Quilt Set"],
            "Sheets": ["{} {} Cotton Sheet Set ({bed_size})", "Silk Blend Sheets ({bed_size})"],
            "Pillowcase": ["Set of {num_small} {} Pillowcases", "Standard Pillowcases"],
            "Table Linen": ["{} {} Tablecloth", "{} Table Runner ({dim_long}cm)", "Set of {num_small} Napkins"]
        },
        "Kitchen": {
            "Tableware": ["{} {} Dinnerware Set ({num}-piece)", "{} Ceramic Plate Set of {num_small}", "{} Mug Set of {num_small}"],
            "Cookware": ["{} {} Non-stick Pan Set", "{} Stainless Steel Pot"],
            "Utensils": ["{} {} Kitchen Utensil Set", "Set of {num_small} Cooking Spoons"],
            "Storage": ["{} {} Food Canister Set of {num_small}", "Stackable Storage Bins ({num_small}-pack)"],
            "Appliances": ["{} {} Electric Kettle", "{} Toaster Oven"],
            "Serveware": ["{} {} Serving Bowl", "{} Cheese Board", "{} Cake Stand"],
            "Glassware": ["Set of {num} {} Tumblers", "Set of {num_small} Wine Glasses"]
        },
        "Bathroom": {
            "Bath Mat": ["{} {} Bath Mat", "Memory Foam Bath Rug"],
            "Shower Curtain": ["{} {} Shower Curtain", "{} Fabric Shower Curtain"],
            "Towel Set": ["{} {} Towel Set ({num_small}-piece)", "{} Bath Towel"],
            "Storage Rack": ["{} {} Shower Caddy", "Over-the-Toilet Storage", "{} Towel Ladder"],
            "Accessory Set": ["{} {} Bathroom Accessory Set ({num_small}-piece)", "{} Soap Dispenser"],
            "Vanity Mirror": ["{} {} LED Vanity Mirror", "{} Fog-Free Shower Mirror"]
        },
        "Storage": {
            "Basket": ["{} {} Woven Basket (Large)", "Set of {num_small} {} Storage Baskets", "{} Laundry Hamper"],
            "Bin": ["{} {} Storage Bin with Lid", "Collapsible Fabric Bin", "{} Toy Bin"],
            "Shelf": ["{} {} Floating Shelf", "Corner Wall Shelf", "{} Cube Storage Unit"],
            "Cabinet": ["{} {} Storage Cabinet", "Accent Storage Cabinet"],
            "Drawer Organizer": ["Set of {num_small} Drawer Dividers", "{} Cutlery Tray"],
            "Utility Cart": ["{} {} Rolling Utility Cart", "{} Kitchen Cart"],
            "Wall Organizer": ["{} {} Wall-Mounted Organizer", "{} Mail Holder"]
        },
        "Office": {
            "Desk Accessory": ["{} {} Desk Organizer", "{} Pen Holder", "{} Document Tray"],
            "Chair": ["{} {} Ergonomic Office Chair", "Swivel Desk Chair", "{} Guest Chair"],
            "Organizer": ["{} {} File Organizer", "Magazine File Holder"],
            "Notice Board": ["{} {} Cork Board", "Magnetic Whiteboard"],
            "Filing Cabinet": ["{} {} 2-Drawer Filing Cabinet", "{} Mobile Pedestal"],
            "Bookshelf": ["{} {} Compact Bookshelf", "{} Ladder Bookshelf"]
        },
        "Kids Room": {
            "Toy Storage": ["{} {} Toy Chest", "Animal Print Storage Bin", "Set of {num_small} Toy Bins"],
            "Decor": ["{} {} Growth Chart", "Unicorn Wall Decal", "Moon Star Projector"],
            "Furniture": ["{} Kids Table & Chair Set ({seat_count}-seater)", "Toddler Armchair", "{} Kids Bed"],
            "Lighting": ["Star Projector Night Light", "Animal Shaped Lamp", "{} Night Light"],
            "Play Mat": ["{} {} Foam Play Mat", "{} Activity Mat"],
            "Crib Bedding": ["{} {} Crib Sheet Set", "{} Crib Blanket"]
        },
        "Outdoor Decor": {
            "Patio Furniture": ["{} {} Patio Chair", "{} Bistro Set ({seat_count}-seater)", "{} Outdoor Sofa"],
            "Garden Lighting": ["Solar Powered String Lights", "{} Pathway Lights (Set of {num_small})", "{} Lanterns"],
            "Planter": ["Large {} {} Planter", "Set of {num_small} {} Outdoor Pots", "{} Hanging Planter"],
            "Outdoor Rug": ["{} {} Outdoor Area Rug", "{} Patio Rug"],
            "Garden Statue": ["{} {} Garden Gnome", "{} Bird Bath"],
            "Fire Pit": ["{} {} Outdoor Fire Pit", "{} Portable Fire Pit"]
        }
    }
    
    selected_templates = prod_name_templates.get(category, {}).get(sub_category, ["{} {} Product"])
    template = random.choice(selected_templates)

    format_params = {
        'num': random.randint(2, 6),
        'num_small': random.randint(2, 4),
        'seat_count': random.choices([1, 2, 3, 4], weights=[0.2, 0.4, 0.3, 0.1], k=1)[0],
        'bed_size': random.choice(["Twin", "Full", "Queen", "King"]),
        'dim_size': random.randint(20, 100),
        'dim_long': random.randint(100, 300)
    }

    try:
        if template.count('{}') == 2:
            return template.format(adj, material, **format_params)
        elif template.count('{}') == 1:
            if sub_category in ["Chair", "Sofa", "Table", "Bed", "Storage", "Planter", "Cookware", "Utensils"]:
                return template.format(material, **format_params)
            else:
                return template.format(adj, **format_params)
        else:
            return template.format(**format_params)
    except (KeyError, IndexError):
        return f"{adj} {material} {sub_category}"

def generate_dimensions_weight(sub_category):
    dims, weight = (0, 0, 0), 0.0
    if sub_category == "Chair": dims, weight = (random.randint(40, 90), random.randint(40, 90), random.randint(70, 110)), round(random.uniform(5, 25), 1)
    elif sub_category == "Sofa": dims, weight = (random.randint(150, 250), random.randint(80, 100), random.randint(70, 90)), round(random.uniform(30, 100), 1)
    elif sub_category == "Table": dims, weight = (random.randint(60, 200), random.randint(40, 100), random.randint(40, 80)), round(random.uniform(10, 80), 1)
    elif sub_category == "Bed": dims, weight = (random.randint(140, 200), random.randint(190, 220), random.randint(30, 60)), round(random.uniform(40, 120), 1)
    elif sub_category == "Bookshelf" or sub_category == "Shelving": dims, weight = (random.randint(50, 120), random.randint(20, 40), random.randint(80, 200)), round(random.uniform(10, 50), 1)
    elif sub_category == "Vase": dims, weight = (random.randint(10, 30), random.randint(10, 30), random.randint(15, 60)), round(random.uniform(0.5, 5), 1)
    elif sub_category == "Rug": dims, weight = (random.choice([120, 160, 200]), random.choice([180, 230, 300]), 1), round(random.uniform(2, 20), 1)
    elif sub_category == "Mirror": dims, weight = (random.randint(40, 90), 3, random.randint(60, 180)), round(random.uniform(2, 15), 1)
    else: dims, weight = (random.randint(5, 50), random.randint(5, 50), random.randint(5, 50)), round(random.uniform(0.1, 5), 1)
    return f"{dims[0]}x{dims[1]}x{dims[2]} cm", weight

def generate_rating_reviews():
    rating = round(random.lognormvariate(1.5, 0.2), 1)
    rating = min(5.0, max(3.0, rating))
    num_reviews = int(random.expovariate(1/100) + 1)
    if rating >= 4.5: num_reviews = int(num_reviews * random.uniform(1, 3))
    num_reviews = max(1, num_reviews)
    return rating, num_reviews

def generate_warranty(category_data):
    min_years, max_years = category_data["warranty_years"]
    if min_years == max_years: return f"{min_years} Year(s)"
    return f"{random.randint(min_years, max_years)} Year(s)"

def generate_tags(category, sub_category, material, colour, product_name):
    # **FIXED**: Using a set for automatic uniqueness and efficiency
    selected_tags = set()
    selected_tags.update(random.sample(["home decor", "essential", "stylish", "functional", "modern home"], random.randint(1, 2)))
    selected_tags.update([s.lower() for s in random.sample(adjectives, random.randint(1, 2))])
    selected_tags.add(material.lower())
    selected_tags.add(colour.lower().replace(" ", "-"))
    selected_tags.add(category.lower().replace(" ", "-"))
    selected_tags.add(sub_category.lower().replace(" ", "-"))
    if "set" in product_name.lower(): selected_tags.add("set")
    if "eco-friendly" in product_name.lower() or "bamboo" in material.lower(): selected_tags.add("eco-friendly")
    if "handcrafted" in product_name.lower(): selected_tags.add("handcrafted")
    return list(selected_tags)

def generate_collective_set(category, sub_category):
    # **FIXED**: Using a set to build the list of collections, preventing duplicates.
    sets = set()
    sets.add(random.choice(["Home Essentials", "Complete Room Package", "Curated Designer Selection"]))
    room_sets = {
        "Furniture": "Living Room Suite", "Art": "Gallery Wall Kit", "Lighting": "Ambiance Lighting Set",
        "Decor": "Living Room Decor Kit", "Textiles": "Cozy Corner Kit", "Kitchen": "Dining & Entertaining Set",
        "Bathroom": "Spa Bathroom Essentials", "Storage": "Organization Master Kit", "Office": "Productivity Workspace Kit",
        "Kids Room": "Kids Room Adventure Set", "Outdoor Decor": "Patio Comfort Zone"
    }
    if category in room_sets: sets.add(room_sets[category])
    if random.random() < 0.6:
        sets.add(random.choice(["Modern Minimalist Collection", "Bohemian Rhapsody Kit", "Rustic Charm Series", "Scandinavian Simplicity"]))
    return list(sets)

# --- Main Generation Logic ---
data = []
header = [
    "SKU Code", "Product Name", "Manufacturer", "Colour", "Material", "Category",
    "Sub-category", "Dimensions (WxDxH cm)", "Weight (kg)", "Stock Quantity",
    "Average Customer Rating", "Number of Reviews", "Warranty", "Is Bestseller",
    "Is New Arrival", "Tags", "Collective Set", "CostPrice", "SellPrice"
]
data.append(header)

for i in range(1, NUM_SKUS + 1):
    sku_code = f"SKU{i:07d}"

    category = random.choices(category_names, weights=category_weights, k=1)[0]
    category_info = categories_subcategories_weighted[category]
    sub_category = random.choices(category_info["sub_categories"], weights=category_info["weights"], k=1)[0]

    manufacturer = get_random_manufacturer(category)
    colour = random.choice(colors)
    material = random.choice(materials)
    adj = random.choice(adjectives)

    product_name = generate_product_name(category, sub_category, material, adj)
    dimensions, weight = generate_dimensions_weight(sub_category)
    stock_quantity = random.choices([random.randint(0, 10), random.randint(11, 100), random.randint(101, 500)], weights=[0.1, 0.4, 0.5], k=1)[0]
    rating, num_reviews = generate_rating_reviews()
    warranty = generate_warranty(category_info)

    is_bestseller = random.random() < 0.05
    is_new_arrival = random.random() < 0.08

    tags = generate_tags(category, sub_category, material, colour, product_name)
    collective_set = generate_collective_set(category, sub_category)

    base_cost_range = category_info["base_price_range"]
    markup_range = category_info["markup_range"]
    cost_price = round(random.uniform(base_cost_range[0], base_cost_range[1]), 2)
    sell_price = round(cost_price * random.uniform(markup_range[0], markup_range[1]), 2)

    tags_str = json.dumps(tags)
    collective_set_str = json.dumps(collective_set)

    row = [
        sku_code, product_name, manufacturer, colour, material, category,
        sub_category, dimensions, weight, stock_quantity,
        rating, num_reviews, warranty, is_bestseller,
        is_new_arrival, tags_str, collective_set_str,
        f"{cost_price:.2f}", f"{sell_price:.2f}"
    ]
    data.append(row)

    if i % 10000 == 0:
        print(f"Generated {i} / {NUM_SKUS} SKUs...")

# --- Write to CSV ---
print("Writing data to CSV file...")
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(data)

print(f"Generation complete. Generated {NUM_SKUS} SKUs and saved to {OUTPUT_FILE}")
