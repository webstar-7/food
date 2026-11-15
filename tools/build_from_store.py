"""Build nyansatek.food (order from restaurants) from the nyansatek.store source.

nyansatek.food is not written by hand: it is Store's index.html with a fixed list of changes applied.
To bring a Store update across, clone webstar-7/nyansatek-market next to this repository and run:

    python3 tools/build_from_store.py

Reads  ../nyansatek-market  (Store, untouched; override with STORE_DIR)
Writes this repository      (index.html, sw.js, manifest.json)
Every replacement is asserted, so a change in Store that this script no longer matches fails loudly.
"""
import json, os, re

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get('STORE_DIR', os.path.join(os.path.dirname(OUT), 'nyansatek-market'))
s = open(f'{SRC}/index.html', encoding='utf-8').read()


def sub(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (old[:90], n, 'expected', count)
    s = s.replace(old, new)


def sub_any(old, new):
    global s
    assert s.count(old) >= 1, old[:90]
    s = s.replace(old, new)


# ---------------------------------------------------------------- colours: Store is navy, Food is orange
sub(":root{--p:#17264a;--a:#d1a03a;", ":root{--p:#c14d0e;--a:#ffe2b8;")
sub('<meta name="theme-color" content="#17264a">', '<meta name="theme-color" content="#d4570e">')
sub(".hero{background:linear-gradient(135deg,#17264a,#22386b);", ".hero{background:linear-gradient(135deg,#cf5a10,#8a3409);")
sub("background:#0d1630;}", "background:#4a1c05;}")
sub(".btn.gold{background:var(--a);color:#1a1405;}", ".btn.gold{background:var(--p);color:#fff;}")
sub(".steps li.now .dot{background:var(--a);box-shadow:0 0 0 4px rgba(209,160,58,.25);}", ".steps li.now .dot{background:#e08a1e;box-shadow:0 0 0 4px rgba(224,138,30,.25);}")
sub(".cartbtn{background:var(--a);color:#1a1405;", ".cartbtn{background:var(--a);color:#5a2206;")

# ---------------------------------------------------------------- data: food categories and food listings
sub(".eq('active', true).eq('vertical', 'shop')", ".eq('active', true).eq('vertical', 'food')")
sub("sb.rpc('market_listings',", "sb.rpc('food_listings',")

# ---------------------------------------------------------------- words
for old, new in [
    ('<title>nyansatek.store · Shop from trusted local shops</title>', '<title>nyansatek.food · Order from restaurants near you</title>'),
    ('content="Shop from trusted local shops in one place. Delivery by NYANSATEK riders or pickup at NYANSATEK points. Pay by MoMo or on delivery."',
     'content="Order from restaurants and eateries near you. Delivery by NYANSATEK riders or pickup at NYANSATEK points. Pay by MoMo or on delivery."'),
    ('content="NYANSATEK Store"', 'content="NYANSATEK Food"'),
    ('nyansatek<span>.store</span>', 'nyansatek<span>.food</span>'),
    ('placeholder="Search products"', 'placeholder="Search dishes"'),
    ('Every shop on nyansatek.store runs on NYANSATEK POS, so stock is live.', 'Every restaurant on nyansatek.food runs on NYANSATEK Restaurant, so the menu is live.'),
    ('>Sell on nyansatek.store</a>', '>List your restaurant</a>'),
    ("document.title = 'nyansatek.store · Shop from trusted local shops';", "document.title = 'nyansatek.food · Order from restaurants near you';"),
    ("gridPage('New on nyansatek.store',", "gridPage('Fresh on nyansatek.food',"),
    ('<b>Shop from trusted local shops, in one place.</b>', '<b>Order from restaurants and eateries near you.</b>'),
    ('<p>Live stock from every shop. Delivery by NYANSATEK riders or pickup at a NYANSATEK point. Pay by MoMo or when you receive it.</p>',
     '<p>Live menus from every kitchen. Delivery by NYANSATEK riders or pickup at a NYANSATEK point. Pay by MoMo or when you receive it.</p>'),
    ('A short tour: browse live stock, pay by MoMo or on delivery, track your order, or collect at a pickup point', 'A short tour: browse dishes, pay by MoMo or on delivery, track your order, or collect at a pickup point'),
    ('<h2 class="sec">Shop by category</h2>', '<h2 class="sec">Order by category</h2>'),
    ("'All products'", "'All dishes'"),
    ('This shop is not on nyansatek.store.', 'This restaurant is not on nyansatek.food.'),
    ('This product is no longer available.', 'This dish is no longer available.'),
    ('<p class="note">Sold by <a href="#/shop/${E(p.shop_slug)}" data-link>', '<p class="note">From <a href="#/r/${E(p.shop_slug)}" data-link>'),
    ('Your cart is empty. <a href="#/" data-link>Start shopping</a>', 'Your cart is empty. <a href="#/" data-link>See what is cooking</a>'),
    ("Each shop's items are ordered and delivered separately.", "Each restaurant's dishes are ordered and delivered separately."),
    ("'Shop confirmed'", "'Restaurant confirmed'"), ("'Packed and ready'", "'Cooked and packed'"),
    ("'Returned to shop'", "'Returned to restaurant'"),
    ("if (path[0] === 'shop') return shopPage(path[1]);", "if (path[0] === 'r' || path[0] === 'shop') return shopPage(path[1]);"),
]:
    sub(old, new, count=s.count(old) or 1)
sub_any("the shop's", "the restaurant's")
sub_any('the shop', 'the restaurant')
sub_any('The shop', 'The restaurant')
sub_any('nyansatek.store', 'nyansatek.food')
sub_any('assets/store-reel', 'assets/food-reel')

# ---------------------------------------------------------------- category heroes: one reel per food category
a = s.index("const CAT_REELS = {")
b = s.index("};", a) + 2
s = s[:a] + """const CAT_REELS = {
  'local-dishes': 'Banku, fufu, kenkey and more.',
  'rice-dishes': 'Jollof, waakye, fried rice.',
  'soups-stews': 'Light soup, groundnut, palm nut.',
  'grills-khebab': 'Hot off the fire.',
  'fast-food': 'Burgers, pizza, fried chicken.',
  'breakfast': 'Start the day right.',
  'pastries-snacks': 'Pies, doughnuts, small chops.',
  'drinks-juices': 'Sobolo, fresh juice, smoothies.' };""" + s[b:]
sub("<p>Live stock from every shop that sells ${E(top.name.toLowerCase())}. Delivery by NYANSATEK riders or pickup at a NYANSATEK point.</p>",
    "<p>${E(top.name)} from every kitchen that serves them. Delivery by NYANSATEK riders or pickup at a NYANSATEK point.</p>")

# ---------------------------------------------------------------- home: a row of the restaurants that are live
sub("""join('')}</div>`, {});
  playHeroReel();
}""", """join('')}</div>
    <div id="rest-row"></div>`, {});
  playHeroReel();
  // Restaurants that are live, each linking to its own page. Loaded after the page so a slow answer never holds the menu back.
  sb.rpc('food_restaurants').then(({ data }) => {
    const el = document.getElementById('rest-row');
    if (!el || !data || !data.length) return;
    el.innerHTML = `<h2 class="sec">Restaurants</h2><div class="cats">${data.map(r =>
      `<a class="cat" href="#/r/${E(r.slug)}" data-link>${E(r.name)}<small>${r.dishes} dish${r.dishes === 1 ? '' : 'es'}${r.tagline ? ' · ' + E(r.tagline) : ''}</small></a>`).join('')}</div>`;
  }, () => {});
}""")

open(f'{OUT}/index.html', 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- manifest, service worker, domain
json.dump({
    "name": "nyansatek.food", "short_name": "NYANSATEK Food",
    "description": "Order from restaurants and eateries near you. Delivery by NYANSATEK riders or pickup at NYANSATEK points.",
    "id": "./", "start_url": "./", "scope": "./", "display": "standalone", "orientation": "any",
    "background_color": "#d4570e", "theme_color": "#d4570e", "categories": ["food"],
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]},
    open(f'{OUT}/manifest.json', 'w'), indent=2)
open(f'{OUT}/manifest.json', 'a').write('\n')
w = open(f'{SRC}/sw.js', encoding='utf-8').read()
for old, new in [("/* nyansatek.store service worker", "/* nyansatek.food service worker"), ("'nyansatek-store-v1'", "'nyansatek-food-v1'"),
                 ("k.startsWith('nyansatek-store-')", "k.startsWith('nyansatek-food-')"), ("'assets/store-reel.jpg'", "'assets/food-reel.jpg'")]:
    assert w.count(old) == 1, old
    w = w.replace(old, new)
open(f'{OUT}/sw.js', 'w', encoding='utf-8').write(w)
open(f'{OUT}/CNAME', 'w').write('nyansatek.food\n')
print('food built:', len(s), 'bytes')
