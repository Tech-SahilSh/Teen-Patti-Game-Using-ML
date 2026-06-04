# ai_model.py

import joblib
import numpy as np

# Model ko load karo
model = joblib.load("ai_model.pkl")

# Output label mapping (reverse from training)
action_map = {
    0: "chaal",
    1: "pack",
    2: "show"
}

def predict_ai_move(card_strength, pot_size, ai_coin, player_coin):
    """
    AI ka move predict karta hai.
    
    Parameters:
        card_strength (float): AI ke cards ki strength (0 to 1)
        pot_size (int): current pot size
        ai_coin (int): AI ke paas kitne coin bache hain
        player_coin (int): player ke paas coin

    Returns:
        action (str): 'chaal', 'pack', or 'show'
    """
    features = np.array([[card_strength, pot_size, ai_coin, player_coin]])
    prediction = model.predict(features)[0]
    return action_map[prediction]

# Example test (remove this when using in actual game)
if __name__ == "__main__":
    move = predict_ai_move(0.75, 40, 80, 70)
    print("AI Move:", move)
