import connect4

def start_game():
    turn = 0
    b1 = connect4.Connect4Board()

    print(b1.display())
    print("To play, enter an open column number or type exit to quit.")
    while(turn<42):
        if turn%2==0:
            piece='x'
            player='1'
        else:
            piece='o'
            player='2'

        while True:
            move = input("Player " + player + " move: ")
            if move == 'exit':
                return
            try:
                move = int(move)
                if b1.check_move(move)=='True':
                    b1.drop_piece(move, piece)
                    break
                else: 
                    print("Cannot insert piece there! Try again. ")
            except ValueError:
                print("Enter valid column number!")
 
        print(b1.display())
        if(b1.find_winner(piece))=='True':
            print("Player " + player + " wins!")
            return


        turn+=1



start_game()