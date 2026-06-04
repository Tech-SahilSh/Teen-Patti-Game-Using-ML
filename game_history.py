import csv
import random

actions = ["chaal", "pack", "show"]
rows = []

for _ in range(1000):
    card_strength = round(random.uniform(0, 1), 2)
    pot_size = random.randint(20, 100)
    player_coin = random.randint(10, 100)
    opponent_coin = random.randint(10, 100)

    # Simple decision logic
    if card_strength > 0.75:
        action = random.choices(["chaal", "show"], weights=[0.6, 0.4])[0]
    elif card_strength < 0.3:
        action = random.choices(["pack", "chaal"], weights=[0.7, 0.3])[0]
    else:
        action = random.choices(actions, weights=[0.5, 0.3, 0.2])[0]

    rows.append([card_strength, pot_size, player_coin, opponent_coin, action])

# Save to CSV file
with open("game_history_1000.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["card_strength", "pot_size", "player_coin", "opponent_coin", "action"])
    writer.writerows(rows)

print("CSV with 1000 rows created: game_history_1000.csv")
