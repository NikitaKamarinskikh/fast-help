

def count_rating(current_rating: float, current_orders_quantity: int, value: int):
    total = current_rating * current_orders_quantity
    total += value
    return round(total / (current_orders_quantity + 1), 1)

