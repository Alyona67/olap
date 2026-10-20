"""
Генератор учебных данных для домена "Розница".
Создаёт 9 таблиц в data/raw/. (Большой объём для реалистичных графиков)
"""
import pandas as pd
import random
from datetime import date, timedelta

random.seed(42)

# ============ ИЗМЕРЕНИЯ ============

# --- dim_product: 1500 товаров ---
categories = ["Молочка", "Хлеб", "Напитки", "Бакалея", "Мясо", "Овощи", "Фрукты", "Заморозка", "Бытовая химия", "Гигиена"]
brands = [
    "LocalFarm", "BakerCo", "JuiceBar", "Aqua", "SweetDay", "TeaHouse", "MeatPro", "VeggieLand", "FoodMaster", 
    "FreshLine", "EcoProduct", "DailyFood", "MilkWay", "BreadHouse", "WaterLife", "CleanHome", "CarePlus"
]
products = []
for i in range(1, 1501):                           # 1500 товаров
    products.append({
        "product_id": 100 + i,
        "product_name": f"Товар {i}",
        "category": random.choice(categories),
        "brand": random.choice(brands),
    })
pd.DataFrame(products).to_csv("data/raw/dim_product.csv", index=False)
print(f"dim_product.csv     — {len(products)} строк")

# --- dim_store: 25 магазинов ---
cities = ["Гродно", "Минск", "Брест", "Гомель", "Витебск", "Могилёв", "Барановичи", "Бобруйск"]
regions = ["Запад", "Центр", "Восток", "Юг"]
stores = []
for i in range(1, 26):
    stores.append({
        "store_id": i,
        "store_name": f"Магазин {i}",
        "city": random.choice(cities),
        "region": random.choice(regions),
    })
pd.DataFrame(stores).to_csv("data/raw/dim_store.csv", index=False)
print(f"dim_store.csv       — {len(stores)} строк")

# --- dim_date: 365 дней (2024) ---
month_names = ["", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
               "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
dates = []
d = date(2024, 1, 1)
for i in range(365):
    dates.append({
        "date_id": int(d.strftime("%Y%m%d")),
        "full_date": d.isoformat(),
        "year": d.year,
        "month": d.month,
        "month_name": month_names[d.month],
        "day_of_week": d.isoweekday(),
    })
    d += timedelta(days=1)
pd.DataFrame(dates).to_csv("data/raw/dim_date.csv", index=False)
print(f"dim_date.csv        — {len(dates)} строк")

# --- dim_customer: 50000 клиентов ---
print("Генерация 50 000 клиентов...")
segments = ["Новый", "Постоянный", "VIP"]
genders = ["М", "Ж"]
customers = []
for i in range(1, 50001):
    customers.append({
        "customer_id": i,
        "customer_name": f"Клиент {i}",
        "city": random.choice(cities),
        "segment": random.choice(segments),
        "gender": random.choice(genders),
    })
pd.DataFrame(customers).to_csv("data/raw/dim_customer.csv", index=False)
print(f"dim_customer.csv    — {len(customers)} строк")

# --- dim_employee: 100 сотрудников ---
positions = ["Продавец", "Кассир", "Менеджер", "Старший смены"]
employees = []
for i in range(1, 101):
    employees.append({
        "employee_id": i,
        "employee_name": f"Сотрудник {i}",
        "position": random.choice(positions),
        "store_id": random.randint(1, 25),
    })
pd.DataFrame(employees).to_csv("data/raw/dim_employee.csv", index=False)
print(f"dim_employee.csv    — {len(employees)} строк")

# --- dim_promotion: 20 акций ---
promo_types = ["Скидка 10%", "Скидка 20%", "2 по цене 1", "Подарок", "Скидка 50%"]
promotions = []
for i in range(1, 21):
    promotions.append({
        "promotion_id": i,
        "promotion_name": f"Акция {i}",
        "promo_type": random.choice(promo_types),
        "discount_pct": random.choice([10, 15, 20, 30, 50]),
    })
pd.DataFrame(promotions).to_csv("data/raw/dim_promotion.csv", index=False)
print(f"dim_promotion.csv   — {len(promotions)} строк")

# ============ ФАКТЫ ============

# --- fact_sales: 500000 чеков ---
print("Генерация 500 000 чеков... (займёт около 20-30 секунд)")
sales = []
sale_id = 1

for _ in range(500000):                            # 500 000 чеков!
    n_items = random.randint(1, 5)                 # 1–5 товаров в чеке
    customer = random.randint(1, 50000)            # случайный клиент
    store = random.randint(1, 25)
    date_ = random.choice(dates)["date_id"]
    employee = random.randint(1, 100)
    promo = random.choice([None] * 3 + list(range(1, 21))) # ~25% чеков со скидкой
    
    for _ in range(n_items):
        qty = random.randint(1, 10)
        price = round(random.uniform(3, 100), 2)
        sales.append({
            "sale_id": sale_id,
            "date_id": date_,
            "store_id": store,
            # Теперь выбираем из 1500 товаров (ID от 101 до 1600)
            "product_id": random.randint(101, 1600), 
            "customer_id": customer,
            "employee_id": employee,
            "promotion_id": promo,
            "qty": qty,
            "amount": round(qty * price, 2),
        })
    sale_id += 1

pd.DataFrame(sales).to_csv("data/raw/fact_sales.csv", index=False)
print(f"fact_sales.csv      — {len(sales)} строк ({sale_id - 1} чеков)")

# --- fact_returns: 50000 возвратов ---
returns = []
for i in range(1, 50001):                           # 50 000 возвратов
    sale = random.choice(sales)
    returns.append({
        "return_id": i,
        "sale_id": sale["sale_id"],
        "date_id": sale["date_id"],
        "store_id": sale["store_id"],
        "product_id": sale["product_id"],
        "qty": random.randint(1, 3),
        "amount": round(random.uniform(3, 100), 2),
        "reason": random.choice(["Брак", "Не подошло", "Передумал", "Просрочка"]),
    })
pd.DataFrame(returns).to_csv("data/raw/fact_returns.csv", index=False)
print(f"fact_returns.csv    — {len(returns)} строк")

# --- fact_inventory: остатки на складе ---
print("Генерация остатков на складе...")
inventory = []
inv_id = 1
sample_dates = random.sample(dates, 30)            # 30 контрольных дней в году
for store_id in range(1, 26):
    # Теперь проверяем наличие 1500 товаров
    for product_id in range(101, 1601):
        if random.random() < 0.9:                  # 90% товаров есть на складе
            for d in sample_dates:
                inventory.append({
                    "inventory_id": inv_id,
                    "date_id": d["date_id"],
                    "store_id": store_id,
                    "product_id": product_id,
                    "qty_on_hand": random.randint(0, 300),
                })
                inv_id += 1
                
pd.DataFrame(inventory).to_csv("data/raw/fact_inventory.csv", index=False)
print(f"fact_inventory.csv  — {len(inventory)} строк")

print("\n" + "=" * 40)
print("Готово! Создано 9 файлов в data/raw/")
print("=" * 40)