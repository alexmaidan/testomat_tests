index = 10
print(index)

price = 10.99
print(price)

price_from_text = float("10.98")
print(price_from_text + 2)

index_of_page = ("2")
print(int(index_of_page) + 1)

actual_prices: list[str] = ["10.88", "42.38", "19.43"]

print(actual_prices)
print(max(actual_prices))


def is_first_price_is_higher(t_prices: list[str]):
    return t_prices[0] == max(t_prices)


print(is_first_price_is_higher(actual_prices))

actual_prices.sort(reverse=True)
print(actual_prices)
#
print(is_first_price_is_higher(actual_prices))
