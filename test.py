
import csv
import random
import json

# --- Configuration ---
NUM_SKUS = 300000
OUTPUT_FILE = 'home_decor_products_1000.csv'

# --- Data Pools ---

manufacturers = [
    "CozyFurnish Co.", "Artify Studios", "LumaLite Inc.", "TimberTouch", "LuxeWeave",
    "UrbanCradle", "TimeCraft", "WoodAge", "Drapia", "ReflectArt", "SleepWise",
    "FineWood", "Modulo Living", "WildHue", "GlowHaus", "EarthBloom", "SoftNest",
    "Scentra", "Lumora", "CloudWeave", "DecoDen", "AquaStone", "ColorChord",
    "WarmThread", "DreamSpace", "TaskBuddy", "ErgoLine", "Playful Minds", "GrowLuxe",
    "GreenAura", "UrbanRoots", "HookNest", "SleepTide", "ReadGlow", "ClayArt",
    "KitchenNest", "FabricFantasy", "EarthWeave", "PureStone", "EcoForm", "GlowNite",
    "WorkNest", "PaperTrail Co.", "DreamGlow", "ClutterFix", "BohoVibe", "WickMuse",
    "Serenity Home", "ModernLines", "RusticCharm", "ElegantSpaces", "BrightInteriors",
    "ZenLiving", "EcoDecor", "SmartHomeGoods", "ChicDecor", "ComfyHome",
    "Horizon Hues", "Grandeur Goods", "Terra Textiles", "Aura Accents", "Vista Decor"
]

colors = [
    "Blue", "Multicolor", "Gold", "Walnut", "Maroon", "White", "Grey", "Black",
    "Floral", "Silver", "Ivory", "Pine", "Terracotta", "Indigo", "Brown", "Green",
    "Teal", "Oak", "Maple", "Pink", "Red", "Yellow", "Orange", "Beige", "Cream",
    "Charcoal", "Emerald", "Lavender", "Turquoise", "Bronze", "Copper", "Natural",
    "Transparent", "Rose Gold", "Navy", "Sage Green", "Mustard Yellow", "Rust"
]

categories_subcategories = {
    "Furniture": ["Chair", "Sofa", "Table", "Bed", "Storage", "Desk", "Shelving", "Vanity"],
    "Art": ["Wall Decor", "Sculpture", "Prints", "Painting", "Tapestry", "Framed Art"],
    "Lighting": ["Ceiling Lamp", "Table Lamp", "Floor Lamp", "Wall Sconce", "Ambient Light", "Pendant Light"],
    "Decor": ["Vase", "Mirror", "Clock", "Candle Holder", "Figurine", "Planter", "Fountain", "Decorative Accent", "Tray", "Coaster", "Rug", "Curtains"],
    "Textiles": ["Rug", "Curtains", "Cushion", "Throw Blanket", "Bedding", "Sheets", "Pillowcase", "Table Linen"],
    "Kitchen": ["Tableware", "Cookware", "Utensils", "Storage", "Appliances", "Serveware", "Glassware"],
    "Bathroom": ["Bath Mat", "Shower Curtain", "Towel Set", "Storage Rack", "Accessory Set", "Vanity Mirror"],
    "Storage": ["Basket", "Bin", "Shelf", "Cabinet", "Drawer Organizer", "Utility Cart", "Wall Organizer"],
    "Office": ["Desk Accessory", "Chair", "Organizer", "Notice Board", "Filing Cabinet", "Bookshelf"],
    "Kids Room": ["Toy Storage", "Decor", "Furniture", "Lighting", "Play Mat", "Crib Bedding"],
    "Outdoor Decor": ["Patio Furniture", "Garden Lighting", "Planter", "Outdoor Rug", "Garden Statue", "Fire Pit"]
}

adjectives = [
    "Modern", "Classic", "Rustic", "Elegant", "Minimalist", "Cozy", "Functional", "Stylish",
    "Spacious", "Compact", "Durable", "Soft", "Plush", "Vibrant", "Tranquil", "Chic",
    "Handcrafted", "Unique", "Vintage", "Industrial", "Bohemian", "Scandinavian", "Geometric",
    "Abstract", "Textured", "Luxurious", "Breezy", "Smart", "Ergonomic", "Art Deco", "Coastal"
]

materials = [
    "Wood", "Metal", "Ceramic", "Glass", "Fabric", "Marble", "Rattan", "Jute", "Linen",
    "Velvet", "Leather", "Terracotta", "Concrete", "Bamboo", "Steel", "Acrylic", "Woven",
    "Crystal", "Resin", "Teak", "Oak", "Pine", "Walnut", "Mahogany", "Brass", "Copper", "Iron"
]

common_nouns = [
    "Armchair", "Sofa", "Table", "Lamp", "Vase", "Mirror", "Rug", "Clock", "Shelf", "Basket",
    "Cushion", "Curtain", "Duvet", "Sculpture", "Print", "Planter", "Fountain", "Organizer",
    "Cabinet", "Candle", "Diffuser", "Tray", "Coaster", "Bookcase", "Bed Frame", "Nightstand",
    "Dresser", "Wall Art", "Pillow", "Container", "Storage Box", "Dinnerware Set", "Mug", "Towels"
]

tags_pool = {
    "general": ["decor", "home", "stylish", "functional", "modern", "classic", "unique", "giftable", "durable"],
    "style": ["minimalist", "bohemian", "scandinavian", "industrial", "rustic", "glam", "coastal", "contemporary", "farmhouse"],
    "room": ["living room", "bedroom", "kitchen", "bathroom", "office", "dining room", "entryway", "kids room", "patio"],
    "material": ["wood", "metal", "ceramic", "glass", "fabric", "marble", "rattan", "jute", "linen", "velvet", "leather", "bamboo", "concrete"],
    "feature": ["comfort", "storage", "lighting", "seating", "ambient", "soft", "portable", "adjustable", "space-saving", "eco-friendly", "handmade"],
    "color_sense": ["vibrant", "neutral", "earthy", "bright", "dark", "pastel"],
    "occasion": ["holiday", "festive", "everyday use"],
    "mood": ["cozy", "relaxing", "energizing", "tranquil", "inviting"]
}

collective_sets_pool = {
    "room_set": ["living room set", "bedroom decor", "dining collection", "office setup", "bathroom essentials", "nursery decor", "outdoor living"],
    "style_set": ["boho chic set", "modern minimalist vibe", "rustic retreat collection", "industrial loft look", "glamorous accents"],
    "functional_set": ["reading nook essentials", "storage solutions", "entertainment zone", "wellness sanctuary", "workspace tools", "sleep comfort set"],
    "material_set": ["wood accent set", "ceramic art collection", "rattan furniture group", "linen luxury set"],
    "themed_set": ["coastal escape", "urban jungle", "zen garden kit", "seasonal decor bundle", "host's delight"],
    "general_set": ["home essentials", "complete decor kit", "designer's choice", "curated collection"]
}

# --- Helper Functions ---

def generate_product_name(category, sub_category):
    # Updated templates to use named placeholders like {num} for quantities
    prod_name_templates = {
        "Furniture": {
            "Chair": ["{} Armchair", "{} Dining Chair (Set of {num})", "{} Accent Chair", "{} Lounge Chair"],
            "Sofa": ["{} Sofa", "{} Loveseat", "{} Sectional Sofa"],
            "Table": ["{} Coffee Table", "{} Dining Table", "{} Side Table", "{} Console Table"],
            "Bed": ["{} Bed Frame (Queen)", "{} Platform Bed", "{} Storage Bed"],
            "Storage": ["{} Drawer Cabinet", "{} Storage Unit", "{} Entryway Bench", "{} Bookshelf with {num} Shelves"],
            "Desk": ["{} Office Desk", "{} Writing Desk", "{} Standing Desk"],
            "Shelving": ["{} Bookshelf", "{} Wall Shelf", "{} Display Shelf", "Set of {num_small} Floating Shelves"],
            "Vanity": ["{} Vanity Table", "{} Bathroom Vanity"]
        },
        "Art": {
            "Wall Decor": ["{} Abstract Canvas Print", "{} Botanical Wall Art", "{} Geometric Wall Decor"],
            "Sculpture": ["{} Figurine", "{} Tabletop Sculpture"],
            "Prints": ["Set of {num_small} Abstract Prints", "Tropical Leaf Print"],
            "Painting": ["{} Oil Painting (30x40)", "Sunset Landscape Painting"],
            "Tapestry": ["{} Wall Tapestry", "Large Bohemian Tapestry"],
            "Framed Art": ["{} Framed Print", "Gallery Wall Art Set of {num_small}"]
        },
        "Lighting": {
            "Ceiling Lamp": ["{} Chandelier", "{} Pendant Light", "{} Flush Mount Light"],
            "Table Lamp": ["{} Table Lamp", "{} Bedside Lamp", "{} Desk Lamp"],
            "Floor Lamp": ["{} Floor Lamp", "{} Arch Floor Lamp", "{} Task Floor Lamp"],
            "Wall Sconce": ["{} Wall Sconce", "LED Wall Sconce"],
            "Ambient Light": ["{} Mood Light", "Smart LED Strip Light", "Solar Pathway Lights (Set of {num_small})"],
            "Pendant Light": ["{} Pendant Light (Small)"]
        },
        "Decor": {
            "Vase": ["{} Ceramic Vase", "{} Glass Vase Set of {num_small}", "{} Terracotta Vase"],
            "Mirror": ["{} Wall Mirror", "{} Full Length Mirror", "{} Vanity Mirror"],
            "Clock": ["{} Wall Clock", "{} Desk Clock", "{} Digital Clock"],
            "Candle Holder": ["{} Candle Holder", "Set of {num_small} Taper Candle Holders", "{} Votive Holder"],
            "Figurine": ["{} Decorative Figurine", "{} Animal Figurine"],
            "Planter": ["{} Ceramic Planter", "Hanging Macrame Planter", "Set of {num_small} Indoor Planters"],
            "Fountain": ["{} Indoor Water Fountain", "Desktop Zen Fountain"],
            "Decorative Accent": ["{} Decorative Bowl", "{} Abstract Decor Piece", "{} Decorative Orb Set of {num_small}"],
            "Tray": ["{} Serving Tray", "{} Ottoman Tray"],
            "Coaster": ["Set of {num_small} Coasters", "{} Drink Coaster"],
            "Rug": ["{} Area Rug", "{} Runner Rug", "{} Round Rug"],
            "Curtains": ["{} Curtain Pair", "Sheer Linen Curtains"]
        },
        "Textiles": {
            "Rug": ["{} Area Rug", "{} Shag Rug", "{} Runner Rug"],
            "Curtains": ["{} Blackout Curtains", "Sheer Linen Curtains", "{} Rod Pocket Curtains"],
            "Cushion": ["{} Throw Pillow", "Set of {num_small} Floor Cushions", "{} Lumbar Pillow"],
            "Throw Blanket": ["{} Knit Throw Blanket", "Faux Fur Throw", "{} Fleece Blanket"],
            "Bedding": ["{} Duvet Cover Set", "Luxury Comforter", "{} Quilt Set"],
            "Sheets": ["{} Cotton Sheet Set", "Silk Blend Sheets", "{} Microfiber Sheets"],
            "Pillowcase": ["Set of {num_small} Linen Pillowcases", "Standard Pillowcases"],
            "Table Linen": ["{} Tablecloth", "{} Table Runner", "Set of {num_small} Napkins"]
        },
        "Kitchen": {
            "Tableware": ["{} Dinnerware Set ({num}-piece)", "{} Ceramic Plate Set of {num_small}", "{} Mug Set of {num_small}"],
            "Cookware": ["{} Non-stick Pan Set", "{} Stainless Steel Pot"],
            "Utensils": ["{} Kitchen Utensil Set", "Set of {num_small} Cooking Spoons"],
            "Storage": ["{} Food Canister Set of {num_small}", "Stackable Storage Bins ({num_small}-pack)"],
            "Appliances": ["{} Electric Kettle", "{} Toaster Oven"],
            "Serveware": ["{} Serving Bowl", "{} Cheese Board", "{} Cake Stand"],
            "Glassware": ["Set of {num} Tumblers", "Set of {num_small} Wine Glasses"]
        },
        "Bathroom": {
            "Bath Mat": ["{} Bath Mat", "Memory Foam Bath Rug"],
            "Shower Curtain": ["{} Shower Curtain", "{} Fabric Shower Curtain"],
            "Towel Set": ["{} Towel Set ({num_small}-piece)", "{} Bath Towel"],
            "Storage Rack": ["{} Shower Caddy", "Over-the-Toilet Storage", "{} Towel Ladder"],
            "Accessory Set": ["{} Bathroom Accessory Set ({num_small}-piece)", "{} Soap Dispenser"],
            "Vanity Mirror": ["{} LED Vanity Mirror", "{} Fog-Free Shower Mirror"]
        },
        "Storage": {
            "Basket": ["{} Woven Basket (Large)", "Set of {num_small} Storage Baskets", "{} Laundry Hamper"],
            "Bin": ["{} Storage Bin with Lid", "Collapsible Fabric Bin", "{} Toy Bin"],
            "Shelf": ["{} Floating Shelf", "Corner Wall Shelf", "{} Cube Storage Unit"],
            "Cabinet": ["{} Storage Cabinet", "Accent Storage Cabinet"],
            "Drawer Organizer": ["Set of {num_small} Drawer Dividers", "{} Cutlery Tray"],
            "Utility Cart": ["{} Rolling Utility Cart", "{} Kitchen Cart"],
            "Wall Organizer": ["{} Wall-Mounted Organizer", "{} Mail Holder"]
        },
        "Office": {
            "Desk Accessory": ["{} Desk Organizer", "Pen Holder", "{} Document Tray"],
            "Chair": ["{} Ergonomic Office Chair", "Swivel Desk Chair", "{} Guest Chair"],
            "Organizer": ["{} File Organizer", "Magazine File Holder"],
            "Notice Board": ["{} Cork Board", "Magnetic Whiteboard"],
            "Filing Cabinet": ["{} 2-Drawer Filing Cabinet", "{} Mobile Pedestal"],
            "Bookshelf": ["{} Compact Bookshelf", "{} Ladder Bookshelf"]
        },
        "Kids Room": {
            "Toy Storage": ["{} Toy Chest", "Animal Print Storage Bin", "Set of {num_small} Toy Bins"],
            "Decor": ["{} Growth Chart", "Unicorn Wall Decal", "Moon Star Projector"],
            "Furniture": ["{} Kids Table & Chair Set ({num_small}-seater)", "Toddler Armchair", "{} Kids Bed"],
            "Lighting": ["Star Projector Night Light", "Animal Shaped Lamp", "{} Night Light"],
            "Play Mat": ["{} Foam Play Mat", "{} Activity Mat"],
            "Crib Bedding": ["{} Crib Sheet Set", "{} Crib Blanket"]
        },
        "Outdoor Decor": {
            "Patio Furniture": ["{} Patio Chair", "{} Bistro Set ({num_small}-seater)", "{} Outdoor Sofa"],
            "Garden Lighting": ["Solar Powered String Lights", "{} Pathway Lights (Set of {num_small})", "{} Lanterns"],
            "Planter": ["Large {} Planter", "Set of {num_small} Outdoor Pots", "{} Hanging Planter"],
            "Outdoor Rug": ["{} Outdoor Area Rug", "{} Patio Rug"],
            "Garden Statue": ["{} Garden Gnome", "{} Bird Bath"],
            "Fire Pit": ["{} Outdoor Fire Pit", "{} Portable Fire Pit"]
        }
    }

    selected_templates = prod_name_templates.get(category, {}).get(sub_category, ["{} Product"])
    template = random.choice(selected_templates)

    # Determine the primary filler (adjective/material)
    filler_type = ""
    if "Table" in sub_category or "Chair" in sub_category or "Cabinet" in sub_category or "Shelf" in sub_category or "Bed" in sub_category or any(item in template.lower() for item in ["wood", "metal", "ceramic"]):
        filler_type = random.choice(materials)
    elif "Art" in category or "Decor" in category or "Lighting" in category:
        filler_type = random.choice(adjectives + materials)
    elif "Textiles" in category:
        filler_type = random.choice(materials + adjectives)
    else:
        filler_type = random.choice(adjectives)

    # Prepare named arguments for formatting
    format_params = {}
    if "{num}" in template:
        format_params['num'] = random.randint(2, 6) # Larger sets
    if "{num_small}" in template:
        format_params['num_small'] = random.randint(2, 4) # Smaller sets/packs

    # Apply formatting
    try:
        if '{}' in template:
            # If the template has an anonymous placeholder, fill it first
            return template.format(filler_type, **format_params)
        else:
            # If no anonymous placeholder, all must be named
            return template.format(**format_params)
    except KeyError as e:
        # This means a named placeholder existed in the template but was not in format_params
        # This shouldn't happen with the current logic, but serves as a robust fallback.
        print(f"Warning: Missing key for formatting '{template}'. Error: {e}. Falling back to generic name.")
        return f"{filler_type} {sub_category}"
    except IndexError as e:
        # This covers cases where '{}' is in template but format_params are also passed positionally
        # The above logic is designed to prevent this by separating.
        print(f"Warning: Index error formatting '{template}'. Error: {e}. Falling back to generic name.")
        return f"{filler_type} {sub_category}"


def generate_tags(category, sub_category, product_name):
    selected_tags = []
    # Ensure a minimum number of tags
    selected_tags.extend(random.sample(tags_pool["general"], random.randint(1, 2)))
    selected_tags.extend(random.sample(tags_pool["feature"], random.randint(1, 2)))

    # Add style tags based on a higher probability
    if random.random() < 0.8:
        selected_tags.extend(random.sample(tags_pool["style"], random.randint(1, 2)))

    # Add room-specific tags based on category/subcategory/product name clues
    lower_product_name = product_name.lower()
    lower_category = category.lower()
    lower_sub_category = sub_category.lower()

    if "living" in lower_product_name or "sofa" in lower_sub_category or lower_category == "furniture" and lower_sub_category in ["chair", "table"]:
        selected_tags.append("living room")
    if "bedroom" in lower_product_name or lower_category == "bedding" or lower_sub_category == "bed":
        selected_tags.append("bedroom")
    if "kitchen" in lower_product_name or lower_category == "kitchen":
        selected_tags.append("kitchen")
    if "bathroom" in lower_product_name or lower_category == "bathroom":
        selected_tags.append("bathroom")
    if "office" in lower_product_name or lower_category == "office" or lower_sub_category == "desk":
        selected_tags.append("home office")
    if "kids" in lower_category or "play" in lower_product_name:
        selected_tags.append("kids room")
        selected_tags.append("child-friendly")
    if "outdoor" in lower_category:
        selected_tags.append("outdoor use")

    # Add material/color specific tags derived from product name or color
    for mat in materials:
        if mat.lower() in lower_product_name:
            selected_tags.append(mat.lower())
    for col in colors:
        if col.lower() in lower_product_name or col.lower() == colour.lower(): # Check actual color as well
            if col.lower() not in selected_tags: # Avoid duplicates
                selected_tags.append(col.lower())

    return list(set(selected_tags)) # Ensure uniqueness and convert to list

def generate_collective_set(category, sub_category):
    selected_sets = []
    selected_sets.append(random.choice(collective_sets_pool["general_set"]))

    if random.random() < 0.7:
        if category in ["Furniture", "Textiles", "Decor", "Lighting"]:
            selected_sets.append(random.choice(collective_sets_pool["room_set"]))
        if random.random() < 0.5:
            selected_sets.append(random.choice(collective_sets_pool["style_set"]))

    if "Storage" in category or "Storage" in sub_category:
        selected_sets.append("organization collection")
    if "Kitchen" in category:
        selected_sets.append("chef's essentials")
    if "Bathroom" in category:
        selected_sets.append("spa day collection")
    if "Kids" in category:
        selected_sets.append("playroom essentials")
    if "Outdoor" in category:
        selected_sets.append("alfresco living")
    if "Furniture" in category and (sub_category == "Chair" or sub_category == "Sofa"):
        selected_sets.append("seating solution")
    if "Lighting" in category:
        selected_sets.append("illumination collection")
    if "Art" in category:
        selected_sets.append("gallery collection")
    if "Textiles" in category:
        selected_sets.append("comfort collection")


    return list(set(selected_sets)) # Ensure uniqueness and convert to list

# --- Main Generation Logic ---
data = []
header = ["SKU_CODE", "PRODUCT_NAME", "Manufacturer", "COLOUR", "CATEGORY", "SUB_CATEGORY", "TAGS", "COLLECTIVE_SET", "COST_PRICE", "SELL_PRICE"]
data.append(header)

for i in range(1, NUM_SKUS + 1):
    sku_code = f"SKU{i:04d}" # Changed to 04d for 1000 SKUs

    # Randomly select a category and then a sub-category that belongs to it
    category = random.choice(list(categories_subcategories.keys()))
    sub_category = random.choice(categories_subcategories[category])

    # Ensure colour is chosen independently for product variation
    colour = random.choice(colors)

    product_name = generate_product_name(category, sub_category)

    # Some product names might not accept a basic filler, or might be very specific,
    # so we can occasionally re-roll or modify if it looks odd.
    # For a robust dataset, this level of fine-tuning might be overkill
    # unless you see glaring issues after initial run.

    manufacturer = random.choice(manufacturers)

    tags = generate_tags(category, sub_category, product_name)
    collective_set = generate_collective_set(category, sub_category)

    cost_price = round(random.uniform(15.00, 350.00), 2)
    # Ensure a reasonable profit margin, e.g., 50% to 200% markup
    sell_price = round(cost_price * random.uniform(1.5, 3.0), 2)
    # Ensure sell_price is always higher than cost_price, minimum $5 markup
    if sell_price < cost_price + 5:
        sell_price = round(cost_price + random.uniform(5.00, 20.00), 2) # Add consistent random markup for minimum profit


    # Format tags and collective_set as JSON strings
    tags_str = json.dumps(tags)
    collective_set_str = json.dumps(collective_set)

    row = [
        sku_code, product_name, manufacturer, colour, category,
        sub_category, tags_str, collective_set_str,
        f"{cost_price:.2f}", f"{sell_price:.2f}"
    ]
    data.append(row)

# --- Write to CSV ---
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(data)

print(f"Generated {NUM_SKUS} SKUs and saved to {OUTPUT_FILE}")

