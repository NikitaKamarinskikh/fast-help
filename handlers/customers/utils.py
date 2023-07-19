from data.config import OrderStatuses


def get_orders_quantity_by_order_status(orders: list, order_status: str) -> int:
    quantity = 0
    if order_status == OrderStatuses.waiting_for_start:
        for order in orders:
            if order.status == OrderStatuses.waiting_for_start:
                quantity += 1
    elif order_status == OrderStatuses.in_progress:
        for order in orders:
            if order.status == OrderStatuses.in_progress:
                quantity += 1
    return quantity







