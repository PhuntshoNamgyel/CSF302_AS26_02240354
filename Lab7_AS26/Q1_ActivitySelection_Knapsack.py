import random


# 1. Greedy activity selection using three rules
def activity_selection(activities, rule):
    if rule == "finish":
        ordered = sorted(activities, key=lambda a: a[1])
    elif rule == "start":
        ordered = sorted(activities, key=lambda a: a[0])
    else:
        ordered = sorted(activities, key=lambda a: a[1] - a[0])

    selected = []

    for activity in ordered:
        start, finish = activity

        if all(finish <= s or start >= f for s, f in selected):
            selected.append(activity)

    return sorted(selected)


# 2. Find counterexamples through random testing
def find_counterexamples(trials=10000):
    found = {}
    rng = random.Random(42)

    for _ in range(trials):
        activities = []

        for _ in range(rng.randint(5, 10)):
            start = rng.randint(0, 20)
            finish = start + rng.randint(1, 10)
            activities.append((start, finish))

        earliest_finish = activity_selection(activities, "finish")

        for rule in ["start", "duration"]:
            other = activity_selection(activities, rule)

            if rule not in found and len(other) < len(earliest_finish):
                found[rule] = (activities, earliest_finish, other)

        if len(found) == 2:
            break

    return found


# 3. Fractional knapsack using value/weight ratio
def fractional_knapsack(items, capacity):
    total_value = 0
    selected = []

    for value, weight in sorted(items, key=lambda x: x[0] / x[1], reverse=True):
        if capacity == 0:
            break

        taken = min(weight, capacity)
        fraction = taken / weight

        total_value += value * fraction
        selected.append((value, weight, round(fraction, 3)))
        capacity -= taken

    return total_value, selected


# 4. Greedy 0/1 knapsack
def greedy_knapsack(items, capacity):
    total_value = 0

    for value, weight in sorted(items, key=lambda x: x[0] / x[1], reverse=True):
        if weight <= capacity:
            total_value += value
            capacity -= weight

    return total_value


# 5. Dynamic programming 0/1 knapsack
def dp_knapsack(items, capacity):
    dp = [0] * (capacity + 1)

    for value, weight in items:
        for w in range(capacity, weight - 1, -1):
            dp[w] = max(dp[w], dp[w - weight] + value)

    return dp[capacity]


# 6. Random testing for worst greedy-to-optimal ratio
def test_knapsack(trials=10000):
    rng = random.Random(42)
    worst_ratio = 1.0
    worst_case = None

    for _ in range(trials):
        capacity = rng.randint(10, 30)

        items = [
            (rng.randint(1, 100), rng.randint(1, capacity))
            for _ in range(rng.randint(4, 10))
        ]

        greedy = greedy_knapsack(items, capacity)
        optimal = dp_knapsack(items, capacity)
        ratio = greedy / optimal

        if ratio < worst_ratio:
            worst_ratio = ratio
            worst_case = (items, capacity, greedy, optimal)

    return worst_ratio, worst_case


# Activity selection
n = int(input("Enter number of activities: "))
activities = []

for i in range(n):
    start, finish = map(int, input(f"Activity {i + 1} (start finish): ").split())
    activities.append((start, finish))

print("\nActivity Selection")
print("Earliest Finish:", activity_selection(activities, "finish"))
print("Earliest Start:", activity_selection(activities, "start"))
print("Shortest Duration:", activity_selection(activities, "duration"))


# Activity selection counterexamples
print("\nRandom Activity Selection Counterexamples")

counterexamples = find_counterexamples()

for rule, (activities, optimal, other) in counterexamples.items():
    print(f"\nRule: {rule}")
    print("Activities:", activities)
    print("Earliest Finish:", optimal, "Count:", len(optimal))
    print(f"{rule.title()}:", other, "Count:", len(other))


# Fractional and 0/1 knapsack example
items = [(60, 10), (100, 20), (120, 30)]
capacity = 50

fractional_value, selected = fractional_knapsack(items, capacity)

print("\nKnapsack Example")
print("Items (value, weight):", items)
print("Capacity:", capacity)
print("Fractional Value:", fractional_value)
print("Selected Fractions:", selected)
print("Greedy 0/1 Value:", greedy_knapsack(items, capacity))
print("DP 0/1 Optimal Value:", dp_knapsack(items, capacity))


# Worst ratio from random testing
print("\nRandom 0/1 Knapsack Comparison")

ratio, case = test_knapsack()

if case:
    items, capacity, greedy, optimal = case

    print("Items:", items)
    print("Capacity:", capacity)
    print("Greedy Value:", greedy)
    print("Optimal DP Value:", optimal)
    print(f"Worst Greedy/Optimal Ratio: {ratio:.4f}")
    print(f"Percentage: {ratio * 100:.2f}%")
else:
    print("No case found where greedy was worse than optimal.")
