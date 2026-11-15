# food

**nyansatek.food**: order from restaurants and eateries, the food sibling of nyansatek.store.

- It uses the same database as Shop, Store and nyansatek.rest. It lists dishes that restaurants
  (organizations with `vertical = 'food'`) have put in a food category, through the
  `food_listings` and `food_restaurants` database functions.
- Riders, pickup points, delivery zones, order tracking and the ops dashboard are shared with
  nyansatek.store (the rider app and ops dashboard live at nyansatek.store/rider and /ops).
- `index.html` is generated from Store's `index.html` by `tools/build_from_store.py`.
- `assets/cat-<slug>.mp4` is the hero reel for each food category.
