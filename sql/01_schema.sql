PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
  customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  country TEXT NOT NULL,
  region TEXT NOT NULL,
  city TEXT NOT NULL,
  signup_at DATE NOT NULL,
  acquisition_channel_id INTEGER,
  FOREIGN KEY (acquisition_channel_id) REFERENCES channels(channel_id)
);

CREATE TABLE IF NOT EXISTS categories (
  category_id INTEGER PRIMARY KEY AUTOINCREMENT,
  category_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
  product_id INTEGER PRIMARY KEY AUTOINCREMENT,
  sku TEXT UNIQUE NOT NULL,
  product_name TEXT NOT NULL,
  category_id INTEGER NOT NULL,
  cost_price REAL NOT NULL CHECK(cost_price >= 0),
  list_price REAL NOT NULL CHECK(list_price >= 0),
  active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)),
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE IF NOT EXISTS channels (
  channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
  channel_name TEXT UNIQUE NOT NULL,
  channel_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS channel_spend (
  spend_date DATE NOT NULL,
  channel_id INTEGER NOT NULL,
  spend REAL NOT NULL CHECK(spend >= 0),
  impressions INTEGER NOT NULL DEFAULT 0,
  clicks INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (spend_date, channel_id),
  FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);

CREATE TABLE IF NOT EXISTS website_sessions (
  session_date DATE NOT NULL,
  channel_id INTEGER NOT NULL,
  sessions INTEGER NOT NULL CHECK(sessions >= 0),
  add_to_carts INTEGER NOT NULL CHECK(add_to_carts >= 0),
  checkouts INTEGER NOT NULL CHECK(checkouts >= 0),
  conversions INTEGER NOT NULL CHECK(conversions >= 0),
  PRIMARY KEY (session_date, channel_id),
  FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);

CREATE TABLE IF NOT EXISTS orders (
  order_id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER NOT NULL,
  order_datetime DATETIME NOT NULL,
  channel_id INTEGER NOT NULL,
  ship_country TEXT NOT NULL,
  ship_region TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('PAID','PENDING','CANCELLED','REFUNDED')),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);

CREATE TABLE IF NOT EXISTS order_items (
  order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL CHECK(quantity > 0),
  unit_price REAL NOT NULL CHECK(unit_price >= 0),
  discount REAL NOT NULL DEFAULT 0 CHECK(discount >= 0),
  FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS payments (
  payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  paid_amount REAL NOT NULL CHECK(paid_amount >= 0),
  paid_at DATETIME NOT NULL,
  method TEXT NOT NULL CHECK(method IN ('CARD','UPI','COD','PAYPAL','WALLET','OTHER')),
  payment_status TEXT NOT NULL CHECK(payment_status IN ('SUCCESS','PENDING','REFUNDED','FAILED')),
  FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shipping (
  shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER UNIQUE NOT NULL,
  courier TEXT NOT NULL,
  shipped_at DATETIME,
  promised_delivery_date DATE,
  delivered_at DATETIME,
  shipping_cost REAL NOT NULL DEFAULT 0 CHECK(shipping_cost >= 0),
  shipping_status TEXT NOT NULL CHECK(shipping_status IN ('PROCESSING','SHIPPED','DELIVERED','RETURNED','CANCELLED')),
  FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS returns (
  return_id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  return_date DATE NOT NULL,
  reason TEXT NOT NULL,
  refund_amount REAL NOT NULL CHECK(refund_amount >= 0),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS inventory_snapshots (
  snapshot_date DATE NOT NULL,
  product_id INTEGER NOT NULL,
  stock_on_hand INTEGER NOT NULL CHECK(stock_on_hand >= 0),
  reorder_level INTEGER NOT NULL CHECK(reorder_level >= 0),
  PRIMARY KEY (snapshot_date, product_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);
