from PIL import Image



class Board():

    def __init__(self, fen):
        self.fen = fen
        self.path = "../Boards/"
        self.board_iter = 0


    def calc_pos(self, pos):
        # returns the pixel position for a piece
        return (pos[0]*146, pos[1]*146)

    def transform_fen(self, fen):
        new_fen = ""
        for char in fen:
            if char.isdigit():
                new_fen += "X" * int(char)
            else:
                new_fen += char
        return new_fen



    def load(self):
        # Load all images
        
        board = Image.open("../Textures/board.png").convert("RGBA")
        yellow = Image.open("../Textures/Yellow.png")
        
        # White
        P = Image.open("../Textures/LightPawn.webp").convert("RGBA").resize((146, 146))
        R = Image.open("../Textures/LightRook.webp").convert("RGBA").resize((146, 146))
        N = Image.open("../Textures/LightKnight.webp").convert("RGBA").resize((146, 146))
        B = Image.open("../Textures/LightBishop.webp").convert("RGBA").resize((146, 146))
        Q = Image.open("../Textures/LightQueen.webp").convert("RGBA").resize((146, 146))
        K = Image.open("../Textures/LightKing.webp").convert("RGBA").resize((146, 146))

        # Black
        p = Image.open("../Textures/DarkPawn.webp").convert("RGBA").resize((146, 146))
        r = Image.open("../Textures/DarkRook.webp").convert("RGBA").resize((146, 146))
        n = Image.open("../Textures/DarkKnight.webp").convert("RGBA").resize((146, 146))
        b = Image.open("../Textures/DarkBishop.webp").convert("RGBA").resize((146, 146))
        q = Image.open("../Textures/DarkQueen.webp").convert("RGBA").resize((146, 146))
        k = Image.open("../Textures/DarkKing.webp").convert("RGBA").resize((146, 146))

        global pieces
        pieces = {"board": board, "Y": yellow, "P": P, "R": R, "N": N, "B": B, "Q": Q, "K": K, "p": p, "r": r, "n": n, "b": b, "q": q, "k": k}

        

        return pieces

    def create_board(self, move = None, show = True):
        fen = self.fen
        pieces = self.load()
        fen = self.transform_fen(fen.split(" ")[0])

        board = pieces["board"]

        if move is not None:
            board.alpha_composite(pieces["Y"], self.calc_pos((move[0], move[1])))
            board.alpha_composite(pieces["Y"], self.calc_pos((move[2], move[3])))

        fen_list = fen.split("/")
        for i_row, v_row in enumerate(fen_list):
            for i_col, v_col in enumerate(v_row):
                if v_col == "X":
                    continue
                board.paste(pieces[v_col], self.calc_pos((i_col, i_row)), pieces[v_col])
        
        


        if show:
            board.show()
        return board

    def update_fen(self, rawmove, show=True):
        fen = self.fen
        # Check for castle
        if rawmove == "O-O":
            # White short castle
            self.update_fen("h1f1", show)
            self.update_fen("e1g1", show)
            return

        elif rawmove == "O-O-O":
            # White long castle
            self.update_fen("a1d1", show)
            self.update_fen("e1c1", show)
            return

        elif rawmove == "o-o":
            # Black short castle
            self.update_fen("h8f8", show)
            self.update_fen("e8g8", show)
            return
            
        elif rawmove == "o-o-o":
            # Black long castle
            self.update_fen("a8d8", show)
            self.update_fen("e8c8", show)
            return

        # We want to convert a move to only integers: e2e4 --> 4 1 4 3 corresponding to the row/col index

        fen = self.transform_fen(fen.split(" ")[0]).split("/") # This gets us a list with each row

        # But we need to have a list with each square, so we can change the list, to later combine it to the FEN listed by rows

        square_fen = [list(row) for row in fen] 

        # Now we have a list of lists for each row

        board_nums = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0} # This contains the index for each row/column
    

        move = [board_nums[char] for char in rawmove]

        piece = square_fen[move[1]][move[0]] # Get the piece

        # Check if piece is a piece
        if piece == "X":
            print(move)
            print("move is faulty")
            raise TypeError

        square_fen[move[1]][move[0]] = "X" # Set the original square to nothing

        square_fen[move[3]][move[2]] = piece # Set the new square to the piece
        self.fen = "/".join(["".join(row) for row in square_fen])
        self.board = self.create_board(move, show)
        return

    def show_move(self, move, show=True):
        # Create the new FEN and board
        self.update_fen(move)
        self.board.save(f"{self.path}Board{self.board_iter}.png")

    def play(self, show=True):
        # Interactive chess player
        self.board = self.create_board(None, show)
        self.board.save(f"{self.path}Board.png")
        input_move = input("Move: ")
        while input_move != "0":
            self.show_move(input_move, show)
            input_move = input("Move: ")
            self.board_iter += 1
