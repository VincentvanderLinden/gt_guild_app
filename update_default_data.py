import pandas as pd
from pathlib import Path

# Parse the table data
data = []

# Flip Co
data.extend([
    {'company_name': 'Flip Co', 'industry': 'Agriculture', 'professions': 'Agriculture, Food Production', 'timezone': 'UTC -07:00', 'local_time': '5:08 AM', 'Produced Goods': 'Rations', 'Guildees Pay:': 35, 'Live EXC Price': 43, 'Live AVG Price': 43, 'Guild Max': 35, 'Guild Min': 32, 'Guild % Discount': 20, 'Guild Fixed Discount': 0},
    {'company_name': 'Flip Co', 'industry': 'Agriculture', 'professions': 'Agriculture, Food Production', 'timezone': 'UTC -07:00', 'local_time': '5:08 AM', 'Produced Goods': 'Gourmet Rations', 'Guildees Pay:': 200, 'Live EXC Price': 195, 'Live AVG Price': 210, 'Guild Max': 300, 'Guild Min': 200, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'Flip Co', 'industry': 'Agriculture', 'professions': 'Agriculture, Food Production', 'timezone': 'UTC -07:00', 'local_time': '5:08 AM', 'Produced Goods': 'Vitaqua', 'Guildees Pay:': 62, 'Live EXC Price': 76, 'Live AVG Price': 88, 'Guild Max': 150, 'Guild Min': 50, 'Guild % Discount': 18, 'Guild Fixed Discount': 0},
    {'company_name': 'Flip Co', 'industry': 'Agriculture', 'professions': 'Agriculture, Food Production', 'timezone': 'UTC -07:00', 'local_time': '5:08 AM', 'Produced Goods': 'Pie', 'Guildees Pay:': 295, 'Live EXC Price': 345, 'Live AVG Price': 345, 'Guild Max': 400, 'Guild Min': 295, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'Flip Co', 'industry': 'Agriculture', 'professions': 'Agriculture, Food Production', 'timezone': 'UTC -07:00', 'local_time': '5:08 AM', 'Produced Goods': 'Coffee', 'Guildees Pay:': 140, 'Live EXC Price': 165, 'Live AVG Price': 180, 'Guild Max': 200, 'Guild Min': 125, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'Flip Co', 'industry': 'Agriculture', 'professions': 'Agriculture, Food Production', 'timezone': 'UTC -07:00', 'local_time': '5:08 AM', 'Produced Goods': 'Ale', 'Guildees Pay:': 70, 'Live EXC Price': 73, 'Live AVG Price': 75, 'Guild Max': 95, 'Guild Min': 70, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'Flip Co', 'industry': 'Agriculture', 'professions': 'Agriculture, Food Production', 'timezone': 'UTC -07:00', 'local_time': '5:08 AM', 'Produced Goods': 'Quantum Research Data', 'Guildees Pay:': 1, 'Live EXC Price': 56000, 'Live AVG Price': 58000, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 99, 'Guild Fixed Discount': 0},
])

# MB Industries
data.extend([
    {'company_name': 'MB Industries', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Fission Fuel', 'Guildees Pay:': 1950, 'Live EXC Price': 2300, 'Live AVG Price': 2550, 'Guild Max': 2250, 'Guild Min': 1913, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'MB Industries', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Nanoweave Shielding', 'Guildees Pay:': 7000, 'Live EXC Price': 7800, 'Live AVG Price': 7900, 'Guild Max': 7300, 'Guild Min': 7000, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'MB Industries', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Fertilizer', 'Guildees Pay:': 38, 'Live EXC Price': 45, 'Live AVG Price': 48, 'Guild Max': 45, 'Guild Min': 38, 'Guild % Discount': 20, 'Guild Fixed Discount': 0},
    {'company_name': 'MB Industries', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Reinforced Glass', 'Guildees Pay:': 215, 'Live EXC Price': 230, 'Live AVG Price': 250, 'Guild Max': 238, 'Guild Min': 213, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'MB Industries', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Composite Shielding', 'Guildees Pay:': 3900, 'Live EXC Price': 4500, 'Live AVG Price': 4500, 'Guild Max': 4000, 'Guild Min': 3900, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'MB Industries', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Biopolyne', 'Guildees Pay:': 1050, 'Live EXC Price': 1000, 'Live AVG Price': 1250, 'Guild Max': 1188, 'Guild Min': 1063, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'MB Industries', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Rejuvaline', 'Guildees Pay:': 600, 'Live EXC Price': 690, 'Live AVG Price': 700, 'Guild Max': 665, 'Guild Min': 595, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'MB Industries', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Bio-Nutrient Blend', 'Guildees Pay:': 135, 'Live EXC Price': 160, 'Live AVG Price': 150, 'Guild Max': 143, 'Guild Min': 128, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'MB Industries', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Nanopolyne', 'Guildees Pay:': 320, 'Live EXC Price': 350, 'Live AVG Price': 375, 'Guild Max': 356, 'Guild Min': 319, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
])

# B0dega
data.extend([
    {'company_name': 'B0dega', 'industry': 'Manufacturing', 'professions': 'Manufacturing, Electronics', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Tools', 'Guildees Pay:': 63, 'Live EXC Price': 79, 'Live AVG Price': 74, 'Guild Max': 75, 'Guild Min': 60, 'Guild % Discount': 20, 'Guild Fixed Discount': 0},
    {'company_name': 'B0dega', 'industry': 'Manufacturing', 'professions': 'Manufacturing, Electronics', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Workwear', 'Guildees Pay:': 68, 'Live EXC Price': 85, 'Live AVG Price': 82, 'Guild Max': 80, 'Guild Min': 60, 'Guild % Discount': 20, 'Guild Fixed Discount': 0},
    {'company_name': 'B0dega', 'industry': 'Manufacturing', 'professions': 'Manufacturing, Electronics', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Exosuit', 'Guildees Pay:': 590, 'Live EXC Price': 740, 'Live AVG Price': 590, 'Guild Max': 600, 'Guild Min': 540, 'Guild % Discount': 20, 'Guild Fixed Discount': 0},
    {'company_name': 'B0dega', 'industry': 'Manufacturing', 'professions': 'Manufacturing, Electronics', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Welding Kit', 'Guildees Pay:': 370, 'Live EXC Price': 420, 'Live AVG Price': 410, 'Guild Max': 420, 'Guild Min': 370, 'Guild % Discount': 20, 'Guild Fixed Discount': 0},
    {'company_name': 'B0dega', 'industry': 'Manufacturing', 'professions': 'Manufacturing, Electronics', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Furniture', 'Guildees Pay:': 240, 'Live EXC Price': 260, 'Live AVG Price': 265, 'Guild Max': 240, 'Guild Min': 300, 'Guild % Discount': 20, 'Guild Fixed Discount': 0},
    {'company_name': 'B0dega', 'industry': 'Manufacturing', 'professions': 'Manufacturing, Electronics', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'VR Headset', 'Guildees Pay:': 2450, 'Live EXC Price': 2900, 'Live AVG Price': 3000, 'Guild Max': 2500, 'Guild Min': 2400, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'B0dega', 'industry': 'Manufacturing', 'professions': 'Manufacturing, Electronics', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Construction Vehicle', 'Guildees Pay:': 2300, 'Live EXC Price': 2900, 'Live AVG Price': 2850, 'Guild Max': 2700, 'Guild Min': 0, 'Guild % Discount': 20, 'Guild Fixed Discount': 0},
    {'company_name': 'B0dega', 'industry': 'Manufacturing', 'professions': 'Manufacturing, Electronics', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Cooling System', 'Guildees Pay:': 840, 'Live EXC Price': 1050, 'Live AVG Price': 1250, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 20, 'Guild Fixed Discount': 0},
    {'company_name': 'B0dega', 'industry': 'Manufacturing', 'professions': 'Manufacturing, Electronics', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Consumer Electronics', 'Guildees Pay:': 720, 'Live EXC Price': 850, 'Live AVG Price': 740, 'Guild Max': 750, 'Guild Min': 600, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
])

# Bane Inc.
data.extend([
    {'company_name': 'Bane Inc.', 'industry': 'Resource Extraction', 'professions': 'Resource Extraction, Agriculture', 'timezone': 'UTC -07:00', 'local_time': '5:08 AM', 'Produced Goods': 'Water', 'Guildees Pay:': 23, 'Live EXC Price': 23, 'Live AVG Price': 23, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Bane Inc.', 'industry': 'Resource Extraction', 'professions': 'Resource Extraction, Agriculture', 'timezone': 'UTC -07:00', 'local_time': '5:08 AM', 'Produced Goods': 'Limestone', 'Guildees Pay:': 55, 'Live EXC Price': 55, 'Live AVG Price': 56, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Bane Inc.', 'industry': 'Resource Extraction', 'professions': 'Resource Extraction, Agriculture', 'timezone': 'UTC -07:00', 'local_time': '5:08 AM', 'Produced Goods': 'Cotton', 'Guildees Pay:': 25, 'Live EXC Price': 25, 'Live AVG Price': 30, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Bane Inc.', 'industry': 'Resource Extraction', 'professions': 'Resource Extraction, Agriculture', 'timezone': 'UTC -07:00', 'local_time': '5:08 AM', 'Produced Goods': 'Leather', 'Guildees Pay:': 63, 'Live EXC Price': 63, 'Live AVG Price': 71, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
])

# Drunkenduo's Ruthless Dividend
data.extend([
    {'company_name': "Drunkenduo's Ruthless Dividend", 'industry': 'Metallurgy', 'professions': 'Metallurgy, Failing Hard, Chicken Farmer', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Truss', 'Guildees Pay:': 460, 'Live EXC Price': 510, 'Live AVG Price': 455, 'Guild Max': 500, 'Guild Min': 350, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': "Drunkenduo's Ruthless Dividend", 'industry': 'Metallurgy', 'professions': 'Metallurgy, Failing Hard, Chicken Farmer', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Composite Truss', 'Guildees Pay:': 1250, 'Live EXC Price': 1650, 'Live AVG Price': 1200, 'Guild Max': 1250, 'Guild Min': 750, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': "Drunkenduo's Ruthless Dividend", 'industry': 'Metallurgy', 'professions': 'Metallurgy, Failing Hard, Chicken Farmer', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Glass', 'Guildees Pay:': 67, 'Live EXC Price': 79, 'Live AVG Price': 77, 'Guild Max': 75, 'Guild Min': 55, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': "Drunkenduo's Ruthless Dividend", 'industry': 'Metallurgy', 'professions': 'Metallurgy, Failing Hard, Chicken Farmer', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Copper Wire', 'Guildees Pay:': 40, 'Live EXC Price': 86, 'Live AVG Price': 59, 'Guild Max': 40, 'Guild Min': 35, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': "Drunkenduo's Ruthless Dividend", 'industry': 'Metallurgy', 'professions': 'Metallurgy, Failing Hard, Chicken Farmer', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Titanium', 'Guildees Pay:': 1700, 'Live EXC Price': 2100, 'Live AVG Price': 1900, 'Guild Max': 1700, 'Guild Min': 1400, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': "Drunkenduo's Ruthless Dividend", 'industry': 'Metallurgy', 'professions': 'Metallurgy, Failing Hard, Chicken Farmer', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Silicon Wafer', 'Guildees Pay:': 205, 'Live EXC Price': 225, 'Live AVG Price': 215, 'Guild Max': 220, 'Guild Min': 200, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': "Drunkenduo's Ruthless Dividend", 'industry': 'Metallurgy', 'professions': 'Metallurgy, Failing Hard, Chicken Farmer', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Platinum', 'Guildees Pay:': 2750, 'Live EXC Price': 3400, 'Live AVG Price': 2850, 'Guild Max': 2750, 'Guild Min': 2100, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
])

# Karsian Industries
data.extend([
    {'company_name': 'Karsian Industries', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Construction Kit', 'Guildees Pay:': 1400, 'Live EXC Price': 1400, 'Live AVG Price': 1350, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Karsian Industries', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Amenities', 'Guildees Pay:': 1650, 'Live EXC Price': 1650, 'Live AVG Price': 1700, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Karsian Industries', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Prefab Kit', 'Guildees Pay:': 1350, 'Live EXC Price': 1350, 'Live AVG Price': 1550, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Karsian Industries', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Tiridium Alloy', 'Guildees Pay:': 6000, 'Live EXC Price': 6000, 'Live AVG Price': 6100, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Karsian Industries', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Structural Elements', 'Guildees Pay:': 3400, 'Live EXC Price': 3400, 'Live AVG Price': 3400, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Karsian Industries', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Tiridium Hull Plate', 'Guildees Pay:': 14000, 'Live EXC Price': 14000, 'Live AVG Price': 15000, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Karsian Industries', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Modern Prefab Kit', 'Guildees Pay:': 3050, 'Live EXC Price': 3050, 'Live AVG Price': 3050, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Karsian Industries', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Advanced Prefab Kit', 'Guildees Pay:': 8900, 'Live EXC Price': 8900, 'Live AVG Price': 9400, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Karsian Industries', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Industrial Machinery', 'Guildees Pay:': 12000, 'Live EXC Price': 12000, 'Live AVG Price': 12000, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
])

# Blackmoore Investment
data.extend([
    {'company_name': 'Blackmoore Investment', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Aluminium', 'Guildees Pay:': 510, 'Live EXC Price': 570, 'Live AVG Price': 460, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Blackmoore Investment', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Iron', 'Guildees Pay:': 270, 'Live EXC Price': 270, 'Live AVG Price': 260, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Blackmoore Investment', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Steel', 'Guildees Pay:': 760, 'Live EXC Price': 810, 'Live AVG Price': 770, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 50},
    {'company_name': 'Blackmoore Investment', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Truss', 'Guildees Pay:': 435, 'Live EXC Price': 510, 'Live AVG Price': 455, 'Guild Max': 450, 'Guild Min': 385, 'Guild % Discount': 15, 'Guild Fixed Discount': 0},
    {'company_name': 'Blackmoore Investment', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Aeridium', 'Guildees Pay:': 1950, 'Live EXC Price': 2150, 'Live AVG Price': 2100, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Blackmoore Investment', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Tiridium Alloy', 'Guildees Pay:': 5500, 'Live EXC Price': 6000, 'Live AVG Price': 6100, 'Guild Max': 0, 'Guild Min': 5500, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Blackmoore Investment', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Composite Truss', 'Guildees Pay:': 1500, 'Live EXC Price': 1650, 'Live AVG Price': 1200, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Blackmoore Investment', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Graphenium Wire', 'Guildees Pay:': 1750, 'Live EXC Price': 1950, 'Live AVG Price': 1800, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Blackmoore Investment', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Titanium', 'Guildees Pay:': 1900, 'Live EXC Price': 2100, 'Live AVG Price': 1900, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
])

# VEB Hochbau Walter Ulbricht
data.extend([
    {'company_name': 'VEB Hochbau Walter Ulbricht', 'industry': 'Construction', 'professions': 'Construction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Prefab Kit', 'Guildees Pay:': 1350, 'Live EXC Price': 1350, 'Live AVG Price': 1550, 'Guild Max': 1500, 'Guild Min': 1350, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'VEB Hochbau Walter Ulbricht', 'industry': 'Construction', 'professions': 'Construction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Modern Prefab Kit', 'Guildees Pay:': 2750, 'Live EXC Price': 3050, 'Live AVG Price': 3050, 'Guild Max': 3000, 'Guild Min': 2700, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'VEB Hochbau Walter Ulbricht', 'industry': 'Construction', 'professions': 'Construction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Structural Elements', 'Guildees Pay:': 3050, 'Live EXC Price': 3400, 'Live AVG Price': 3400, 'Guild Max': 3200, 'Guild Min': 2900, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'VEB Hochbau Walter Ulbricht', 'industry': 'Construction', 'professions': 'Construction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Amenities', 'Guildees Pay:': 1500, 'Live EXC Price': 1650, 'Live AVG Price': 1700, 'Guild Max': 1600, 'Guild Min': 1500, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
])

# VEB Speis & Schacht Staßfurt
data.extend([
    {'company_name': 'VEB Speis & Schacht Staßfurt', 'industry': 'Agriculture', 'professions': 'Agriculture, Food Production, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Bioxene', 'Guildees Pay:': 340, 'Live EXC Price': 340, 'Live AVG Price': 375, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
])

# VEB Chemiewerke Magdeburg
data.extend([
    {'company_name': 'VEB Chemiewerke Magdeburg', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Polyethylene', 'Guildees Pay:': 17, 'Live EXC Price': 18, 'Live AVG Price': 17, 'Guild Max': 0, 'Guild Min': 14, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'VEB Chemiewerke Magdeburg', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Hydrogen Fuel', 'Guildees Pay:': 105, 'Live EXC Price': 115, 'Live AVG Price': 125, 'Guild Max': 0, 'Guild Min': 100, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'VEB Chemiewerke Magdeburg', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Fission Fuel', 'Guildees Pay:': 2300, 'Live EXC Price': 2300, 'Live AVG Price': 2550, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'VEB Chemiewerke Magdeburg', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Fertilizer', 'Guildees Pay:': 43, 'Live EXC Price': 45, 'Live AVG Price': 48, 'Guild Max': 0, 'Guild Min': 40, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'VEB Chemiewerke Magdeburg', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Coolant', 'Guildees Pay:': 41, 'Live EXC Price': 41, 'Live AVG Price': 41, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'VEB Chemiewerke Magdeburg', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Reinforced Glass', 'Guildees Pay:': 250, 'Live EXC Price': 230, 'Live AVG Price': 250, 'Guild Max': 0, 'Guild Min': 250, 'Guild % Discount': 0, 'Guild Fixed Discount': 5},
    {'company_name': 'VEB Chemiewerke Magdeburg', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Insulation Panels', 'Guildees Pay:': 570, 'Live EXC Price': 570, 'Live AVG Price': 660, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'VEB Chemiewerke Magdeburg', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Graphene', 'Guildees Pay:': 420, 'Live EXC Price': 420, 'Live AVG Price': 445, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'VEB Chemiewerke Magdeburg', 'industry': 'Chemistry', 'professions': 'Chemistry, Resource Extraction', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Composite Shielding', 'Guildees Pay:': 4300, 'Live EXC Price': 4500, 'Live AVG Price': 4500, 'Guild Max': 0, 'Guild Min': 4000, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
])

# Technically Federated Reserves
data.extend([
    {'company_name': 'Technically Federated Reserves', 'industry': 'Chemistry', 'professions': 'Chemistry, Construction, Resource Extraction, Jack-of-all-Trades', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Flux', 'Guildees Pay:': 60, 'Live EXC Price': 69, 'Live AVG Price': 68, 'Guild Max': 60, 'Guild Min': 60, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Technically Federated Reserves', 'industry': 'Chemistry', 'professions': 'Chemistry, Construction, Resource Extraction, Jack-of-all-Trades', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Amenities', 'Guildees Pay:': 1550, 'Live EXC Price': 1650, 'Live AVG Price': 1700, 'Guild Max': 1550, 'Guild Min': 1550, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Technically Federated Reserves', 'industry': 'Chemistry', 'professions': 'Chemistry, Construction, Resource Extraction, Jack-of-all-Trades', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Construction Kit', 'Guildees Pay:': 1250, 'Live EXC Price': 1400, 'Live AVG Price': 1350, 'Guild Max': 1250, 'Guild Min': 1250, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Technically Federated Reserves', 'industry': 'Chemistry', 'professions': 'Chemistry, Construction, Resource Extraction, Jack-of-all-Trades', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Prefab Kit', 'Guildees Pay:': 1500, 'Live EXC Price': 1350, 'Live AVG Price': 1550, 'Guild Max': 1500, 'Guild Min': 1500, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Technically Federated Reserves', 'industry': 'Chemistry', 'professions': 'Chemistry, Construction, Resource Extraction, Jack-of-all-Trades', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Modern Prefab Kit', 'Guildees Pay:': 2800, 'Live EXC Price': 3050, 'Live AVG Price': 3050, 'Guild Max': 2800, 'Guild Min': 2800, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Technically Federated Reserves', 'industry': 'Chemistry', 'professions': 'Chemistry, Construction, Resource Extraction, Jack-of-all-Trades', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Structural Elements', 'Guildees Pay:': 3050, 'Live EXC Price': 3400, 'Live AVG Price': 3400, 'Guild Max': 3050, 'Guild Min': 3050, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Technically Federated Reserves', 'industry': 'Chemistry', 'professions': 'Chemistry, Construction, Resource Extraction, Jack-of-all-Trades', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Heat Shielding', 'Guildees Pay:': 3000, 'Live EXC Price': 3750, 'Live AVG Price': 3900, 'Guild Max': 3000, 'Guild Min': 3000, 'Guild % Discount': 30, 'Guild Fixed Discount': 0},
])

# DeLey
data.extend([
    {'company_name': 'DeLey', 'industry': 'Jack-of-all-Trades', 'professions': 'Jack-of-all-Trades', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Select Item', 'Guildees Pay:': 0, 'Live EXC Price': 0, 'Live AVG Price': 0, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
])

# Kombinat Fertigungswerke Ost
data.extend([
    {'company_name': 'Kombinat Fertigungswerke Ost', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Advanced Tools', 'Guildees Pay:': 205, 'Live EXC Price': 225, 'Live AVG Price': 200, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Kombinat Fertigungswerke Ost', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Hauler Bridge', 'Guildees Pay:': 85000, 'Live EXC Price': 88000, 'Live AVG Price': 86000, 'Guild Max': 0, 'Guild Min': 85000, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Kombinat Fertigungswerke Ost', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Tools', 'Guildees Pay:': 71, 'Live EXC Price': 79, 'Live AVG Price': 74, 'Guild Max': 0, 'Guild Min': 70, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'Kombinat Fertigungswerke Ost', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Fission Reactor', 'Guildees Pay:': 94000, 'Live EXC Price': 94000, 'Live AVG Price': 85000, 'Guild Max': 0, 'Guild Min': 80000, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Kombinat Fertigungswerke Ost', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Exosuit', 'Guildees Pay:': 670, 'Live EXC Price': 740, 'Live AVG Price': 590, 'Guild Max': 0, 'Guild Min': 500, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
])

# Cracklor Ltd
data.extend([
    {'company_name': 'Cracklor Ltd', 'industry': 'Construction', 'professions': 'Construction, Manufacturing, Metallurgy', 'timezone': 'UTC +13:00', 'local_time': '1:08 AM', 'Produced Goods': 'Amenities', 'Guildees Pay:': 1500, 'Live EXC Price': 1650, 'Live AVG Price': 1700, 'Guild Max': 1500, 'Guild Min': 1500, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Cracklor Ltd', 'industry': 'Construction', 'professions': 'Construction, Manufacturing, Metallurgy', 'timezone': 'UTC +13:00', 'local_time': '1:08 AM', 'Produced Goods': 'Construction Kit', 'Guildees Pay:': 1300, 'Live EXC Price': 1400, 'Live AVG Price': 1350, 'Guild Max': 1300, 'Guild Min': 1200, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Cracklor Ltd', 'industry': 'Construction', 'professions': 'Construction, Manufacturing, Metallurgy', 'timezone': 'UTC +13:00', 'local_time': '1:08 AM', 'Produced Goods': 'Prefab Kit', 'Guildees Pay:': 1400, 'Live EXC Price': 1350, 'Live AVG Price': 1550, 'Guild Max': 1400, 'Guild Min': 1400, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Cracklor Ltd', 'industry': 'Construction', 'professions': 'Construction, Manufacturing, Metallurgy', 'timezone': 'UTC +13:00', 'local_time': '1:08 AM', 'Produced Goods': 'Construction Vehicle', 'Guildees Pay:': 2400, 'Live EXC Price': 2900, 'Live AVG Price': 2850, 'Guild Max': 2400, 'Guild Min': 2400, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
])

# Potatoes
data.extend([
    {'company_name': 'Potatoes', 'industry': 'Agriculture', 'professions': 'Agriculture, Science', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Glass', 'Guildees Pay:': 70, 'Live EXC Price': 79, 'Live AVG Price': 77, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Potatoes', 'industry': 'Agriculture', 'professions': 'Agriculture, Science', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Rations', 'Guildees Pay:': 35, 'Live EXC Price': 43, 'Live AVG Price': 43, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Potatoes', 'industry': 'Agriculture', 'professions': 'Agriculture, Science', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Fine Rations', 'Guildees Pay:': 80, 'Live EXC Price': 100, 'Live AVG Price': 91, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
])

# Pear Inc
data.extend([
    {'company_name': 'Pear Inc', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Steel', 'Guildees Pay:': 770, 'Live EXC Price': 810, 'Live AVG Price': 770, 'Guild Max': 0, 'Guild Min': 600, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Pear Inc', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Composite Truss', 'Guildees Pay:': 1550, 'Live EXC Price': 1650, 'Live AVG Price': 1200, 'Guild Max': 0, 'Guild Min': 700, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Pear Inc', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Truss', 'Guildees Pay:': 485, 'Live EXC Price': 510, 'Live AVG Price': 455, 'Guild Max': 0, 'Guild Min': 375, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Pear Inc', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Tiridium Alloy', 'Guildees Pay:': 5700, 'Live EXC Price': 6000, 'Live AVG Price': 6100, 'Guild Max': 0, 'Guild Min': 5500, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Pear Inc', 'industry': 'Construction', 'professions': 'Construction, Metallurgy', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Modern Prefab Kit', 'Guildees Pay:': 2900, 'Live EXC Price': 3050, 'Live AVG Price': 3050, 'Guild Max': 0, 'Guild Min': 2800, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
])

# The Boring Company
data.extend([
    {'company_name': 'The Boring Company', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Drill', 'Guildees Pay:': 630, 'Live EXC Price': 700, 'Live AVG Price': 750, 'Guild Max': 700, 'Guild Min': 600, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'The Boring Company', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Mining Vehicle', 'Guildees Pay:': 3050, 'Live EXC Price': 3400, 'Live AVG Price': 3250, 'Guild Max': 3300, 'Guild Min': 2850, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
    {'company_name': 'The Boring Company', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Construction Vehicle', 'Guildees Pay:': 2600, 'Live EXC Price': 2900, 'Live AVG Price': 2850, 'Guild Max': 3000, 'Guild Min': 2300, 'Guild % Discount': 10, 'Guild Fixed Discount': 0},
])

# Caboose Inc.
data.extend([
    {'company_name': 'Caboose Inc.', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +04:00', 'local_time': '4:08 PM', 'Produced Goods': 'Tools', 'Guildees Pay:': 75, 'Live EXC Price': 79, 'Live AVG Price': 74, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Caboose Inc.', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +04:00', 'local_time': '4:08 PM', 'Produced Goods': 'Workwear', 'Guildees Pay:': 81, 'Live EXC Price': 85, 'Live AVG Price': 82, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Caboose Inc.', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +04:00', 'local_time': '4:08 PM', 'Produced Goods': 'Furniture', 'Guildees Pay:': 245, 'Live EXC Price': 260, 'Live AVG Price': 265, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Caboose Inc.', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +04:00', 'local_time': '4:08 PM', 'Produced Goods': 'Welding Kit', 'Guildees Pay:': 400, 'Live EXC Price': 420, 'Live AVG Price': 410, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Caboose Inc.', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +04:00', 'local_time': '4:08 PM', 'Produced Goods': 'Construction Tools', 'Guildees Pay:': 160, 'Live EXC Price': 170, 'Live AVG Price': 165, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Caboose Inc.', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +04:00', 'local_time': '4:08 PM', 'Produced Goods': 'Construction Vehicle', 'Guildees Pay:': 2750, 'Live EXC Price': 2900, 'Live AVG Price': 2850, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Caboose Inc.', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +04:00', 'local_time': '4:08 PM', 'Produced Goods': 'Combustion Engine', 'Guildees Pay:': 790, 'Live EXC Price': 830, 'Live AVG Price': 820, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Caboose Inc.', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +04:00', 'local_time': '4:08 PM', 'Produced Goods': 'Fabric', 'Guildees Pay:': 51, 'Live EXC Price': 54, 'Live AVG Price': 54, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Caboose Inc.', 'industry': 'Manufacturing', 'professions': 'Manufacturing', 'timezone': 'UTC +04:00', 'local_time': '4:08 PM', 'Produced Goods': 'Laboratory Suit', 'Guildees Pay:': 1150, 'Live EXC Price': 1150, 'Live AVG Price': 1100, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
])

# Skunk Industries
data.extend([
    {'company_name': 'Skunk Industries', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC -08:00', 'local_time': '4:08 AM', 'Produced Goods': 'Steel', 'Guildees Pay:': 770, 'Live EXC Price': 810, 'Live AVG Price': 770, 'Guild Max': 850, 'Guild Min': 720, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Skunk Industries', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC -08:00', 'local_time': '4:08 AM', 'Produced Goods': 'Platinum', 'Guildees Pay:': 3000, 'Live EXC Price': 3400, 'Live AVG Price': 2850, 'Guild Max': 3000, 'Guild Min': 2700, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'Skunk Industries', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC -08:00', 'local_time': '4:08 AM', 'Produced Goods': 'Titanium', 'Guildees Pay:': 2000, 'Live EXC Price': 2100, 'Live AVG Price': 1900, 'Guild Max': 2100, 'Guild Min': 1650, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
])

# ZorkCorp
data.extend([
    {'company_name': 'ZorkCorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Steel', 'Guildees Pay:': 770, 'Live EXC Price': 810, 'Live AVG Price': 770, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'ZorkCorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Glass', 'Guildees Pay:': 75, 'Live EXC Price': 79, 'Live AVG Price': 77, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'ZorkCorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Pipes', 'Guildees Pay:': 155, 'Live EXC Price': 165, 'Live AVG Price': 160, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'ZorkCorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Aluminium', 'Guildees Pay:': 540, 'Live EXC Price': 570, 'Live AVG Price': 460, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'ZorkCorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Copper Wire', 'Guildees Pay:': 82, 'Live EXC Price': 86, 'Live AVG Price': 59, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
    {'company_name': 'ZorkCorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC +01:00', 'local_time': '1:08 PM', 'Produced Goods': 'Truss', 'Guildees Pay:': 485, 'Live EXC Price': 510, 'Live AVG Price': 455, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 5, 'Guild Fixed Discount': 0},
])

# Piecorp
data.extend([
    {'company_name': 'Piecorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC -06:00', 'local_time': '6:08 AM', 'Produced Goods': 'Aluminium', 'Guildees Pay:': 570, 'Live EXC Price': 570, 'Live AVG Price': 460, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Piecorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC -06:00', 'local_time': '6:08 AM', 'Produced Goods': 'Iron', 'Guildees Pay:': 270, 'Live EXC Price': 270, 'Live AVG Price': 260, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Piecorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC -06:00', 'local_time': '6:08 AM', 'Produced Goods': 'Steel', 'Guildees Pay:': 810, 'Live EXC Price': 810, 'Live AVG Price': 770, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Piecorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC -06:00', 'local_time': '6:08 AM', 'Produced Goods': 'Truss', 'Guildees Pay:': 510, 'Live EXC Price': 510, 'Live AVG Price': 455, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Piecorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC -06:00', 'local_time': '6:08 AM', 'Produced Goods': 'Titanium', 'Guildees Pay:': 2100, 'Live EXC Price': 2100, 'Live AVG Price': 1900, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Piecorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC -06:00', 'local_time': '6:08 AM', 'Produced Goods': 'Platinum', 'Guildees Pay:': 3400, 'Live EXC Price': 3400, 'Live AVG Price': 2850, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Piecorp', 'industry': 'Metallurgy', 'professions': 'Metallurgy', 'timezone': 'UTC -06:00', 'local_time': '6:08 AM', 'Produced Goods': 'Silicon Wafer', 'Guildees Pay:': 225, 'Live EXC Price': 225, 'Live AVG Price': 215, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
])

# Romero Enterprises
data.extend([
    {'company_name': 'Romero Enterprises', 'industry': 'Food Production', 'professions': 'Food Production, Metallurgy', 'timezone': 'UTC -05:00', 'local_time': '7:08 AM', 'Produced Goods': 'Fine Rations', 'Guildees Pay:': 100, 'Live EXC Price': 100, 'Live AVG Price': 91, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Romero Enterprises', 'industry': 'Food Production', 'professions': 'Food Production, Metallurgy', 'timezone': 'UTC -05:00', 'local_time': '7:08 AM', 'Produced Goods': 'Steel', 'Guildees Pay:': 810, 'Live EXC Price': 810, 'Live AVG Price': 770, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Romero Enterprises', 'industry': 'Food Production', 'professions': 'Food Production, Metallurgy', 'timezone': 'UTC -05:00', 'local_time': '7:08 AM', 'Produced Goods': 'Ale', 'Guildees Pay:': 73, 'Live EXC Price': 73, 'Live AVG Price': 75, 'Guild Max': 0, 'Guild Min': 70, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Romero Enterprises', 'industry': 'Food Production', 'professions': 'Food Production, Metallurgy', 'timezone': 'UTC -05:00', 'local_time': '7:08 AM', 'Produced Goods': 'Truss', 'Guildees Pay:': 510, 'Live EXC Price': 510, 'Live AVG Price': 455, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Romero Enterprises', 'industry': 'Food Production', 'professions': 'Food Production, Metallurgy', 'timezone': 'UTC -05:00', 'local_time': '7:08 AM', 'Produced Goods': 'Copper Wire', 'Guildees Pay:': 86, 'Live EXC Price': 86, 'Live AVG Price': 59, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Romero Enterprises', 'industry': 'Food Production', 'professions': 'Food Production, Metallurgy', 'timezone': 'UTC -05:00', 'local_time': '7:08 AM', 'Produced Goods': 'Copper', 'Guildees Pay:': 810, 'Live EXC Price': 810, 'Live AVG Price': 680, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
])

# Stellara
data.extend([
    {'company_name': 'Stellara', 'industry': 'Science', 'professions': 'Science', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Research Data', 'Guildees Pay:': 1200, 'Live EXC Price': 1200, 'Live AVG Price': 1200, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Stellara', 'industry': 'Science', 'professions': 'Science', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Advanced Research Data', 'Guildees Pay:': 8300, 'Live EXC Price': 8300, 'Live AVG Price': 5600, 'Guild Max': 0, 'Guild Min': 5500, 'Guild % Discount': 0, 'Guild Fixed Discount': 0},
    {'company_name': 'Stellara', 'industry': 'Science', 'professions': 'Science', 'timezone': 'UTC +00:00', 'local_time': '12:08 PM', 'Produced Goods': 'Quantum Research Data', 'Guildees Pay:': 42000, 'Live EXC Price': 56000, 'Live AVG Price': 58000, 'Guild Max': 0, 'Guild Min': 0, 'Guild % Discount': 25, 'Guild Fixed Discount': 0},
])

# Create DataFrame
df = pd.DataFrame(data)

# Save to feather
output_path = Path('gt_guild_app/assets/data/default_guild_data.feather')
df.to_feather(output_path)

print(f"Created default_guild_data.feather with {len(df)} rows")
print(f"Companies: {df['company_name'].nunique()}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nSample rows:")
print(df.head(10))
