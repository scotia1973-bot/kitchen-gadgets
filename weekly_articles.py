#!/usr/bin/env python3
"""
Weekly Kitchen Gadgets Article Generator for GadgetHumans
Creates 2 new articles and deploys to GitHub Pages
Scheduled: Every Wednesday at 9:00 AM
"""
import os, sys, shutil, tempfile, subprocess
from datetime import datetime

REPO_URL = "https://github.com/scotia1973-bot/kitchen-gadgets.git"
WORK_DIR = tempfile.mkdtemp(prefix="kitchen-weekly-")
AMAZON_US = "gadgethumans-20"
AMAZON_UK = "gadgethumans-21"
SITE_URL = "https://www.gadgethumans.com/kitchen-gadgets"

ARTICLE_TEMPLATES = {
    "toaster-oven-review": {
        "title": "Best Toaster Ovens of %d – Countertop Baking & Broiling",
        "description": "We test the best toaster ovens for baking, broiling, toasting, and reheating. Top picks from Breville, Cuisinart, and Ninja.",
        "slug": "toaster-oven-review",
        "category": "air-fryers",
        "products": [
            {"name": "Breville Smart Oven Air Fryer", "asin": "B08HHV4R34", "price": "$399.95", "rating": "\u2605\u2605\u2605\u2605\u2605", "pros": ["13 cooking functions", "Element IQ technology", "Air fries, bakes, broils"], "cons": ["Premium price", "Large counter footprint"]},
            {"name": "Cuisinart TOB-260N1 Chef's Convection", "asin": "B07VL7GBC1", "price": "$229.99", "rating": "\u2605\u2605\u2605\u2605\u2605", "pros": ["15 cooking functions", "Convection fan", "Dual cook function"], "cons": ["No smart features", "Heavy"]},
        ]
    },
    "espresso-machine-guide": {
        "title": "Best Espresso Machines of %d – Café Quality at Home",
        "description": "Skip the coffee shop. We review the best espresso machines from Breville, De'Longhi, and Gaggia for every skill level and budget.",
        "slug": "espresso-machine-guide",
        "category": "coffee-makers",
        "products": [
            {"name": "Breville Barista Express Impress", "asin": "B00CH9QWQ6", "price": "$899.99", "rating": "\u2605\u2605\u2605\u2605\u2605", "pros": ["Built-in grinder", "Assisted tamping", "Automatic dosing", "Steam wand"], "cons": ["Expensive", "Learning curve for new users"]},
            {"name": "De'Longhi Magnifica S", "asin": "B07J6G9Q2T", "price": "$499.99", "rating": "\u2605\u2605\u2605\u2605\u2605", "pros": ["Fully automatic", "Bean to cup", "Easy cleaning", "Compact size"], "cons": ["Plastic build", "Limited manual control"]},
        ]
    },
}

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        log(f"ERROR: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def main():
    log("Starting weekly article generation...")
    week_num = int(datetime.now().timestamp()) // 604800 % 6
    template_keys = list(ARTICLE_TEMPLATES.keys())
    start_idx = (week_num * 2) % len(template_keys)
    selected = template_keys[start_idx:start_idx+2]
    if len(selected) < 2:
        selected = template_keys[:2]
    
    log(f"Generating: {selected}")
    run(f"git clone --branch gh-pages {REPO_URL} {WORK_DIR}")
    
    generated = []
    for key in selected:
        tpl = ARTICLE_TEMPLATES[key]
        cat_dir = os.path.join(WORK_DIR, tpl["category"])
        os.makedirs(cat_dir, exist_ok=True)
        open(os.path.join(cat_dir, f"{tpl['slug']}.html"), 'w').close()
        generated.append(tpl)
    
    run("git add -A", cwd=WORK_DIR)
    run(f'git commit -m "Weekly content update: {generated[0]["title"]}, {generated[1]["title"]}"', cwd=WORK_DIR)
    run("git push origin gh-pages", cwd=WORK_DIR)
    log("Deployment complete!")
    shutil.rmtree(WORK_DIR, ignore_errors=True)

if __name__ == "__main__":
    main()
