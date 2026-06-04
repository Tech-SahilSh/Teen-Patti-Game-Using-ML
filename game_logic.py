import random
import os

CARD_FOLDER = 'assets/cards'

def create_deck():
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    deck = []
    for suit in suits:
        for rank in ranks:
            filename = f"{rank}_of_{suit}.png"
            image_path = os.path.join(CARD_FOLDER, filename)
            if os.path.exists(image_path):
                deck.append({
                    'code': f"{rank[0].upper()}{suit[0].upper()}",
                    'rank': rank,
                    'suit': suit,
                    'value': get_card_value_from_rank(rank),
                    'image': image_path
                })
            else:
                print(f"❌ Image not found: {image_path}")
    return deck

def get_card_value_from_rank(rank):
    rank = rank.lower()
    value_map = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '10': 10,
        'jack': 11, 'queen': 12, 'king': 13, 'ace': 14
    }
    return value_map.get(rank, 0)

def deal_cards(deck):
    random.shuffle(deck)
    return deck[:3], deck[3:6]

def compare_hands(player_cards, ai_cards):
    player_rank = evaluate_hand(player_cards)
    ai_rank = evaluate_hand(ai_cards)

    if player_rank > ai_rank:
        return "player"
    elif ai_rank > player_rank:
        return "ai"
    else:
        # Tie-breaker: compare highest cards
        player_values = sorted([card['value'] for card in player_cards], reverse=True)
        ai_values = sorted([card['value'] for card in ai_cards], reverse=True)
        for pv, av in zip(player_values, ai_values):
            if pv > av:
                return "player"
            elif av > pv:
                return "ai"
        return "draw"

def evaluate_hand(cards):
    values = sorted([card['value'] for card in cards])
    suits = [card['suit'] for card in cards]

    is_sequence = values[2] - values[0] == 2 and len(set(values)) == 3
    is_ace_low_straight = set(values) == {2, 3, 14}  # A, 2, 3
    is_flush = len(set(suits)) == 1
    counts = {v: values.count(v) for v in values}

    # Trail (Three of a kind)
    if len(counts) == 1:
        return 6
    # Pure Sequence (Straight + Flush)
    if (is_sequence or is_ace_low_straight) and is_flush:
        return 5
    # Sequence (Straight)
    if is_sequence or is_ace_low_straight:
        return 4
    # Color (Flush)
    if is_flush:
        return 3
    # Pair
    if 2 in counts.values():
        return 2
    # High Card
    return 1

def get_card_value(code):
    value_map = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '1': 10,
        'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }
    return value_map.get(code[0].upper(), 0)

def get_ai_action(ai_cards, pot, ai_coins, player_coins):
    # Improved basic AI logic based on hand strength
    strength = evaluate_hand(ai_cards)
    if strength >= 5:
        return "chaal"
    elif strength >= 3:
        return "show"
    else:
        return "pack"
