# Author: Erik Grinn
# GitHub username: erikgrinn
# Date: 5/31/24
# Description: Portfolio project - Atomic Chess


class ChessPiece:
    """ class of chess piece defining type, position, and color """
    def __init__(self, type, position, color, art):
        self._type = type
        self._position = position
        self._color = color
        self._art = art

    def get_type(self):
        """ returns piece type """
        return self._type

    def get_position(self):
        """ returns piece position """
        return self._position

    def get_color(self):
        """ returns piece color """
        return self._color

    def get_art(self):
        """ returns art of chess piece for printing"""
        return self._art

    def set_position(self, position):
        """ sets piece to new position """
        self._position = position


class ChessVar:
    """ class keeping track of board and game """
    def __init__(self):
        """ initializes beginning state of game """
        self._game_state = 'UNFINISHED'
        self._current_turn = 'white'
        self._board = self.start_board()

    def start_board(self):
        """ initializes beginning state of board """
        board = {}
        columns = 'abcdefgh'
        rows = '12345678'
        pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        colors = ['white', 'black']
        for col in columns:
            # pawns
            board[col + rows[1]] = ChessPiece(pieces[0], col + rows[1], colors[0], '♙')
            board[col + rows[6]] = ChessPiece(pieces[0], col + rows[6], colors[1], '♟')

        # rooks
        board[columns[0] + rows[0]] = ChessPiece(pieces[3], columns[0] + rows[0], colors[0], '♖')
        board[columns[7] + rows[0]] = ChessPiece(pieces[3], columns[7] + rows[0], colors[0], '♖')
        board[columns[0] + rows[7]] = ChessPiece(pieces[3], columns[0] + rows[7], colors[1], '♜')
        board[columns[7] + rows[7]] = ChessPiece(pieces[3], columns[7] + rows[7], colors[1], '♜')

        # knights
        board[columns[1] + rows[0]] = ChessPiece(pieces[1], columns[1] + rows[0], colors[0], '♘')
        board[columns[6] + rows[0]] = ChessPiece(pieces[1], columns[6] + rows[0], colors[0], '♘')
        board[columns[1] + rows[7]] = ChessPiece(pieces[1], columns[1] + rows[7], colors[1], '♞')
        board[columns[6] + rows[7]] = ChessPiece(pieces[1], columns[6] + rows[7], colors[1], '♞')

        # bishops
        board[columns[2] + rows[0]] = ChessPiece(pieces[2], columns[2] + rows[0], colors[0], '♗')
        board[columns[5] + rows[0]] = ChessPiece(pieces[2], columns[5] + rows[0], colors[0], '♗')
        board[columns[2] + rows[7]] = ChessPiece(pieces[2], columns[2] + rows[7], colors[1], '♝')
        board[columns[5] + rows[7]] = ChessPiece(pieces[2], columns[5] + rows[7], colors[1], '♝')

        # queens
        board[columns[3] + rows[0]] = ChessPiece(pieces[4], columns[3] + rows[0], colors[0], '♕')
        board[columns[3] + rows[7]] = ChessPiece(pieces[4], columns[3] + rows[7], colors[1], '♛')

        # kings
        board[columns[4] + rows[0]] = ChessPiece(pieces[5], columns[4] + rows[0], colors[0], '♔')
        board[columns[4] + rows[7]] = ChessPiece(pieces[5], columns[4] + rows[7], colors[1], '♚')

        return board

    def get_game_state(self):
        """ returns game_state """
        return self._game_state

    def set_white_won(self):
        """ sets game_state to WHITE_WON """
        self._game_state = 'WHITE_WON'

    def set_black_won(self):
        """ sets game_state to BLACK_WON """
        self._game_state = 'BLACK_WON'

    def make_move(self, start, finish):
        """ moves position of piece on start position to finish position.
         if start position does not belong to player, or if move not allowed, returns False """
        if self._game_state != 'UNFINISHED':
            return False

        if start in self._board:
            piece = self._board[start]
        else:
            return False

        if piece.get_color() != self._current_turn:
            return False

        if self.valid_move(piece, start, finish):
            if self._game_state == 'UNFINISHED':
                if piece.get_color() == 'white':
                    self._current_turn = 'black'
                elif piece.get_color() == 'black':
                    self._current_turn = 'white'

            if finish in self._board:
                if self._board[finish].get_color() == piece.get_color():
                    return False

                if piece.get_type() == 'king':
                    return False

                area = self.explosion_area(finish)

                king_count = 0
                for pos in area:
                    if pos in self._board:
                        if self._board[pos].get_type() == 'king':
                            king_count += 1
                            if king_count == 2:
                                return False

                for pos in area:
                    if pos in self._board:
                        if self._board[pos].get_type() == 'king':
                            if self._board[pos].get_color() == 'white':
                                self.set_black_won()
                            elif self._board[pos].get_color() == 'black':
                                self.set_white_won()
                            del self._board[pos]
                        elif self._board[pos].get_type() != 'pawn':
                            del self._board[pos]
                        elif self._board[pos].get_type() == 'pawn' and pos == finish:
                            del self._board[pos]

                self._board[finish] = piece
                piece.set_position(finish)
                del self._board[start]
                del self._board[finish]
                return True

            else:
                self._board[finish] = piece
                piece.set_position(finish)
                del self._board[start]
                return True
        return False

    def explosion_area(self, center):
        """ iterates over explosion area, deleting all but pawns. Changes game state if
        king involved """
        columns = 'abcdefgh'
        center_letter_idx = columns.find(center[0])
        area = []

        if 0 <= center_letter_idx < 7:
            right_col = center_letter_idx + 1
        else:
            right_col = None

        if center_letter_idx > 0:
            left_col = center_letter_idx - 1
        else:
            left_col = None

        if 1 <= int(center[1]) < 8:
            upper_row = int(center[1]) + 1
        else:
            upper_row = None

        if int(center[1]) > 1:
            lower_row = int(center[1]) - 1
        else:
            lower_row = None

        for row in [lower_row, int(center[1]), upper_row]:
            for col in [left_col, center_letter_idx, right_col]:
                area.append(columns[col] + str(row))

        return area

    def valid_move(self, piece, start, finish):
        """ checks if move is valid for piece according to piece-specific move-sets """
        columns = 'abcdefgh'
        start_letter_idx = columns.find(start[0])
        finish_letter_idx = columns.find(finish[0])
        type = piece.get_type()

        if type == 'pawn':
            if piece.get_color() == 'white' and start[0] == finish[0] and finish not in self._board:
                if int(start[1]) == 2:
                    if int(finish[1]) - int(start[1]) == (1 and 2):
                        return True
                if int(finish[1]) - int(start[1]) == 1:
                    return True
            elif piece.get_color() == 'black' and start[0] == finish[0] and finish not in self._board:
                if int(start[1]) == 7:
                    if abs(int(finish[1]) - int(start[1])) == (1 and 2):
                        return True
                if int(start[1]) - int(finish[1]) == 1:
                    return True
            elif (abs(start_letter_idx - finish_letter_idx) == 1) and (abs(int(start[1]) - int(finish[1])) == 1) \
                    and finish in self._board:
                return True
            return False

        if type == 'rook':
            if piece.get_color() == 'white':
                if start[0] == finish[0] and (1 <= int(finish[1]) - int(start[1]) <= 7):
                    return True
                elif start[1] == finish[1] and (finish[0] in columns):
                    return True
            elif piece.get_color() == 'black':
                if start[0] == finish[0] and (1 <= int(start[1]) - int(finish[1]) <= 7):
                    return True
                elif start[1] == finish[1] and (finish[0] in columns):
                    return True
            return False

        if type == 'knight':
            if abs(finish_letter_idx - start_letter_idx) == 2:
                if abs(int(start[1]) - int(finish[1])) == 1:
                    return True
            if abs(int(start[1]) - int(finish[1])) == 2:
                if abs(finish_letter_idx - start_letter_idx) == 1:
                    return True
            return False

        if type == 'bishop':
            if abs(int(start[1]) - int(finish[1])) == 0:
                return False
            elif abs(finish_letter_idx - start_letter_idx)/abs(int(start[1]) - int(finish[1])) == 1:
                return True
            return False

        if type == 'queen':
            if piece.get_color() == 'white':
                if start_letter_idx == finish_letter_idx and (1 <= int(finish[1]) <= 8):
                    return True
                elif int(start[1]) == int(finish[1]) and (finish[0] in columns):
                    return True
                elif abs(finish_letter_idx - start_letter_idx) / abs(int(start[1]) - int(finish[1])) == 1:
                    return True
            elif piece.get_color() == 'black':
                if start_letter_idx == finish_letter_idx and (1 <= int(finish[1]) <= 8):
                    return True
                elif int(start[1]) == int(finish[1]) and (finish[0] in columns):
                    return True
                elif abs(finish_letter_idx - start_letter_idx) / abs(int(start[1]) - int(finish[1])) == 1:
                    return True
            return False

        if type == 'king':
            if abs(int(start[1]) - int(finish[1])) == 1 and abs(finish_letter_idx - start_letter_idx) == 0:
                return True
            elif abs(finish_letter_idx - start_letter_idx) == 1 and abs(int(start[1]) - int(finish[1])) == 0:
                return True
            elif abs(finish_letter_idx - start_letter_idx) == 1 and \
                    abs(int(start[1]) - int(finish[1])) == 1:
                return True
            return False

    def print_board(self):
        """ prints the current state of the board to output terminal """
        board_print = '\n'
        for row in '87654321':
            for col in 'abcdefgh':
                position = col + row
                if position in self._board:
                    piece = self._board[position]
                    board_print += piece.get_art()
                else:
                    board_print += '.'
                board_print += '  '
            board_print += '\n'
        print(board_print)
        if self._game_state == 'UNFINISHED':
            print('Current turn:', self._current_turn, '\n')
