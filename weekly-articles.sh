#!/bin/bash
# ============================================================
# Weekly Kitchen Gadgets Article Generator - Wednesdays 9:00 AM
# ============================================================
set -e
cd /Users/scottwishart/kitchen-gadgets
python3 weekly_articles.py
echo "Done! Site updated at https://www.gadgethumans.com/kitchen-gadgets/"
