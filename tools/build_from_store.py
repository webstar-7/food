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


def cut(start, end, keep_end=True):
    """Remove the text from `start` up to `end` (kept unless keep_end=False); both must be there once."""
    global s
    assert s.count(start) == 1, (start[:90], s.count(start))
    a = s.index(start)
    b = s.index(end, a)
    s = s[:a] + (s[b:] if keep_end else s[b + len(end):])


# ---------------------------------------------------------------- Store's pop-up tile advertises nyansatek.food: not on Food itself
cut('/* pop-up tile linking to nyansatek.food', '</style>')
cut('<div class="foodtile" id="foodtile">', '</div>\n', keep_end=False)
cut('// ---------- pop-up tile for nyansatek.food ----------', '// GitHub Pages hosting')
sub('  foodTile();\n', '')

# ---------------------------------------------------------------- "List your shop" becomes "List your restaurant"
# Store has a #/partners page for shops (NYANSATEK POS, source=store). Food swaps it for the restaurant version:
# NYANSATEK Restaurant checkout with source=food, so the account is made with the Online Menu add-on switched on
# (included) and the request to join nyansatek.food already sent; the NYANSATEK team approves it in /ops.
# Done before the word changes below, so they never rewrite the Food text.
cut('// ---------- "List your shop" ----------', '// ---------- listings ----------')
sub("// ---------- listings ----------", """// ---------- "List your restaurant" ----------
// Listing is free and needs no software. Customers pay NYANSATEK by MoMo; the team places each order with the
// restaurant by phone, calls a rider, and pays the restaurant its menu prices by close of business.
// NYANSATEK Restaurant is optional.
const JOIN_CHECKOUT = 'https://nyansatek.systems/checkout.html?product=rest&source=food&plan=';
const JOIN_WHATSAPP = 'https://wa.me/233536340578?text=' + encodeURIComponent('Hello NYANSATEK, I want to list my restaurant on nyansatek.food.');
function partnersPage() {
  document.title = 'List your restaurant · nyansatek.food';
  app.innerHTML = `<div class="join">
    <div class="hero"><b style="display:block;font-size:1.5rem;line-height:1.2;">Bring your kitchen to nyansatek.food</b>
      <p style="max-width:56ch;">Hungry customers near you order here. They pay NYANSATEK by MoMo, we place each order with you by phone
      and send a rider to collect it. You get your full menu price by close of business.</p>
      <div class="join-cta"><a class="btn" style="background:#fff;color:var(--p);" href="${JOIN_WHATSAPP}" target="_blank" rel="noopener">List my restaurant</a>
        <a class="btn" style="background:transparent;border:1px solid rgba(255,255,255,.65);" href="tel:0536340578">Call 053 634 0578</a></div></div>

    <h2 class="sec">How it works</h2>
    <ol class="join-steps">
      <li><b>Get listed</b>Call or WhatsApp us. Listing is free and you need no new software: we put your menu up for you.</li>
      <li><b>Your menu goes up</b>With your prices and photos. On NYANSATEK Restaurant you can update it yourself at nyansatek.rest.</li>
      <li><b>Customers order and pay us</b>By MoMo, before anything happens. No unpaid or prank orders reach your kitchen.</li>
      <li><b>We call you, then a rider</b>We place the order with you by phone and send a rider to collect it.</li>
    </ol>

    <h2 class="sec">What you get</h2>
    <div class="join-gets">
      <div><b>Listed on nyansatek.food</b>Your dishes in front of customers searching for food near them.</div>
      <div><b>Your full price, every day</b>You receive exactly your menu prices by MoMo by close of business.</div>
      <div><b>Paid before you cook</b>Every order is paid by MoMo first. No pay on delivery, no prank orders.</div>
      <div><b>Delivery arranged for you</b>We call a rider to collect and deliver. The customer pays the rider's fee.</div>
      <div><b>No new software needed</b>Keep running your kitchen your way. We take the orders and call you.</div>
      <div><b>NYANSATEK Restaurant, if you want it</b>Till, kitchen screen and your own online menu page, with sales and profit reports.</div>
    </div>

    <h2 class="sec">What it costs</h2>
    <p style="margin:6px 0 10px;line-height:1.5;"><b>Listing on nyansatek.food is free.</b></p>
    <div class="join-price">
      <div class="box"><div class="note">NYANSATEK Restaurant (optional) · monthly</div><div class="amt">GH₵200</div><div class="note">per month</div>
        <a class="btn" href="${JOIN_CHECKOUT}standard">Choose monthly</a></div>
      <div class="box"><div class="note">NYANSATEK Restaurant (optional) · yearly, two months free</div><div class="amt">GH₵2,000</div><div class="note">per year</div>
        <a class="btn" href="${JOIN_CHECKOUT}yearly">Choose yearly</a></div>
    </div>
    <p class="note">No setup fee. Cancel anytime.</p>

    <div class="box"><b>Already use NYANSATEK Restaurant?</b>
      <p class="note" style="margin-top:4px;">Your online menu is already switched on, free. Call or WhatsApp us on <a href="tel:0536340578">053 634 0578</a>
      and we will list you on nyansatek.food.</p></div>
  </div>`;
}

// ---------- listings ----------""")
sub('.join-band{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin:22px 0 34px;padding:16px 18px;border-radius:14px;background:#fbf6ea;border:1px solid #ecd9a8;color:#3d2c06;',
    '.join-band{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin:22px 0 34px;padding:16px 18px;border-radius:14px;background:#fff4e6;border:1px solid #f6d3a8;color:#5a2206;')
sub('/* "List your shop" page and the band on the home page */', '/* "List your restaurant" page and the band on the home page */')

# Home: a row of the restaurants that are live, then the "List your restaurant" band in place of Store's shop band.
a = s.index('<a class="join-band" href="#/partners" data-link><span><b>Own a shop?</b>')
b = s.index("playHeroReel();\n}", a) + len("playHeroReel();\n}")
s = s[:a] + """<div id="rest-row"></div>
    <a class="join-band" href="#/partners" data-link><span><b>Own a restaurant, chop bar or eatery?</b>
      Put your menu in front of hungry customers near you.</span><span class="join-go">List your restaurant →</span></a>`, {});
  playHeroReel();
  // Restaurants that are live, each linking to its own page. Loaded after the page so a slow answer never holds the menu back.
  sb.rpc('food_restaurants').then(({ data }) => {
    const el = document.getElementById('rest-row');
    if (!el || !data || !data.length) return;
    el.innerHTML = `<h2 class="sec">Restaurants</h2><div class="cats">${data.map(r =>
      `<a class="cat" href="#/r/${E(r.slug)}" data-link>${E(r.name)}<small>${r.dishes} dish${r.dishes === 1 ? '' : 'es'}${r.tagline ? ' · ' + E(r.tagline) : ''}</small></a>`).join('')}</div>`;
  }, () => {});
}""" + s[b:]

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
    ('content="Shop from trusted local shops in one place. Pay by MoMo and a rider brings it to your door."',
     'content="Order from restaurants and eateries near you. Pay by MoMo and a rider brings it to your door."'),
    ('content="NYANSATEK Store"', 'content="NYANSATEK Food"'),
    ('nyansatek<span>.store</span>', 'nyansatek<span>.food</span>'),
    ('placeholder="Search products"', 'placeholder="Search dishes"'),
    ('Every shop on nyansatek.store runs on NYANSATEK POS, so stock is live.', 'Every restaurant on nyansatek.food is checked by the NYANSATEK team.'),
    ('>List your shop</a>', '>List your restaurant</a>'),
    ("document.title = 'nyansatek.store · Shop from trusted local shops';", "document.title = 'nyansatek.food · Order from restaurants near you';"),
    ("gridPage('New on nyansatek.store',", "gridPage('Fresh on nyansatek.food',"),
    ('<b>Shop from trusted local shops, in one place.</b>', '<b>Order from restaurants and eateries near you.</b>'),
    ('<p>Live stock from every shop. Pay by MoMo and a rider brings it to your door.</p>',
     '<p>Dishes from kitchens near you. Pay by MoMo and a rider brings it to your door.</p>'),
    ('A short tour: browse live stock, pay by MoMo and track your order', 'A short tour: browse dishes, pay by MoMo and track your order'),
    ('<h2 class="sec">Shop by category</h2>', '<h2 class="sec">Order by category</h2>'),
    ("'All products'", "'All dishes'"),
    ('This shop is not on nyansatek.store.', 'This restaurant is not on nyansatek.food.'),
    ('This product is no longer available.', 'This dish is no longer available.'),
    ('<p class="note">Sold by <a href="#/shop/${E(p.shop_slug)}" data-link>', '<p class="note">From <a href="#/r/${E(p.shop_slug)}" data-link>'),
    ('Your cart is empty. <a href="#/" data-link>Start shopping</a>', 'Your cart is empty. <a href="#/" data-link>See what is cooking</a>'),
    ("'Shop confirmed'", "'Restaurant confirmed'"), ("'Packed and ready'", "'Cooked and packed'"),
    ("'Returned to shop'", "'Returned to restaurant'"),
    ("if (path[0] === 'shop') return shopPage(path[1]);", "if (path[0] === 'r' || path[0] === 'shop') return shopPage(path[1]);"),
]:
    sub(old, new, count=s.count(old) or 1)
s = s.replace('the shop', 'the restaurant')
s = s.replace('The shop', 'The restaurant')
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

open(f'{OUT}/index.html', 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- manifest, service worker, domain
json.dump({
    "name": "nyansatek.food", "short_name": "NYANSATEK Food",
    "description": "Order from restaurants and eateries near you. Pay by MoMo and a rider brings it to your door.",
    "id": "./", "start_url": "./", "scope": "./", "display": "standalone", "orientation": "any",
    "background_color": "#d4570e", "theme_color": "#d4570e", "categories": ["food"],
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]},
    open(f'{OUT}/manifest.json', 'w'), indent=2)
open(f'{OUT}/manifest.json', 'a').write('\n')
w = open(f'{SRC}/sw.js', encoding='utf-8').read()
for old, new in [("/* nyansatek.store service worker", "/* nyansatek.food service worker"),
                 ("k.startsWith('nyansatek-store-')", "k.startsWith('nyansatek-food-')"), ("'assets/store-reel.jpg'", "'assets/food-reel.jpg'")]:
    assert w.count(old) == 1, old
    w = w.replace(old, new)
# Store bumps its cache version (v1, v2, ...) whenever installed apps must refresh; Food follows the same number.
w, n = re.subn(r"'nyansatek-store-v(\d+)'", r"'nyansatek-food-v\1'", w)
assert n == 1, 'service worker VERSION not found'
open(f'{OUT}/sw.js', 'w', encoding='utf-8').write(w)
open(f'{OUT}/CNAME', 'w').write('nyansatek.food\n')
print('food built:', len(s), 'bytes')
