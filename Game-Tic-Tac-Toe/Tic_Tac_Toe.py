from PyQt5 import QtWidgets
import GameDesign
import sys
import random
from math import inf as infinity

from PyQt5.QtGui import QIcon


class GameApp(QtWidgets.QWidget, GameDesign.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('rick.ico'))
        # Подключение клик-сигнала кнопки старт
        self.btn_start.clicked.connect(self.start_click)
        # Подключение клик-сигнала кнопки сброса счета
        self.btn_reset.clicked.connect(self.reset_click)
        # подключение клик-сигналов игрового поля
        self.pB1.clicked.connect(self.button_click)
        self.pB2.clicked.connect(self.button_click)
        self.pB3.clicked.connect(self.button_click)
        self.pB4.clicked.connect(self.button_click)
        self.pB5.clicked.connect(self.button_click)
        self.pB6.clicked.connect(self.button_click)
        self.pB7.clicked.connect(self.button_click)
        self.pB8.clicked.connect(self.button_click)
        self.pB9.clicked.connect(self.button_click)
        # Все кнопки поля отключаем
        for i in range(1, 10):
            command = f"self.pB{i}.setEnabled(False)"
            exec(command)
        # инициализация счета
        self.X_score = 0
        self.O_score = 0

    def start_click(self):
        # Инициализация настроек игры
        # print('The Game had starting')
        self.stop_game = False
        # инициализация массива имитирующего игровое поле
        self.board = [' '] * 9
        # инициализация игроков
        self.x_player = self.comboBox_X.currentIndex()
        self.o_player = self.comboBox_O.currentIndex()
        # настройка стартового поля игры
        for i in range(1, 10):
            command = f"self.pB{i}.setText('')\n" \
                      f"self.pB{i}.setEnabled(True)\n" \
                      f"self.pB{i}.setStyleSheet('background: white')\n"
            exec(command)

        # определяем режим игры
        if self.x_player != 0 and self.o_player != 0:
            # режим бот против бота
            self.bot_vs_bot = True
            self.fight_of_bots()
        else:
            # режим с игроком
            self.bot_vs_bot = False
            # определяем чей первый ход
            if self.x_player != 0:
                # бот ходит первым
                self.move_of_bot()

    def reset_click(self):
        self.X_score = 0
        self.O_score = 0
        self.lbl_score.setText(f"{self.X_score} : {self.O_score}")

    def button_click(self):
        # Ход Человека
        self.mark = self.definition_of_mark
        button = self.sender()
        name = button.objectName()
        index = int(list(name)[-1]) - 1
        self.update_board(index, self.mark)
        self.check_win()

        # Ход Бота
        if not self.bot_vs_bot:
            self.move_of_bot()
            self.check_win()

    @property
    def definition_of_mark(self):
        if self.board.count('X') > self.board.count('O'):
            mark = 'O'
        else:
            mark = 'X'
        return mark

    def get_winning_combos(self, board):
        return [
            {0: board[0], 1: board[1], 2: board[2]},
            {3: board[3], 4: board[4], 5: board[5]},
            {6: board[6], 7: board[7], 8: board[8]},
            {0: board[0], 3: board[3], 6: board[6]},
            {1: board[1], 4: board[4], 7: board[7]},
            {2: board[2], 5: board[5], 8: board[8]},
            {0: board[0], 4: board[4], 8: board[8]},
            {2: board[2], 4: board[4], 6: board[6]},
        ]

    def game_over(self, board):
        combo_wins = self.get_winning_combos(board)
        current_values = [(list(combo.values()), list(combo.keys())) for combo in combo_wins]
        for combo in current_values:
            if combo[0].count('X') == 3:
                return "X wins", combo[1]
            elif combo[0].count('O') == 3:
                return "O wins", combo[1]
        if board.count(' ') == 0:
            return "Draw", []

    def check_win(self):
        if not self.stop_game:
            result = self.game_over(self.board)
            if result:
                if result[0] == "X wins":
                    self.X_score += 1
                elif result[0] == "O wins":
                    self.O_score += 1
                elif result[0] == "Draw":
                    pass

                self.stop_game = True
                self.finished_board(result[1])

    def update_board(self, index, mark):
        self.board[index] = mark
        command = f"self.pB{index + 1}.setText(mark)\n" \
                  f"self.pB{index + 1}.setEnabled(False)\n"
        if mark == 'X':
            command += f"self.pB{index + 1}.setStyleSheet('color: blue; background: #eae4e5;')\n"
        else:
            command += f"self.pB{index + 1}.setStyleSheet('color: red; background: #eae4e5;')\n"

        exec(command)

    def finished_board(self, wins_index):
        self.lbl_score.setText(f"{self.X_score} : {self.O_score}")
        for i in range(0, 9):
            command = f"self.pB{i + 1}.setEnabled(False)\n"
            if wins_index:
                if i in wins_index:
                    command += f"self.pB{i + 1}.setStyleSheet('background: #2dff3f; color: black')\n"
                else:
                    command += f"self.pB{i + 1}.setStyleSheet('background: #ff233a; color: black')\n"
            else:
                command += f"self.pB{i + 1}.setStyleSheet('background: #eeff2f; color: black')\n"
            exec(command)

    def move_of_bot(self):
        if not self.stop_game and not self.bot_vs_bot:
            self.mark = self.definition_of_mark
            self.opponent_mark = 'X' if self.mark == "O" else 'O'
            if self.x_player == 1 or self.o_player == 1:
                self.easy_bot(self.mark)
            elif self.x_player == 2 or self.o_player == 2:
                self.medium_bot(self.mark, self.opponent_mark)
            elif self.x_player == 3 or self.o_player == 3:
                self.hard_bot(self.mark, self.opponent_mark)

    def easy_bot(self, mark):
        index = self.random_move()
        self.update_board(index, mark)

    def random_move(self):
        possible_index = [ind for ind, val in enumerate(self.board) if val == ' ']
        index = random.choice(possible_index)
        return index

    def medium_bot(self, mark, opponent_mark):
        index = self.priority(mark, opponent_mark)
        if not index:
            index = self.random_move()

        self.update_board(index, mark)

    def priority(self, my_mark, opponent_mark):
        combo_win = self.get_winning_combos(self.board)
        combo_values = [(list(c.values()), list(c.keys())) for c in combo_win]
        for combo in combo_values:
            # Сначала проверяем свою победную комбинацию
            if combo[0].count(my_mark) == 2 and combo[0].count(' ') == 1:
                ind = combo[0].index(' ')
                return combo[1][ind]
            # Если своей победной комбинации нет, то проверяем победные комбинации противника
            elif combo[0].count(opponent_mark) == 2 and combo[0].count(' ') == 1:
                ind = combo[0].index(' ')
                return combo[1][ind]

    def hard_bot(self, mark, opponent_mark):
        self.scores = {opponent_mark: -100,
                       mark: 100,
                       'draw': 0}

        index = self.minimax(mark, opponent_mark, self.board, 0, 'MAX')
        self.update_board(index, mark)

    def minimax(self, mark, opponent_mark, board, depth, TURN):
        result = self.game_over(board)
        if result:
            if mark == 'O':
                if result[0] == "X wins":
                    return self.scores[opponent_mark]
                if result[0] == "O wins":
                    return self.scores[mark]
            else:
                if result[0] == "X wins":
                    return self.scores[mark]
                if result[0] == "O wins":
                    return self.scores[opponent_mark]
            if result[0] == "Draw":
                return self.scores['draw']

        if depth == 0 or depth % 2 == 0:
            TURN = 'MAX'
            char = mark
        else:
            TURN = 'MIN'
            best_score = infinity
            char = opponent_mark

        all_scores = []
        for i in range(9):
            if board[i] == ' ':
                board[i] = char
                score = self.minimax(mark, opponent_mark, board, depth + 1, TURN)
                board[i] = ' '
                all_scores.append((i, score))

        best_score = max(all_scores, key=lambda k: k[1]) if TURN == 'MAX' else min(all_scores, key=lambda k: k[1])
        if depth == 0:
            return best_score[0]
        else:
            return best_score[1]

    def fight_of_bots(self):
        while not self.stop_game:
            self.mark = self.definition_of_mark
            self.opponent_mark = 'X' if self.mark == "O" else 'O'
            if self.mark == 'X':
                if self.x_player == 1:
                    self.easy_bot(self.mark)
                elif self.x_player == 2:
                    self.medium_bot(self.mark, self.opponent_mark)
                elif self.x_player == 3:
                    self.hard_bot(self.mark, self.opponent_mark)
                    
            elif self.mark == 'O':
                if self.o_player == 1:
                    self.easy_bot(self.mark)
                elif self.o_player == 2:
                    self.medium_bot(self.mark, self.opponent_mark)
                elif self.o_player == 3:
                    self.hard_bot(self.mark, self.opponent_mark)

            self.check_win()


def main():
    app = QtWidgets.QApplication([])
    window = GameApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
