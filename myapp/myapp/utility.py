def calculate_total(order_items):
    if not isinstance(order_items, list):
        order_items = list(order_items)  # แปลงเป็นรายการถ้ายังไม่เป็น
    
    total = 0
    for item in order_items:
        if hasattr(item, 'total_price'):  # ตรวจสอบว่ามีฟิลด์ total_price หรือไม่
            total += item.total_price
        else:
            raise ValueError("Item does not have total_price attribute")
    return total