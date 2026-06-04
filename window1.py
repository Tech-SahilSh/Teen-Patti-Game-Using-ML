# main.py

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox,
    QHBoxLayout, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QFont
import sys
from game_logic import create_deck, deal_cards, compare_hands, get_ai_action

player_name = ""
player_coins = 100
ai_coins = 100
pot = 0
player_cards = []
ai_cards = []

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Kala Bazari")
        self.setGeometry(300, 200, 500, 300)
        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        self.title_label = QLabel("Welcome to Kala Bazari")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setStyleSheet("color: red;")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setStyleSheet("padding: 8px; font-size: 16px; color: white; background-color: #333;")

        self.start_button = QPushButton("Start Game")
        self.start_button.setStyleSheet("padding: 8px; font-size: 16px; background-color: red; color: white;")

        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.name_input)
        layout.addWidget(self.start_button)
        layout.addStretch()

        self.setLayout(layout)
        self.start_button.clicked.connect(self.launch_game)

    def launch_game(self):
        global player_name
        name = self.name_input.text().strip()
        if name == "":
            QMessageBox.warning(self, "Input Error", "Please enter your name.")
            return
        player_name = name
        self.hide()
        self.game_window = TeenPattiGame()
        self.game_window.show()


class TeenPattiGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teen Patti - Game")
        self.setGeometry(200, 100, 800, 600)
        self.setStyleSheet("background-color: lightgreen;")

        self.player_card_labels = [QLabel() for _ in range(3)]
        self.ai_card_labels = [QLabel() for _ in range(3)]

        self.chaal_btn = QPushButton("Chaal")
        self.pack_btn = QPushButton("Pack")
        self.show_btn = QPushButton("Show")
        for btn in [self.chaal_btn, self.pack_btn, self.show_btn]:
            btn.setEnabled(False)

        self.coin_label = QLabel()
        self.pot_label = QLabel("Pot: 0")

        self.loader_label = QLabel("")
        self.loader_label.setAlignment(Qt.AlignCenter)
        self.loader_label.hide()

        self.setup_layout()
        self.start_game()

    def setup_layout(self):
        main_layout = QGridLayout()

        # Left side (Player)
        player_name_label = QLabel(player_name)
        player_name_label.setFont(QFont("Arial", 14, QFont.Bold))
        profile_icon = QLabel()
        profile_icon.setPixmap(QPixmap("assets/profile.png").scaled(40, 40))

        player_info = QHBoxLayout()
        player_info.addWidget(profile_icon)
        player_info.addWidget(player_name_label)
        player_info.addStretch()

        left_layout = QVBoxLayout()
        left_layout.addLayout(player_info)
        left_layout.addStretch()
        for card in self.player_card_labels:
            left_layout.addWidget(card, alignment=Qt.AlignLeft)
        left_layout.addStretch()

        button_row = QHBoxLayout()
        button_row.addWidget(self.chaal_btn)
        button_row.addWidget(self.pack_btn)
        button_row.addWidget(self.show_btn)
        left_layout.addLayout(button_row)

        # Right side (AI)
        ai_name_label = QLabel("Marco")
        ai_name_label.setFont(QFont("Arial", 14, QFont.Bold))
        ai_icon = QLabel()
        ai_icon.setPixmap(QPixmap("assets/ai.png").scaled(40, 40))

        ai_info = QHBoxLayout()
        ai_info.addWidget(ai_icon)
        ai_info.addWidget(ai_name_label)
        ai_info.addStretch()

        right_layout = QVBoxLayout()
        right_layout.addLayout(ai_info)
        right_layout.addStretch()
        for card in self.ai_card_labels:
            right_layout.addWidget(card, alignment=Qt.AlignRight)
        right_layout.addStretch()

        # Center (Distributor image)
        center_layout = QVBoxLayout()
        self.center_img = QLabel()
        self.center_img.setPixmap(QPixmap("assets/model.png").scaled(100, 100))
        center_layout.addWidget(self.center_img, alignment=Qt.AlignCenter)
        center_layout.addWidget(self.loader_label, alignment=Qt.AlignCenter)
        center_layout.addWidget(self.coin_label, alignment=Qt.AlignCenter)
        center_layout.addWidget(self.pot_label, alignment=Qt.AlignCenter)

        main_layout.addLayout(left_layout, 0, 0)
        main_layout.addLayout(center_layout, 0, 1)
        main_layout.addLayout(right_layout, 0, 2)

        self.setLayout(main_layout)

        self.chaal_btn.clicked.connect(self.chaal_action)
        self.pack_btn.clicked.connect(self.pack_action)
        self.show_btn.clicked.connect(self.show_action)

    def start_game(self):
        global player_coins, ai_coins, pot

        player_coins = 100
        ai_coins = 100
        pot = 20
        player_coins -= 10
        ai_coins -= 10

        self.update_display()
        self.loader_label.setText("Shuffling and distributing cards...")
        self.loader_label.show()
        QTimer.singleShot(3000, self.complete_distribution)

    def complete_distribution(self):
        global player_cards, ai_cards
        deck = create_deck()
        player_cards, ai_cards = deal_cards(deck)

        for i, card in enumerate(player_cards):
            pixmap = QPixmap(card['image'])
            if pixmap.isNull():
                pixmap = QPixmap('assets/card_back.png')
            self.player_card_labels[i].setPixmap(pixmap.scaled(80, 120))

        for i, card in enumerate(ai_cards):
            pixmap = QPixmap(card['image'])
            if pixmap.isNull():
                pixmap = QPixmap('assets/card_back.png')
            self.ai_card_labels[i].setPixmap(pixmap.scaled(80, 120))

        QTimer.singleShot(2000, self.hide_ai_cards)

    def hide_ai_cards(self):
        for card in self.ai_card_labels:
            card.setPixmap(QPixmap("assets/card_back.png").scaled(80, 120))

        self.loader_label.hide()
        QMessageBox.information(self, "Game Started", f"10 coins deducted from both. Pot = {pot}")
        self.enable_action_buttons()

    def update_display(self):
        self.coin_label.setText(f"{player_name}'s Coins: {player_coins} | AI Coins: {ai_coins}")
        self.pot_label.setText(f"Pot: {pot}")

    def enable_action_buttons(self):
        self.chaal_btn.setEnabled(True)
        self.pack_btn.setEnabled(True)
        self.show_btn.setEnabled(True)

    def disable_action_buttons(self):
        self.chaal_btn.setEnabled(False)
        self.pack_btn.setEnabled(False)
        self.show_btn.setEnabled(False)

    def chaal_action(self):
        global player_coins, pot
        if player_coins >= 10:
            player_coins -= 10
            pot += 10
            self.update_display()
            QMessageBox.information(self, "Chaal", "You played chaal. 10 coins added to pot.")
            self.ai_turn()
        else:
            QMessageBox.warning(self, "Not enough coins", "You don't have enough coins to chaal.")

    def pack_action(self):
        QMessageBox.information(self, "Pack", "You packed. You lost this round.")
        self.disable_action_buttons()
        self.end_round(forced_winner="ai")

    def show_action(self):
        self.disable_action_buttons()
        self.ai_turn(force_show=True)

    def ai_turn(self, force_show=False):
        global ai_cards, pot, ai_coins, player_coins

        if force_show:
            ai_move = "show"
        else:
            ai_move = get_ai_action(ai_cards, pot, ai_coins, player_coins)

        QMessageBox.information(self, "AI Move", f"AI played: {ai_move.upper()}")

        if ai_move == "chaal":
            ai_coins -= 10
            pot += 10
            self.update_display()
        elif ai_move == "pack":
            self.end_round(forced_winner="player")
            return

        if ai_move == "show":
            self.end_round()

    def end_round(self, forced_winner=None):
        global player_coins, ai_coins, pot, player_cards, ai_cards

        for i, card in enumerate(ai_cards):
            pixmap = QPixmap(card['image'])
            self.ai_card_labels[i].setPixmap(pixmap.scaled(80, 120))

        if forced_winner:
            winner = forced_winner
        else:
            winner = compare_hands(player_cards, ai_cards)

        if winner == "player":
            player_coins += pot
            message = f"{player_name} wins the round and gets {pot} coins!"
        elif winner == "ai":
            ai_coins += pot
            message = f"AI wins the round and gets {pot} coins!"
        else:
            player_coins += pot // 2
            ai_coins += pot // 2
            message = f"It's a draw! Pot split."

        pot = 0
        self.update_display()
        QMessageBox.information(self, "Round Result", message)

        if player_coins < 10 or ai_coins < 10:
            QMessageBox.information(self, "Game Over", "Game Over! One player is out of coins.")
            self.close()
        else:
            reply = QMessageBox.question(self, "Play Again?", "Do you want to play another round?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.start_new_round()
            else:
                self.close()

    def start_new_round(self):
        self.start_game()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome = WelcomeWindow()
    welcome.show()
    sys.exit(app.exec_())
