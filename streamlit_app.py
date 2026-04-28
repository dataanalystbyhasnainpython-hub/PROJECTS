# streamlit_app.py - Complete Self-Installing Application
"""
Pakistan Market Price Analyzer - Auto-Installing Version
No requirements.txt needed • Auto-detects and installs missing libraries
"""

import subprocess
import sys
import importlib

# ============================================================================
# AUTO-INSTALLER - Installs all required libraries automatically
# ============================================================================

def install_requirements():
    """Automatically install all required libraries"""
    
    required_libraries = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'plotly': 'plotly',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'plotly.graph_objects': 'plotly',
        'plotly.express': 'plotly'
    }
    
    missing_libraries = []
    
    for import_name, package_name in required_libraries.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing_libraries.append(package_name)
    
    if missing_libraries:
        # Remove duplicates
        missing_libraries = list(set(missing_libraries))
        print(f"Installing missing libraries: {missing_libraries}")
        
        for package in missing_libraries:
            try:
                subprocess.check_call([
                    sys.executable, 
                    "-m", 
                    "pip", 
                    "install", 
                    "--quiet", 
                    package
                ])
                print(f"✓ Installed {package}")
            except Exception as e:
                print(f"✗ Failed to install {package}: {e}")

# Run installer before anything else
install_requirements()

# ============================================================================
# NOW IMPORT ALL LIBRARIES
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# COMPLETE DATABASE
# ============================================================================

class PakistanProductDatabase:
    """Complete product database with all categories"""
    
    def __init__(self):
        self.products = self._initialize_all_products()
        self.markets = self._initialize_pakistan_markets()
        
    def _initialize_all_products(self):
        """All product categories"""
        
        products = [
            # Electronics - Laptops
            {"name": "Dell Latitude 3420", "brand": "Dell", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 185000, "specs": "i5-1135G7, 8GB RAM, 256GB SSD, 14\"", "variant": "Business", "popularity": "High"},
            {"name": "Dell Inspiron 15 3520", "brand": "Dell", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 145000, "specs": "i3-1215U, 8GB RAM, 512GB SSD, 15.6\"", "variant": "Home", "popularity": "High"},
            {"name": "Dell XPS 13 Plus", "brand": "Dell", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 425000, "specs": "i7-1360P, 16GB RAM, 1TB SSD, 13.4\" OLED", "variant": "Premium", "popularity": "Medium"},
            {"name": "Dell G15 Gaming", "brand": "Dell", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 285000, "specs": "Ryzen 7, 16GB RAM, 512GB SSD, RTX 3050", "variant": "Gaming", "popularity": "High"},
            {"name": "HP Pavilion 15", "brand": "HP", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 165000, "specs": "i5-1235U, 8GB RAM, 512GB SSD, 15.6\"", "variant": "Home", "popularity": "High"},
            {"name": "HP EliteBook 840 G9", "brand": "HP", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 245000, "specs": "i7-1255U, 16GB RAM, 512GB SSD, 14\"", "variant": "Business", "popularity": "High"},
            {"name": "HP Victus 15", "brand": "HP", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 225000, "specs": "Ryzen 5, 8GB RAM, 512GB SSD, GTX 1650", "variant": "Gaming", "popularity": "High"},
            {"name": "Lenovo ThinkPad E14", "brand": "Lenovo", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 175000, "specs": "i5-1135G7, 8GB RAM, 512GB SSD, 14\"", "variant": "Business", "popularity": "High"},
            {"name": "Lenovo IdeaPad Slim 3", "brand": "Lenovo", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 135000, "specs": "Ryzen 5, 8GB RAM, 512GB SSD, 15.6\"", "variant": "Home", "popularity": "High"},
            {"name": "Lenovo Legion 5", "brand": "Lenovo", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 315000, "specs": "Ryzen 7, 16GB RAM, 1TB SSD, RTX 3060", "variant": "Gaming", "popularity": "High"},
            {"name": "MacBook Air M1", "brand": "Apple", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 285000, "specs": "M1 Chip, 8GB RAM, 256GB SSD", "variant": "Premium", "popularity": "High"},
            {"name": "MacBook Air M2", "brand": "Apple", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 365000, "specs": "M2 Chip, 8GB RAM, 256GB SSD", "variant": "Premium", "popularity": "High"},
            {"name": "MacBook Pro 14\" M3", "brand": "Apple", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 525000, "specs": "M3 Pro, 18GB RAM, 512GB SSD", "variant": "Professional", "popularity": "Medium"},
            {"name": "Acer Aspire 5", "brand": "Acer", "category": "Electronics", "subcategory": "Laptops", 
             "base_price": 155000, "specs": "i5-1235U, 8GB RAM, 512GB SSD", "variant": "Home", "popularity": "High"},
            
            # Electronics - Smartphones
            {"name": "iPhone 15 Pro Max", "brand": "Apple", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 525000, "specs": "256GB, Titanium, A17 Pro", "variant": "Flagship", "popularity": "High"},
            {"name": "iPhone 15 Pro", "brand": "Apple", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 435000, "specs": "128GB, Titanium, A17 Pro", "variant": "Flagship", "popularity": "High"},
            {"name": "iPhone 15", "brand": "Apple", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 315000, "specs": "128GB, A16 Bionic", "variant": "Premium", "popularity": "High"},
            {"name": "iPhone 14", "brand": "Apple", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 275000, "specs": "128GB, A15 Bionic", "variant": "Premium", "popularity": "High"},
            {"name": "iPhone 13", "brand": "Apple", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 215000, "specs": "128GB, A15 Bionic", "variant": "Premium", "popularity": "High"},
            {"name": "Samsung Galaxy S24 Ultra", "brand": "Samsung", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 425000, "specs": "256GB, 12GB RAM", "variant": "Flagship", "popularity": "High"},
            {"name": "Samsung Galaxy S24", "brand": "Samsung", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 285000, "specs": "128GB, 8GB RAM", "variant": "Flagship", "popularity": "High"},
            {"name": "Samsung Galaxy A54", "brand": "Samsung", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 115000, "specs": "128GB, 8GB RAM", "variant": "Mid-Range", "popularity": "High"},
            {"name": "Samsung Galaxy A14", "brand": "Samsung", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 45000, "specs": "64GB, 4GB RAM", "variant": "Budget", "popularity": "High"},
            {"name": "Google Pixel 8 Pro", "brand": "Google", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 315000, "specs": "128GB, Tensor G3", "variant": "Flagship", "popularity": "Medium"},
            {"name": "OnePlus 12", "brand": "OnePlus", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 245000, "specs": "256GB, 16GB RAM", "variant": "Flagship", "popularity": "High"},
            {"name": "Infinix Note 30", "brand": "Infinix", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 45000, "specs": "128GB, 8GB RAM", "variant": "Budget", "popularity": "High"},
            {"name": "Tecno Camon 20", "brand": "Tecno", "category": "Electronics", "subcategory": "Smartphones", 
             "base_price": 42000, "specs": "256GB, 8GB RAM", "variant": "Budget", "popularity": "High"},
            
            # Electronics - Tablets & Watches
            {"name": "iPad Pro 12.9\" M2", "brand": "Apple", "category": "Electronics", "subcategory": "Tablets", 
             "base_price": 385000, "specs": "WiFi, 256GB, M2 Chip", "variant": "Professional", "popularity": "Medium"},
            {"name": "iPad Air 5th Gen", "brand": "Apple", "category": "Electronics", "subcategory": "Tablets", 
             "base_price": 225000, "specs": "WiFi, 64GB, M1 Chip", "variant": "Premium", "popularity": "High"},
            {"name": "iPad 10th Gen", "brand": "Apple", "category": "Electronics", "subcategory": "Tablets", 
             "base_price": 145000, "specs": "WiFi, 64GB", "variant": "Standard", "popularity": "High"},
            {"name": "Samsung Galaxy Tab S9", "brand": "Samsung", "category": "Electronics", "subcategory": "Tablets", 
             "base_price": 185000, "specs": "WiFi, 128GB", "variant": "Premium", "popularity": "Medium"},
            {"name": "Apple Watch Series 9", "brand": "Apple", "category": "Electronics", "subcategory": "Smartwatches", 
             "base_price": 125000, "specs": "GPS, 45mm", "variant": "Premium", "popularity": "High"},
            {"name": "Samsung Galaxy Watch 6", "brand": "Samsung", "category": "Electronics", "subcategory": "Smartwatches", 
             "base_price": 85000, "specs": "Bluetooth, 44mm", "variant": "Premium", "popularity": "High"},
            {"name": "AirPods Pro 2nd Gen", "brand": "Apple", "category": "Electronics", "subcategory": "Audio", 
             "base_price": 75000, "specs": "USB-C, ANC", "variant": "Premium", "popularity": "High"},
            {"name": "Sony WH-1000XM5", "brand": "Sony", "category": "Electronics", "subcategory": "Audio", 
             "base_price": 95000, "specs": "Wireless, ANC", "variant": "Premium", "popularity": "High"},
            {"name": "JBL Flip 6", "brand": "JBL", "category": "Electronics", "subcategory": "Audio", 
             "base_price": 35000, "specs": "Bluetooth, Waterproof", "variant": "Standard", "popularity": "High"},
            
            # Personal Care
            {"name": "Head & Shoulders Shampoo", "brand": "Head & Shoulders", "category": "Personal Care", "subcategory": "Shampoo", 
             "base_price": 850, "specs": "400ml, Anti-Dandruff", "variant": "Standard", "popularity": "High"},
            {"name": "Pantene Shampoo", "brand": "Pantene", "category": "Personal Care", "subcategory": "Shampoo", 
             "base_price": 750, "specs": "400ml, Hair Fall Control", "variant": "Standard", "popularity": "High"},
            {"name": "Sunsilk Shampoo", "brand": "Sunsilk", "category": "Personal Care", "subcategory": "Shampoo", 
             "base_price": 650, "specs": "400ml, Black Shine", "variant": "Standard", "popularity": "High"},
            {"name": "Dove Shampoo", "brand": "Dove", "category": "Personal Care", "subcategory": "Shampoo", 
             "base_price": 850, "specs": "400ml, Intense Repair", "variant": "Premium", "popularity": "High"},
            {"name": "Lux Soap", "brand": "Lux", "category": "Personal Care", "subcategory": "Soap", 
             "base_price": 120, "specs": "150g", "variant": "Standard", "popularity": "High"},
            {"name": "Dove Soap", "brand": "Dove", "category": "Personal Care", "subcategory": "Soap", 
             "base_price": 160, "specs": "100g", "variant": "Premium", "popularity": "High"},
            {"name": "Lifebuoy Soap", "brand": "Lifebuoy", "category": "Personal Care", "subcategory": "Soap", 
             "base_price": 100, "specs": "125g", "variant": "Standard", "popularity": "High"},
            {"name": "Colgate Toothpaste", "brand": "Colgate", "category": "Personal Care", "subcategory": "Toothpaste", 
             "base_price": 180, "specs": "200g", "variant": "Standard", "popularity": "High"},
            {"name": "Nivea Body Lotion", "brand": "Nivea", "category": "Personal Care", "subcategory": "Body Lotion", 
             "base_price": 650, "specs": "400ml", "variant": "Standard", "popularity": "High"},
            
            # Clothing
            {"name": "Simple Cotton Shalwar Kameez", "brand": "Local", "category": "Clothing", "subcategory": "Men's Traditional", 
             "base_price": 1500, "specs": "Cotton, Simple Stitching", "variant": "Basic", "popularity": "High"},
            {"name": "Premium Cotton Shalwar Kameez", "brand": "J.", "category": "Clothing", "subcategory": "Men's Traditional", 
             "base_price": 3500, "specs": "Egyptian Cotton, Premium", "variant": "Premium", "popularity": "High"},
            {"name": "Designer Shalwar Kameez", "brand": "Amir Adnan", "category": "Clothing", "subcategory": "Men's Traditional", 
             "base_price": 8500, "specs": "Embroidered, Festive", "variant": "Luxury", "popularity": "Medium"},
            {"name": "Men's Jeans", "brand": "Levi's", "category": "Clothing", "subcategory": "Men's Western", 
             "base_price": 4500, "specs": "Slim Fit, Denim", "variant": "Standard", "popularity": "High"},
            {"name": "Simple Lawn Suit", "brand": "Local", "category": "Clothing", "subcategory": "Women's Traditional", 
             "base_price": 1200, "specs": "Unstitched, 3-Piece", "variant": "Basic", "popularity": "High"},
            {"name": "Premium Lawn Suit", "brand": "Gul Ahmed", "category": "Clothing", "subcategory": "Women's Traditional", 
             "base_price": 3200, "specs": "Printed, 3-Piece", "variant": "Premium", "popularity": "High"},
            {"name": "Designer Lawn Suit", "brand": "Sana Safinaz", "category": "Clothing", "subcategory": "Women's Traditional", 
             "base_price": 6500, "specs": "Embroidered, 3-Piece", "variant": "Luxury", "popularity": "High"},
            {"name": "Peshawari Chappal", "brand": "Service", "category": "Clothing", "subcategory": "Footwear", 
             "base_price": 2500, "specs": "Leather, Handmade", "variant": "Standard", "popularity": "High"},
            
            # Groceries
            {"name": "Basmati Rice Super Kernel", "brand": "Falak", "category": "Groceries", "subcategory": "Rice", 
             "base_price": 380, "specs": "Per KG, Premium", "variant": "Premium", "popularity": "High"},
            {"name": "Chakki Atta Fine", "brand": "Ashrafi", "category": "Groceries", "subcategory": "Flour", 
             "base_price": 140, "specs": "Per KG", "variant": "Premium", "popularity": "High"},
            {"name": "Cooking Oil", "brand": "Soya Supreme", "category": "Groceries", "subcategory": "Oil", 
             "base_price": 520, "specs": "Per KG", "variant": "Premium", "popularity": "High"},
            {"name": "White Sugar", "brand": "Local", "category": "Groceries", "subcategory": "Sugar", 
             "base_price": 140, "specs": "Per KG", "variant": "Standard", "popularity": "High"},
            {"name": "Daal Chana", "brand": "Local", "category": "Groceries", "subcategory": "Pulses", 
             "base_price": 260, "specs": "Per KG", "variant": "Standard", "popularity": "High"},
            {"name": "Black Tea", "brand": "Tapal", "category": "Groceries", "subcategory": "Beverages", 
             "base_price": 480, "specs": "385g", "variant": "Premium", "popularity": "High"},
            {"name": "Milk Pack", "brand": "Olpers", "category": "Groceries", "subcategory": "Dairy", 
             "base_price": 230, "specs": "1 Liter", "variant": "Premium", "popularity": "High"},
            
            # Home Appliances
            {"name": "Dawlance Refrigerator 9178", "brand": "Dawlance", "category": "Appliances", "subcategory": "Refrigerator", 
             "base_price": 85000, "specs": "12 cu ft, Glass Door", "variant": "Standard", "popularity": "High"},
            {"name": "Haier Refrigerator HRF-336", "brand": "Haier", "category": "Appliances", "subcategory": "Refrigerator", 
             "base_price": 125000, "specs": "14 cu ft, Inverter", "variant": "Premium", "popularity": "High"},
            {"name": "Dawlance Washing Machine 6100", "brand": "Dawlance", "category": "Appliances", "subcategory": "Washing Machine", 
             "base_price": 45000, "specs": "Twin Tub, 10kg", "variant": "Standard", "popularity": "High"},
            {"name": "Gree AC 1 Ton", "brand": "Gree", "category": "Appliances", "subcategory": "AC", 
             "base_price": 125000, "specs": "1 Ton, Inverter", "variant": "Premium", "popularity": "High"},
            {"name": "Philips Iron", "brand": "Philips", "category": "Appliances", "subcategory": "Iron", 
             "base_price": 2800, "specs": "Dry Iron, 1000W", "variant": "Standard", "popularity": "High"},
            
            # Furniture
            {"name": "Wooden Bed Double", "brand": "Interwood", "category": "Furniture", "subcategory": "Bedroom", 
             "base_price": 45000, "specs": "Double Size, Sheesham", "variant": "Premium", "popularity": "High"},
            {"name": "Sofa Set 3+1+1", "brand": "Interwood", "category": "Furniture", "subcategory": "Living Room", 
             "base_price": 85000, "specs": "Fabric, Modern", "variant": "Premium", "popularity": "High"},
            {"name": "Dining Table 6 Chairs", "brand": "Interwood", "category": "Furniture", "subcategory": "Dining", 
             "base_price": 55000, "specs": "Sheesham, 6 Seater", "variant": "Premium", "popularity": "High"},
            {"name": "Wardrobe 2 Door", "brand": "Interwood", "category": "Furniture", "subcategory": "Bedroom", 
             "base_price": 35000, "specs": "Sheesham, Mirror", "variant": "Premium", "popularity": "High"},
            
            # Home Decor
            {"name": "Handmade Carpet 6x4", "brand": "Local", "category": "Home Decor", "subcategory": "Carpets", 
             "base_price": 25000, "specs": "Persian Design, Wool", "variant": "Premium", "popularity": "Medium"},
            {"name": "Prayer Mat", "brand": "Local", "category": "Home Decor", "subcategory": "Religious", 
             "base_price": 1500, "specs": "Velvet, Padded", "variant": "Standard", "popularity": "High"},
            {"name": "Bedsheet Set", "brand": "ChenOne", "category": "Home Decor", "subcategory": "Bedding", 
             "base_price": 3200, "specs": "Cotton, 1+2 Pillow Covers", "variant": "Premium", "popularity": "High"},
            {"name": "Curtains Set", "brand": "ChenOne", "category": "Home Decor", "subcategory": "Curtains", 
             "base_price": 4500, "specs": "2 Panels, Blackout", "variant": "Premium", "popularity": "High"},
        ]
        
        return pd.DataFrame(products)
    
    def _initialize_pakistan_markets(self):
        """All Pakistan markets"""
        
        markets = [
            {"name": "Emporium Mall", "city": "Lahore", "type": "Premium Mall", "multiplier": 1.45, "rating": 4.6},
            {"name": "Packages Mall", "city": "Lahore", "type": "Premium Mall", "multiplier": 1.42, "rating": 4.4},
            {"name": "Dolmen Mall", "city": "Karachi", "type": "Premium Mall", "multiplier": 1.40, "rating": 4.5},
            {"name": "Lucky One Mall", "city": "Karachi", "type": "Premium Mall", "multiplier": 1.38, "rating": 4.3},
            {"name": "Centaurus Mall", "city": "Islamabad", "type": "Luxury Mall", "multiplier": 1.65, "rating": 4.7},
            {"name": "Fortress Square", "city": "Lahore", "type": "Standard Mall", "multiplier": 1.32, "rating": 4.0},
            {"name": "Mall of Lahore", "city": "Lahore", "type": "Standard Mall", "multiplier": 1.30, "rating": 4.1},
            {"name": "Atrium Mall", "city": "Karachi", "type": "Standard Mall", "multiplier": 1.28, "rating": 3.9},
            {"name": "Giga Mall", "city": "Islamabad", "type": "Standard Mall", "multiplier": 1.30, "rating": 3.9},
            {"name": "Hafeez Center", "city": "Lahore", "type": "Electronics Market", "multiplier": 1.15, "rating": 4.2},
            {"name": "Techno City", "city": "Karachi", "type": "Electronics Market", "multiplier": 1.12, "rating": 4.1},
            {"name": "Anarkali Bazaar", "city": "Lahore", "type": "Traditional Bazaar", "multiplier": 1.10, "rating": 4.3},
            {"name": "Liberty Market", "city": "Lahore", "type": "Local Bazaar", "multiplier": 1.15, "rating": 4.2},
            {"name": "Zainab Market", "city": "Karachi", "type": "Traditional Bazaar", "multiplier": 1.12, "rating": 4.0},
            {"name": "Tariq Road", "city": "Karachi", "type": "Local Bazaar", "multiplier": 1.14, "rating": 4.1},
            {"name": "Raja Bazaar", "city": "Rawalpindi", "type": "Traditional Bazaar", "multiplier": 1.10, "rating": 3.8},
            {"name": "Shah Alam Market", "city": "Lahore", "type": "Wholesale Hub", "multiplier": 1.00, "rating": 3.7},
            {"name": "Jodia Bazaar", "city": "Karachi", "type": "Wholesale Hub", "multiplier": 1.02, "rating": 3.5},
            {"name": "Faisalabad Textile", "city": "Faisalabad", "type": "Factory Outlet", "multiplier": 0.90, "rating": 4.0},
            {"name": "Local Store", "city": "All Cities", "type": "Local Shop", "multiplier": 1.20, "rating": 3.5},
            {"name": "Daraz.pk", "city": "Online", "type": "E-commerce", "multiplier": 1.18, "rating": 4.0},
            {"name": "PriceOye", "city": "Online", "type": "E-commerce", "multiplier": 1.12, "rating": 4.1},
        ]
        
        return pd.DataFrame(markets)
    
    def search_products(self, query):
        """Search products"""
        query_lower = query.lower()
        mask = (
            self.products['name'].str.lower().str.contains(query_lower, na=False) |
            self.products['brand'].str.lower().str.contains(query_lower, na=False) |
            self.products['category'].str.lower().str.contains(query_lower, na=False) |
            self.products['subcategory'].str.lower().str.contains(query_lower, na=False)
        )
        return self.products[mask].copy()
    
    def get_all_prices(self, product_base_price):
        """Get prices from all markets"""
        prices = []
        for _, market in self.markets.iterrows():
            final_price = round(product_base_price * market['multiplier'], 2)
            prices.append({
                'Market': market['name'],
                'City': market['city'],
                'Type': market['type'],
                'Price': final_price,
                'Rating': market['rating'],
                'Multiplier': f"{market['multiplier']:.2f}x"
            })
        return pd.DataFrame(prices).sort_values('Price')

# ============================================================================
# BILL GENERATION
# ============================================================================

def generate_bill(customer_name, product, market, price, quantity, total, payment):
    bill = f"""
    <div style="font-family: Arial; max-width: 800px; margin: auto; padding: 20px; border: 2px solid #006837; border-radius: 10px;">
        <div style="text-align: center;">
            <h1 style="color: #006837;">🇵🇰 PAKISTAN MARKET PRO</h1>
            <p>Official Purchase Receipt</p>
            <div style="height: 3px; background: linear-gradient(90deg, #006837 33%, white 33%, white 66%, #006837 66%);"></div>
        </div>
        <div style="margin: 20px 0;">
            <table style="width: 100%;">
                <tr><td><strong>Bill No:</strong> PMP-{datetime.now().strftime('%Y%m%d%H%M')}</td><td><strong>Date:</strong> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</td></tr>
                <tr><td><strong>Customer:</strong> {customer_name}</td><td><strong>Payment:</strong> {payment}</td></tr>
                <tr><td><strong>Market:</strong> {market['Market']}</td><td><strong>Location:</strong> {market['City']}</td></tr>
            </table>
        </div>
        <table style="width: 100%; border-collapse: collapse;">
            <thead><tr style="background: #006837; color: white;"><th style="padding: 10px;">Product</th><th style="padding: 10px;">Details</th><th style="padding: 10px;">Qty</th><th style="padding: 10px;">Price</th><th style="padding: 10px;">Total</th></tr></thead>
            <tbody><tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 10px;"><strong>{product['name']}</strong><br><small>{product['brand']}</small></td>
                <td style="padding: 10px; font-size: 12px;">{product['specs']}</td>
                <td style="padding: 10px; text-align: center;">{quantity}</td>
                <td style="padding: 10px; text-align: right;">Rs. {price:,.2f}</td>
                <td style="padding: 10px; text-align: right;">Rs. {total:,.2f}</td>
            </tr></tbody>
            <tfoot><tr style="border-top: 2px solid #006837; font-weight: bold;"><td colspan="4" style="padding: 10px; text-align: right;">Total Amount:</td><td style="padding: 10px; text-align: right;">Rs. {total:,.2f}</td></tr></tfoot>
        </table>
        <div style="margin-top: 40px; text-align: center; border-top: 2px dashed #006837; padding-top: 20px;">
            <div style="display: inline-block; border: 3px solid #006837; padding: 15px 30px; border-radius: 10px;">
                <p style="font-size: 22px; color: #006837; margin: 0; font-weight: bold;">✦ MUHAMMAD HASNAIN ✦</p>
                <p style="margin: 5px 0; color: #666;">Authorized Dealer • All Pakistan</p>
                <p style="margin: 5px 0; color: #006837; font-weight: bold;">✓ Verified & Approved ✓</p>
            </div>
        </div>
    </div>
    """
    return bill

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.set_page_config(page_title="Pakistan Market Pro", page_icon="🇵🇰", layout="wide")
    
    st.markdown("""
    <style>
        .main-title { background: linear-gradient(135deg, #006837 0%, #00a859 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 30px; }
        .product-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 10px 0; border-left: 5px solid #006837; }
        .price-tag { font-size: 24px; font-weight: bold; color: #006837; }
        .best-price { background: linear-gradient(135deg, #006837 0%, #00a859 100%); color: white; padding: 15px; border-radius: 10px; }
        .stButton > button { width: 100%; background-color: #006837; color: white; font-weight: bold; padding: 10px; font-size: 16px; }
        .search-box { background: #f8f9fa; padding: 30px; border-radius: 15px; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)
    
    @st.cache_resource
    def load_database():
        return PakistanProductDatabase()
    
    db = load_database()
    
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'selected_product' not in st.session_state:
        st.session_state.selected_product = None
    if 'price_df' not in st.session_state:
        st.session_state.price_df = None
    
    st.markdown("""
    <div class="main-title">
        <h1>🇵🇰 Pakistan Market Price Analyzer</h1>
        <h2>All Products • Electronics • Personal Care • Clothing • Groceries</h2>
        <p>Dell • HP • Apple • Samsung • Shampoo • Clothing • Rice • Complete Database</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.image("https://flagcdn.com/pk.svg", width=100)
        st.markdown("## 📊 Categories")
        categories = db.products['category'].unique()
        for cat in sorted(categories):
            count = len(db.products[db.products['category'] == cat])
            st.markdown(f"• **{cat}** ({count})")
        st.markdown("---")
        st.markdown("### 🔥 Quick Search")
        if st.button("💻 Dell Laptop"): st.session_state.search_query = "Dell"
        if st.button("📱 iPhone"): st.session_state.search_query = "iPhone"
        if st.button("🧴 Shampoo"): st.session_state.search_query = "Shampoo"
        if st.button("👔 Shalwar Kameez"): st.session_state.search_query = "Shalwar"
        if st.button("🍚 Rice"): st.session_state.search_query = "Rice"
    
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    st.markdown("## 🔍 Search Any Product")
    
    search_query = st.text_input(
        "Enter product name, brand, or category",
        placeholder="e.g., Dell Laptop, iPhone, Shampoo, Shalwar Kameez, Rice...",
        value=st.session_state.get('search_query', ''),
        key="search_input"
    )
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("💻 Electronics", use_container_width=True): search_query = "Electronics"
    with c2:
        if st.button("🧴 Personal Care", use_container_width=True): search_query = "Personal Care"
    with c3:
        if st.button("👔 Clothing", use_container_width=True): search_query = "Clothing"
    with c4:
        if st.button("🍚 Groceries", use_container_width=True): search_query = "Groceries"
    with c5:
        if st.button("🏠 Appliances", use_container_width=True): search_query = "Appliances"
    
    if st.button("🔍 Search", type="primary", use_container_width=True):
        if search_query:
            with st.spinner(f"Searching..."):
                st.session_state.search_results = db.search_products(search_query)
                st.session_state.selected_product = None
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.search_results is not None:
        results = st.session_state.search_results
        
        if len(results) > 0:
            st.markdown(f"### 📦 Found {len(results)} Products")
            cols = st.columns(2)
            for idx, (_, product) in enumerate(results.iterrows()):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div class="product-card">
                        <h3>{product['name']}</h3>
                        <p><strong>Brand:</strong> {product['brand']} | <strong>Category:</strong> {product['category']}</p>
                        <p><strong>Specs:</strong> {product['specs']}</p>
                        <p class="price-tag">Base Price: Rs. {product['base_price']:,.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"📊 Analyze Prices", key=f"sel_{idx}", use_container_width=True):
                        st.session_state.selected_product = product
                        st.session_state.price_df = db.get_all_prices(product['base_price'])
                        st.rerun()
        else:
            st.warning(f"No products found for '{search_query}'")
    
    if st.session_state.selected_product is not None:
        product = st.session_state.selected_product
        price_df = st.session_state.price_df
        
        st.markdown("---")
        st.markdown(f"## 📊 Price Analysis: {product['name']}")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"**Brand:** {product['brand']}")
            st.markdown(f"**Category:** {product['category']}")
        with c2:
            st.markdown(f"**Specs:** {product['specs']}")
            st.markdown(f"**Variant:** {product['variant']}")
        with c3:
            st.markdown(f"**Base Price:** Rs. {product['base_price']:,.2f}")
            savings = price_df['Price'].max() - price_df['Price'].min()
            st.markdown(f"**Potential Savings:** Rs. {savings:,.2f}")
        
        st.markdown("### 💰 Price Comparison")
        
        def color_prices(val):
            if isinstance(val, (int, float)):
                if val < price_df['Price'].quantile(0.33):
                    return 'background-color: #90EE90'
                elif val < price_df['Price'].quantile(0.66):
                    return 'background-color: #FFE4B5'
                else:
                    return 'background-color: #FFB6C1'
            return ''
        
        styled_df = price_df.style.applymap(color_prices, subset=['Price'])
        st.dataframe(styled_df, use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(price_df.head(15), x='Market', y='Price', color='Type', title="Price Comparison")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.scatter(price_df, x='Rating', y='Price', color='Type', hover_name='Market', title="Price vs Rating")
            st.plotly_chart(fig, use_container_width=True)
        
        cheapest = price_df.iloc[0]
        st.markdown(f"""
        <div class="best-price">
            <h3>💰 Best Price: {cheapest['Market']}</h3>
            <p>{cheapest['City']}</p>
            <h3>Rs. {cheapest['Price']:,.2f}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("## 🛒 Purchase")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            selected_market_name = st.selectbox("Select Market", price_df['Market'].tolist())
            selected_market = price_df[price_df['Market'] == selected_market_name].iloc[0]
            price = selected_market['Price']
            quantity = st.number_input("Quantity", min_value=1, value=1)
            total = price * quantity
            st.markdown(f"### Total: Rs. {total:,.2f}")
        with c2:
            customer_name = st.text_input("Your Name", "Customer")
            payment_method = st.selectbox("Payment", ["Cash on Delivery", "JazzCash", "EasyPaisa", "Bank Transfer"])
        
        if st.button("✅ Generate Bill", type="primary", use_container_width=True):
            bill_html = generate_bill(customer_name, product, selected_market, price, quantity, total, payment_method)
            st.markdown(bill_html, unsafe_allow_html=True)
            st.download_button("📥 Download Bill", data=bill_html, 
                             file_name=f"Bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                             mime="text/html", use_container_width=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p>🇵🇰 Pakistan Market Price Analyzer • Complete Database • Smart Shopping</p>
        <p style="font-size: 12px; color: #666;">© 2024 Muhammad Hasnain - Authorized Dealer All Pakistan</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
