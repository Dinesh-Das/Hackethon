# **Refining the Data**

# I'm working on the Python script, focusing on the data generation for home decor and Asian Paints products. The core task is modifying the data pools to incorporate more specific items and paint details, expanding upon the existing structure. I'm aiming for realism and variety.


# **Implementing New Categories**

# I've started integrating the new product categories requested, focusing on Asian Paints and Home Necessities. I'm meticulously refining the data pools, creating new subcategories, and crafting product name templates to ensure a diverse and realistic output. I'm working on adding paint-specific details.


# **Expanding the Data Sets**

# I'm now deeply immersed in customizing the data pools. I'm populating the 'Asian Paints' category, developing product names and subcategories, and ensuring color integration. Home necessities are coming next, with product names and templates tailored to their individual categories. It feels like I'm right on schedule.


# **Outlining New Structures**

# I'm now deep into the restructuring phase. I've removed the manufacturers list and adjusted the SKU count to match the output filename. I'm updating the `categories_subcategories` structure with the new 'Asian Paints' and 'Home Necessities' categories. I'm considering the best approach to the existing categories and subcategories.


# **Modifying Product Generation**

# I'm presently working on modifying the core product generation function and data pools. My focus is on integrating the "Asian Paints" and "Home Necessities" product lines. I'm crafting the `prod_name_templates` and adjusting the logic for selecting adjectives or colors as fillers. The goal is realistic, diverse product naming.


# **Updating Core Structures**

# I'm currently focused on refining the fundamental data structures. This involves adding 'Asian Paints' and 'Home Necessities' to `categories_subcategories`, designing specific templates for product names, and ensuring color integration for paint products. I'm modifying the script for efficient output.


# **Expanding the Product Lines**

# I'm now focusing on the "Asian Paints" and "Home Necessities" product lines. I've incorporated the new categories and subcategories into the product name templates, designing specific formats and selecting adjectives. I'm also adjusting the core logic to integrate colors with the paint categories. The data generation feels much more comprehensive now.


# **Modifying Name Generation**

# I'm now refining the product name generation, specifically for Asian Paints and Home Necessities. I'm focused on integrating the new `asian_paints_lines` into the name generation and modifying the filler type selection for paints. I'm also updating the home necessities templates to include adjectives. I will review the existing filler logic to ensure it is compatible.


# **Implementing Asian Paint Products**

# I'm now focusing on the data structures, specifically `prod_name_templates`. I'm reworking the paint templates to incorporate specific product lines like "Royale" and "Apex" instead of relying on a filler. I'm also crafting the "Home Necessities" templates, focusing on adjective-based product names, and refining the color selections. I will review the logic.


# **Analyzing Function Adjustments**

# I'm now examining the `generate_tags` and `generate_collective_set` functions to ensure the new categories and product lines are handled correctly. It seems the current code will generate relevant tags for the existing categories and subcategories. I will also add color as a tag for Asian Paints products and ensure that the adjective tags are used for Home Necessities products.


# **Refining Product Templates**

# I'm now modifying the product name templates to specify the "Asian Paints" and "Home Necessities" categories. I'm focusing on adding product line names for paints and including the correct adjective selection for the home necessities. I'm going to also review my logic.


# **Reviewing the Changes**

# I'm meticulously reviewing all the adjustments implemented in the script. I'm checking the integration of the new categories into the `categories_subcategories` structure and verifying the product name templates for both Asian Paints and Home Necessities. I'm checking the logic to make sure everything matches the code.


# **Finalizing the Implementation**

# I'm now fully focused on completing the code modifications. I've implemented all the category and template changes. I've updated the `generate_tags` and `generate_collective_set` functions to add category-specific tags and sets. I've checked the `colors` list, which seems good. I am now reviewing the code to check the logic.


# **Updating The Core Code**

# I'm now fully immersed in code modification. I've removed the unused manufacturer list, fixed the SKU count and the final `print` statement. I've also updated the `categories_subcategories` to include the new categories. Now I'm going to integrate the specific product lines into templates and adjust the helper functions.


# Of course! I have modified the Python script as requested. Here are the key changes I've made:

# 1.  **Updated Data Pools:** I've enhanced the `categories_subcategories` and the `prod_name_templates` to better generate data for Home Decoration, Asian Paints products, and Home Necessities like mattresses, sofas, etc.
# 2.  **Realistic Product Names:** The product name generation for Asian Paints now uses more realistic, brand-like names (e.g., "Royale Luxury Emulsion", "Apex Ultima Protek").
# 3.  **Manufacturer Column Removed:** The unused `manufacturers` data list has been completely removed from the code, fulfilling the request to not have a manufacturer column.
# 4.  **Enhanced Tagging:** The `generate_tags` and `generate_collective_set` functions have been updated to create more relevant tags and sets for the new product categories.
# 5.  **Configuration Tweak:** `NUM_SKUS` has been set to 1000 to match the original filename's intent and provide a manageable dataset.

# Here is the modified code:

# ```python
import csv
import random
import json

# --- Configuration ---
NUM_SKUS = 1000
OUTPUT_FILE = 'home_products_data.csv'

# --- Data Pools ---

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
    "Decor": ["Vase", "Mirror", "Clock", "Candle Holder", "Figurine", "Planter", "Fountain", "Decorative Accent", "Tray", "Coaster"],
    "Textiles": ["Rug", "Cushion", "Throw Blanket", "Bedding", "Sheets", "Pillowcase", "Table Linen"],
    "Kitchen": ["Tableware", "Cookware", "Utensils", "Storage", "Appliances", "Serveware", "Glassware"],
    "Bathroom": ["Bath Mat", "Shower Curtain", "Towel Set", "Storage Rack", "Accessory Set", "Vanity Mirror"],
    "Storage": ["Basket", "Bin", "Shelf", "Cabinet", "Drawer Organizer", "Utility Cart", "Wall Organizer"],
    "Home Necessities": ["Mattress", "Bedsheets", "Sofas", "Curtains", "Pillows", "Blankets"],
    "Paints": ["Interior Paints", "Exterior Paints", "Enamels", "Wood Finishes", "Metal Finishes", "Primers"]
}

adjectives = [
    "Modern", "Classic", "Rustic", "Elegant", "Minimalist", "Cozy", "Functional", "Stylish",
    "Spacious", "Compact", "Durable", "Soft", "Plush", "Vibrant", "Tranquil", "Chic",
    "Handcrafted", "Unique", "Vintage", "Industrial", "Bohemian", "Scandinavian", "Geometric",
    "Abstract", "Textured", "Luxurious", "Breezy", "Smart", "Ergonomic", "Art Deco", "Coastal",
    "Orthopedic", "Thermal", "Hypoallergenic"
]

materials = [
    "Wood", "Metal", "Ceramic", "Glass", "Fabric", "Marble", "Rattan", "Jute", "Linen",
    "Velvet", "Leather", "Terracotta", "Concrete", "Bamboo", "Steel", "Acrylic", "Woven",
    "Crystal", "Resin", "Teak", "Oak", "Pine", "Walnut", "Mahogany", "Brass", "Copper", "Iron",
    "Cotton", "Microfiber", "Silk", "Wool", "Memory Foam"
]

tags_pool = {
    "general": ["decor", "home", "stylish", "functional", "modern", "classic", "unique", "giftable", "durable"],
    "style": ["minimalist", "bohemian", "scandinavian", "industrial", "rustic", "glam", "coastal", "contemporary", "farmhouse"],
    "room": ["living room", "bedroom", "kitchen", "bathroom", "office", "dining room", "entryway", "kids room", "patio"],
    "material": ["wood", "metal", "ceramic", "glass", "fabric", "marble", "rattan", "jute", "linen", "velvet", "leather", "bamboo", "concrete"],
    "feature": ["comfort", "storage", "lighting", "seating", "ambient", "soft", "portable", "adjustable", "space-saving", "eco-friendly", "handmade", "essential"],
    "color_sense": ["vibrant", "neutral", "earthy", "bright", "dark", "pastel"],
    "occasion": ["holiday", "festive", "everyday use", "renovation"],
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
    prod_name_templates = {
        "Furniture": {
            "Chair": ["{} Armchair", "{} Dining Chair (Set of 2)", "{} Accent Chair"],
            "Sofa": ["{} Sofa", "{} Loveseat", "{} Sectional Sofa"],
            "Table": ["{} Coffee Table", "{} Dining Table", "{} Side Table"],
            "Bed": ["{} Bed Frame (Queen)", "{} Platform Bed", "{} Storage Bed"],
            "Storage": ["{} Drawer Cabinet", "{} Storage Unit", "{} Bookshelf"],
            "Desk": ["{} Office Desk", "{} Writing Desk", "{} Standing Desk"],
            "Shelving": ["{} Bookshelf", "{} Wall Shelf", "Set of 3 Floating Shelves"],
            "Vanity": ["{} Vanity Table", "{} Bathroom Vanity"]
        },
        "Art": {
            "Wall Decor": ["{} Abstract Canvas Print", "{} Botanical Wall Art"],
            "Sculpture": ["{} Tabletop Sculpture", "{} Abstract Figurine"],
            "Prints": ["Set of 3 Abstract Prints", "Tropical Leaf Print"],
            "Painting": ["{} Oil Painting (30x40)", "Sunset Landscape Painting"],
            "Tapestry": ["{} Wall Tapestry", "Large Bohemian Tapestry"],
            "Framed Art": ["{} Framed Print", "Gallery Wall Art Set of 5"]
        },
        "Lighting": {
            "Ceiling Lamp": ["{} Chandelier", "{} Pendant Light", "{} Flush Mount Light"],
            "Table Lamp": ["{} Table Lamp", "{} Bedside Lamp"],
            "Floor Lamp": ["{} Floor Lamp", "{} Arch Floor Lamp"],
            "Wall Sconce": ["{} Wall Sconce", "LED Wall Sconce"],
            "Ambient Light": ["{} Mood Light", "Smart LED Strip Light"],
            "Pendant Light": ["{} Geometric Pendant Light", "{} Rattan Pendant Light"]
        },
        "Decor": {
            "Vase": ["{} Ceramic Vase", "{} Glass Vase Set of 3", "{} Terracotta Vase"],
            "Mirror": ["{} Wall Mirror", "{} Full Length Mirror", "{} Vanity Mirror"],
            "Clock": ["{} Wall Clock", "{} Desk Clock"],
            "Candle Holder": ["{} Candle Holder", "Set of 3 Taper Candle Holders"],
            "Figurine": ["{} Decorative Figurine", "{} Animal Figurine"],
            "Planter": ["{} Ceramic Planter", "Hanging Macrame Planter", "Set of 3 Indoor Planters"],
            "Fountain": ["{} Indoor Water Fountain", "Desktop Zen Fountain"],
            "Decorative Accent": ["{} Decorative Bowl", "{} Abstract Decor Piece"],
            "Tray": ["{} Serving Tray", "{} Ottoman Tray"],
            "Coaster": ["Set of 4 Marble Coasters", "{} Agate Drink Coaster"]
        },
        "Textiles": {
            "Rug": ["{} Area Rug (5x7)", "{} Shag Rug", "{} Jute Runner Rug"],
            "Cushion": ["{} Throw Pillow", "Set of 2 Velvet Floor Cushions", "{} Lumbar Pillow"],
            "Throw Blanket": ["{} Knit Throw Blanket", "Faux Fur Throw", "{} Fleece Blanket"],
            "Bedding": ["{} Duvet Cover Set (Queen)", "Luxury Comforter", "{} Quilt Set"],
            "Sheets": ["{} Cotton Sheet Set", "{} Silk Blend Sheets"],
            "Pillowcase": ["Set of 2 Linen Pillowcases", "Standard Pillowcases"],
            "Table Linen": ["{} Tablecloth", "{} Table Runner", "Set of 6 Napkins"]
        },
        "Kitchen": {
            "Tableware": ["{} Dinnerware Set (16-piece)", "{} Ceramic Plate Set of 4", "{} Mug Set of 4"],
            "Cookware": ["{} Non-stick Pan Set", "{} Stainless Steel Pot"],
            "Utensils": ["{} Kitchen Utensil Set", "Set of 5 Cooking Spoons"],
            "Storage": ["{} Food Canister Set of 3", "Stackable Storage Bins (2-pack)"],
            "Appliances": ["{} Electric Kettle", "{} Toaster Oven"],
            "Serveware": ["{} Serving Bowl", "{} Cheese Board"],
            "Glassware": ["Set of 6 Tumblers", "Set of 4 Wine Glasses"]
        },
        "Bathroom": {
            "Bath Mat": ["{} Bath Mat", "Memory Foam Bath Rug"],
            "Shower Curtain": ["{} Shower Curtain", "Waffle Weave Shower Curtain"],
            "Towel Set": ["{} Towel Set (6-piece)", "{} Turkish Bath Towel"],
            "Storage Rack": ["{} Shower Caddy", "Over-the-Toilet Storage"],
            "Accessory Set": ["{} Bathroom Accessory Set (4-piece)", "{} Soap Dispenser"],
            "Vanity Mirror": ["{} LED Vanity Mirror", "{} Fog-Free Shower Mirror"]
        },
        "Storage": {
            "Basket": ["{} Woven Basket (Large)", "Set of 3 Storage Baskets", "{} Laundry Hamper"],
            "Bin": ["{} Storage Bin with Lid", "Collapsible Fabric Bin"],
            "Shelf": ["{} Floating Shelf", "Corner Wall Shelf", "{} Cube Storage Unit"],
            "Cabinet": ["{} Storage Cabinet", "Accent Storage Cabinet"],
            "Drawer Organizer": ["Set of 6 Drawer Dividers", "Bamboo Cutlery Tray"],
            "Utility Cart": ["{} Rolling Utility Cart", "{} Kitchen Cart"],
            "Wall Organizer": ["{} Wall-Mounted Organizer", "{} Mail Holder"]
        },
        "Home Necessities": {
            "Mattress": ["{} Memory Foam Mattress (Queen)", "{} Hybrid Spring Mattress (King)", "{} Orthopedic Mattress"],
            "Bedsheets": ["{} 400-TC Cotton Bedsheet Set", "{} Silky Satin Bedsheet Set", "{} Microfiber Bedsheet"],
            "Sofas": ["{} 3-Seater Velvet Sofa", "{} Leather Loveseat", "{} Modular Sectional Sofa"],
            "Curtains": ["{} Blackout Curtains (Pair)", "{} Sheer Linen Curtains", "{} Thermal Insulated Curtains"],
            "Pillows": ["{} Memory Foam Pillow", "Set of 2 Down Alternative Pillows", "{} Orthopedic Cervical Pillow"],
            "Blankets": ["{} Plush Fleece Blanket", "{} Chunky Knit Wool Blanket", "{} Weighted Cotton Blanket"]
        },
        "Paints": {
            "Interior Paints": ["Royale Luxury Emulsion", "Tractor Emulsion Shyne", "Apcolite Premium Satin Emulsion", "Royale Matt Finish"],
            "Exterior Paints": ["Apex Ultima Protek Weatherproof", "Ace Advanced Exterior Emulsion", "Apex Dust Proof Emulsion"],
            "Enamels": ["Apcolite Premium Gloss Enamel", "Tractor Synthetic Enamel", "Apcolite Satin Enamel"],
            "Wood Finishes": ["PU Interior Wood Finish (Gloss)", "Melamine Gold Clear Finish", "Royale Touch Wood Varnish"],
            "Metal Finishes": ["Apex Metal Enamel", "Direct to Metal Protective Paint", "Rust-Stop Metal Paint"],
            "Primers": ["TrueCare Interior Wall Primer", "TrueCare Exterior Wall Primer", "Universal Wood Primer", "Red Oxide Metal Primer"]
        }
    }

    selected_templates = prod_name_templates.get(category, {}).get(sub_category, ["Generic {} Product"])
    template = random.choice(selected_templates)

    if '{}' in template:
        filler_choices = adjectives + materials
        # Narrow down filler choices for better context
        if category == "Home Necessities" or sub_category in ["Cushion", "Throw Blanket"]:
            filler_choices = adjectives
        elif category in ["Furniture", "Storage"] or sub_category in ["Table", "Chair", "Bed"]:
             filler_choices = materials
        
        filler_type = random.choice(filler_choices)
        return template.format(filler_type)
    else:
        # For templates without a placeholder, like Asian Paints
        return template


def generate_tags(category, sub_category, product_name, colour):
    selected_tags = []
    selected_tags.extend(random.sample(tags_pool["general"], random.randint(1, 2)))
    selected_tags.extend(random.sample(tags_pool["feature"], random.randint(1, 2)))

    if random.random() < 0.8:
        selected_tags.extend(random.sample(tags_pool["style"], random.randint(1, 2)))

    lower_product_name = product_name.lower()
    lower_category = category.lower()

    if "living" in lower_product_name or "sofa" in lower_product_name:
        selected_tags.append("living room")
    if "bed" in lower_product_name or "mattress" in lower_product_name or sub_category in ["Bedsheets", "Pillows", "Blankets"]:
        selected_tags.append("bedroom")
    if "kitchen" in lower_product_name or lower_category == "kitchen":
        selected_tags.append("kitchen")
    if "bath" in lower_product_name or lower_category == "bathroom":
        selected_tags.append("bathroom")
    if "office" in lower_product_name or sub_category == "Desk":
        selected_tags.append("home office")
    
    if "paints" in lower_category:
        selected_tags.extend(["paint", "renovation", "wall treatment"])
    if "home necessities" in lower_category:
        selected_tags.extend(["essential", "comfort"])

    for mat in materials:
        if mat.lower() in lower_product_name:
            selected_tags.append(mat.lower())
    
    if colour.lower() not in selected_tags:
        selected_tags.append(colour.lower())

    return list(set(selected_tags))

def generate_collective_set(category, sub_category):
    selected_sets = []
    selected_sets.append(random.choice(collective_sets_pool["general_set"]))

    if random.random() < 0.7:
        if category in ["Furniture", "Textiles", "Decor", "Lighting", "Home Necessities"]:
            selected_sets.append(random.choice(collective_sets_pool["room_set"]))
        if random.random() < 0.5:
            selected_sets.append(random.choice(collective_sets_pool["style_set"]))

    if "paints" in category.lower():
        selected_sets.extend(["painting project kit", "home renovation supplies"])
    if "home necessities" in category.lower():
        if sub_category in ["Mattress", "Bedsheets", "Pillows", "Blankets"]:
            selected_sets.extend(["bedroom comfort bundle", "sleep well set"])
        if sub_category == "Sofas":
            selected_sets.append("living room seating solution")

    return list(set(selected_sets))

# --- Main Generation Logic ---
data = []
header = ["SKU_CODE", "PRODUCT_NAME", "COLOUR", "CATEGORY", "SUB_CATEGORY", "TAGS", "COLLECTIVE_SET", "COST_PRICE", "SELL_PRICE"]
data.append(header)

for i in range(1, NUM_SKUS + 1):
    sku_code = f"SKU{i:04d}"

    category = random.choice(list(categories_subcategories.keys()))
    sub_category = random.choice(categories_subcategories[category])

    colour = random.choice(colors)
    product_name = generate_product_name(category, sub_category)
    
    tags = generate_tags(category, sub_category, product_name, colour)
    collective_set = generate_collective_set(category, sub_category)

    cost_price = round(random.uniform(15.00, 450.00), 2)
    sell_price = round(cost_price * random.uniform(1.5, 3.0), 2)
    if sell_price <= cost_price:
        sell_price = round(cost_price + random.uniform(10.00, 50.00), 2)

    tags_str = json.dumps(tags)
    collective_set_str = json.dumps(collective_set)

    row = [
        sku_code, product_name, colour, category,
        sub_category, tags_str, collective_set_str,
        f"{cost_price:.2f}", f"{sell_price:.2f}"
    ]
    data.append(row)

# --- Write to CSV ---
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(data)

print(f"Generated {NUM_SKUS} SKUs and saved to '{OUTPUT_FILE}'")
