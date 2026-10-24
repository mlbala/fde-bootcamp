def calculate_total(price, quantity):
    # name, quantity --> parameter
    total_price_1 = price * quantity
    return total_price_1

value_1 = calculate_total(60, 70)
# print(value_1)
# 60, 70 --> argument

value_2 = calculate_total(1000, 2)

print(value_1+value_2)