# all possible item prices
price_range = [i * 0.01 for i in range(1, 778)]

# variables for the best combination and minimal optimization function value
best_combination = None
min_opt_val = float('inf')

# exhaustive search using nested loops
for p1 in price_range:
    for p2 in price_range:
        for p3 in price_range:
            for p4 in price_range:
                # calculating the optimization function value
                opt_val = (p1 + p2 + p3 + p4 - 7.77) ** 2 + (p1 * p2 * p3 * p4 - 7.77) ** 2

                # updating the best combination
                if opt_val < min_opt_val:
                    min_opt_val = opt_val
                    best_combination = (p1, p2, p3, p4)

print(f"Best answer: {best_combination}")
