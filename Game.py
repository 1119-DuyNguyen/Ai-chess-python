import chess as ch
import simple_chalk as chalk
#thư viện chess



class Ai:
    INFINITY=9999
    # color : black/ white
    def __init__(self, board: ch.Board, maxDepth, color):
        self.board=board
        self.color=color
        self.maxDepth=maxDepth
    
    def getBestMove(self):
        move=self.engine(1,-self.INFINITY,self.INFINITY)
        #print(move)
        return move

    def evalFunct(self)->float:
        compt = 0
        for i in range(64):
            compt+=self.squareResPoints(ch.SQUARES[i])

        compt += self.endgameOpportunity() 
        # print(compt)
        return compt

    def endgameOpportunity(self):
        if (self.board.is_checkmate()):
            #minimize player
            if (self.board.turn == self.color):
                return -self.INFINITY
            #maximizeplayer
            else:
                return self.INFINITY

        return 0

    #tính theo hệ số điểm của Hans Berliner'system
        #https://en.wikipedia.org/wiki/Chess_piece_relative_value#Hans_Berliner.27s_system
    def squareResPoints(self, square):
        pieceValue = 0
        typePiece=self.board.piece_type_at(square)
        if(typePiece==None): return pieceValue

        if(typePiece == ch.PAWN):
            pieceValue = 1
        elif (typePiece == ch.ROOK):
            pieceValue = 5.1
        elif (typePiece == ch.BISHOP):
            pieceValue = 3.33
        elif (typePiece == ch.KNIGHT):
            pieceValue = 3.2
        elif (typePiece == ch.QUEEN):
            pieceValue = 8.8

        if (self.board.color_at(square)!=self.color):
            return -pieceValue
        else:
            return pieceValue
 
    def engine(self,depth,alpha,beta):
        
        if ( depth == self.maxDepth or self.board.is_game_over()):
            return self.evalFunct()
        
        else:
            moveList = list(self.board.legal_moves)
            firstMove=None
            newValueComputation = None

            if(depth % 2 != 0):
                newValueComputation = -self.INFINITY
                for move in moveList:
                    
                    #Play move i
                    self.board.push(move)
    
                    value = self.engine(depth + 1,alpha,beta) 

                    if(value > newValueComputation ):
                        if (depth == 1):
                            firstMove=move
                        newValueComputation = value
                        alpha= max(newValueComputation,alpha)
                    self.board.pop()   
                    if(alpha>=beta):
                        break    
            else:
                newValueComputation = self.INFINITY
                for move in moveList:
                
                    self.board.push(move)

                    value = self.engine(depth + 1,alpha,beta) 
                    if(value < newValueComputation):
                        newValueComputation = value
                        beta= min(newValueComputation,beta)

                    self.board.pop()
                    if(alpha>=beta):
                        break                    
            if (depth>1):
                return newValueComputation
            else:
                return firstMove
            
class Game:


    def __init__(self, board:ch.Board,WHITE,BLACK):
        self.board=board       
        self.WHITE=WHITE
        self.BLACK=BLACK    
        self.board.is_game_over= self.is_game_over
        print("")
        titleColor = chalk.bgRed.white.bold
        print(titleColor("Chess AI | CLI"))
        print("")
    def chooseMode(self):
        print(chalk.bgBlue.white("""Nếu muốn thoát game hãy ấn q """))
        while(True):
            choice=input("Hãy chọn chế độ ?\n1.Người và máy \n2.Máy và máy \n3.Người và người \n ")
            if(choice=='1'):
                return self.PVAMode()
            elif(choice=='2'):
                return self.AVAMode()
            elif(choice=='3'):
                return self.PVPMode()
            elif(choice=='q'):
                return 0
            else: print(chalk.bgRed.bold.white("Lựa chọn không hợp lệ "))

    def startGame(self):
        return self.chooseMode()
    
    def printBoard(self):
        string = self.board.__str__()
        string = string.replace('\n',' ')
        #quân đen
        string = string.replace('p',u'\u265F')
        string = string.replace('r',u'\u265C')
        string = string.replace('n',u'\u265E')
        string = string.replace('b', u'\u265D')
        string = string.replace('q',u'\u265B')
        string = string.replace('k',u'\u265A')
        # quân trắng 
        string = string.replace('P',u'\u2659')
        string = string.replace('R', u'\u2656')
        string = string.replace('N', u'\u2658')
        string = string.replace('B',  u'\u2657')
        string = string.replace('Q',u'\u2655')
        string = string.replace('K', u'\u2654')
        string = string.replace('\n',' ')

        string= string.split(' ')
        
        #bàn cờ 15x8 do khoảng trắng
        print(chalk.bgWhite.black.bold("   A  B  C  D  E  F  G  H "))
        for y in range(8):
            #vì bàn cờ in ngược
            print(chalk.bgWhite.black.bold(str(8-y)+'|'),end=' ')
            for x in range(8):
                print(string[y * 8 + x],end='  ')
            print()   
            
    def getValidDepth(self):
        while(True):
            try:
                maxDepth = int(input("""Chọn độ sâu(độ sâu càng lớn AI càng nghĩ lâu): """))
                if(maxDepth>=1):
                    return maxDepth
                else: raise ValueError("lựa chọn không hợp lệ")
            except:
                print(chalk.bgRed.bold.white("Lựa chọn phải là 1 số nguyên dương >= 1 "))


    def playHumanMove(self):
        while(True):
            try:
                print(chalk.bgGreen.bold.white('Ví dụ nước đi hợp lệ: a2 a3'))

                play = input(chalk.bgBlue.white.underline("Nước đi >>> ")).lower().replace(' ','')
                if(play=='q'): return 0
                self.board.push_san(play)
                return 1
            except:
                print(chalk.bgRed.bold.white(" Nước đi không hợp lệ "))
            
    def playEngineMove(self, maxDepth, color):
        engine = Ai(self.board, maxDepth, color)

        if(not self.board.is_game_over()):
            move=engine.getBestMove()
            if(move!=None): self.board.push(move)

    def PVAMode(self):
        color=None
        while(True):
            print(chalk.bgBlue.white("""Chọn quân cờ (gõ "b"(quân đen) hoặc "w"(quân trắng))"""))
            color = input(">>> ")
            if(color=="b" or color=="w"): break
            elif(color=='q'): print('Hi vọng bạn đã có những ván chơi thật tuyệt'); return 0
            else :  print(chalk.bgRed.bold.white("Lựa chọn không hợp lệ "))

        #tìm độ khóa
        maxDepth=self.getValidDepth()

        if color=="b":
            while (True):
                print(chalk.bgBlue.white("AI đang suy nghĩ..."))
                if(self.board.is_game_over()): break
                self.playEngineMove(maxDepth, self.WHITE)
                self.printBoard()
                if(self.board.is_game_over()): break
                if(not self.playHumanMove()):print('Hi vọng bạn đã có những ván chơi thật tuyệt'); return 0
                self.printBoard()

            self.printOutcome()    
        elif color=="w":
            while (True):
                if(self.board.is_game_over()): break
                self.printBoard()
                if(not self.playHumanMove()):print('Hi vọng bạn đã có những ván chơi thật tuyệt'); return 0
                if(self.board.is_game_over()): break
                print(chalk.bgBlue.white("AI đang suy nghĩ..."))
                self.playEngineMove(maxDepth, self.BLACK)
                self.printBoard()

            self.printOutcome()
        #reset the board
        self.board.reset()
        #start another game
        return 1
    def AVAMode(self):
                
        maxDepth=self.getValidDepth()

        while (True):
                #tìm kiếm hàm trong module board
                if(self.board.is_game_over()): break
                print(chalk.bgBlue.white("AI 1 đang suy nghĩ..."))
                self.playEngineMove(maxDepth, self.WHITE)
                self.printBoard()
                if(self.board.is_game_over()): break
                print(chalk.bgBlue.white("AI 2 đang suy nghĩ..."))

                self.playEngineMove(maxDepth, self.BLACK)
                self.printBoard()

        self.printBoard()
        self.printOutcome()    
        #reset the board
        self.board.reset()
        #start another game
        return 1  
    
    def PVPMode(self):
        color=None
        while(True):
            print(chalk.bgBlue.white("""người chơi 1 chọn quân cờ (gõ "b"(quân đen) hoặc "w"(quân trắng))"""))
            color = input(">>> ")
            if(color=="b" or color=="w"): break
            elif(color=='q'): print('Hi vọng bạn đã có những ván chơi thật tuyệt'); return 0
            else :  print(chalk.bgRed.bold.white("Lựa chọn không hợp lệ "))
        
        self.printBoard()       
        
        while(True):              
            if(self.board.is_game_over()): break        
            print(chalk.bgWhite.white("""Xin mời quân trắng đi"""))
            if(not self.playHumanMove()):print('Hi vọng bạn đã có những ván chơi thật tuyệt'); return 0
            
            self.printBoard()
            if(self.board.is_game_over()): break
            print(chalk.bgBlue.white("""Xin mời quân đen đi"""))
            if(not self.playHumanMove()):print('Hi vọng bạn đã có những ván chơi thật tuyệt'); return 0

            self.printBoard()

        self.printOutcome()
    def is_game_over(self):
        if(self.board.is_checkmate()):
            return True 
        elif(self.board.is_stalemate()):
            return True 
        elif(self.board.is_repetition()):
            return True
        elif(self.board.is_fifty_moves()):
            return True
        elif(self.board.is_insufficient_material()):
            return True
        return False
    def printOutcome(self):
        if(self.board.is_checkmate()):
            print('Trận đấu kết thúc do chiếu hết') 
        elif(self.board.is_stalemate()):
            print('Trận đấu hòa do hết nước đi') 
        elif(self.board.is_repetition()):
            print('Trận đấu hòa do lặp lại nước đi 3 lần')
        elif(self.board.is_fifty_moves()):
            print('Trận đấu hòa do 50 nước đi không có quân bị bắt')
        elif(self.board.is_insufficient_material()):
            print("Trận dấu hòa do cả hai bên không có đủ lực lượng để chiến thắng")
        



