from data.config import OrderStatuses


def get_orders_quantity_by_order_status(orders: list, order_status: str) -> int:
    q: int = 0
    if order_status == OrderStatuses.waiting_for_start:
        for order in orders:
            if order.status == OrderStatuses.waiting_for_start:
                q += 1
    elif order_status == OrderStatuses.in_progress:
        for order in orders:
            if order.status == OrderStatuses.in_progress:
                q += 1
    return q







