import time

DAMA = 40
INF = 10000000
EXECTIME = 13  # execution time of minimnax algoritahm

moves = []
value_dame =  [0, 50, 70, 100, 120, 140, 160, 180, 200, 215, 230, 240, 250]
value_chipa = [0, 30, 60, 90, 120, 140, 160, 180, 200, 215, 230, 240, 250]
dikt = {}


def in_bounds(r, c):
    return 7 >= r >= 0 and 7 >= c >= 0


def to_string(player):
    if player == 1:
        return "1"
    if player == 2:
        return "2"


def opposite_player(p):
    if p == 1:
        return 2
    else:
        return 1


def state_of_board(board):  # True ako je neko pobedio (ostao bez figurica)
    jed = dva = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1 or board[i][j] == 3:
                jed += 1
            elif board[i][j] == 2 or board[i][j] == 4:
                dva += 1

    return dva == 0 or jed == 0


def onion_rings(r):
    if r == 0 or r == 7:
        return 30
    return 0


def print_board(board):
    print("Board:")
    for red in board:
        print(red)


def value_of_board(board):  # Ako je sto vece 2 pobedjuje, sto manje 1
    if state_of_board(board):  # ako je neko pobedio, to je najveca(najmanja) vrednost
        for i in range(8):
            for j in range(8):
                if board[i][j] == 1 or board[i][j] == 3:
                    return INF
                if board[i][j] == 2 or board[i][j] == 4:
                    return -INF

    if no_more_moves(board, 1):
        return INF
    if no_more_moves(board, 2):
        return -INF

    jed = dva = 0
    jed_d = dva_d = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                jed += 1
            elif board[i][j] == 2:
                dva += 1
            if board[i][j] == 3:
                jed_d += 1
            if board[i][j] == 4:
                dva_d += 1

    score = 0
    score += value_chipa[dva]
    score += value_dame[dva_d]
    score -= value_chipa[jed]
    score -= value_dame[jed_d]

    for r in range(8):
        for c in range(8):
            if board[r][c] == 1 or board[r][c] == 3:
                score -= onion_rings(r)
            if board[r][c] == 2 or board[r][c] == 4:
                score += onion_rings(r)
            if board[r][c] == 3:
                score -= DAMA
            if board[r][c] == 4:
                score += DAMA
    return (-1) * score


def no_more_moves(board, player):
    if player == 2:
        for r in range(8):
            for c in range(8):
                if board[r][c] == 2 or board[r][c] == 4:
                    mooves = []
                    find_moves(board, r, c, 2, [], True, mooves)
                    if len(mooves) != 0:
                        return False
    if player == 1:

        for r in range(8):
            for c in range(8):
                if board[r][c] == 1 or board[r][c] == 3:
                    mooves = []
                    find_moves(board, r, c, 1, [], True, mooves)
                    if len(mooves) != 0:
                        return False
    return True


def find_moves(board, r, c, igrac, dosad, prvi_potez, moves):
    if igrac == 1:
        if prvi_potez:
            if in_bounds(r + 1, c + 1) and board[r + 1][c + 1] == 0:
                moves.append([(r + 1, c + 1)])

            if in_bounds(r + 1, c - 1) and board[r + 1][c - 1] == 0:
                moves.append([(r + 1, c - 1)])

        if in_bounds(r + 2, c + 2) and (board[r + 1][c + 1] == 2 or board[r + 1][c + 1] == 4) and board[r + 2][
            c + 2] == 0:
            novi_dosad = dosad.copy()
            novi_dosad.append((r + 2, c + 2))
            moves.append(novi_dosad)

            pojeden = board[r + 1][c + 1]
            board[r + 1][c + 1] = 0
            board[r][c], board[r + 2][c + 2] = board[r + 2][c + 2], board[r][c]

            find_moves(board, r + 2, c + 2, igrac, novi_dosad, False, moves)

            board[r + 1][c + 1] = pojeden
            board[r][c], board[r + 2][c + 2] = board[r + 2][c + 2], board[r][c]

        if in_bounds(r + 2, c - 2) and (board[r + 1][c - 1] == 2 or board[r + 1][c - 1] == 4) and board[r + 2][
            c - 2] == 0:
            novi_dosad = dosad.copy()
            novi_dosad.append((r + 2, c - 2))
            moves.append(novi_dosad)

            pojeden = board[r + 1][c - 1]
            board[r + 1][c - 1] = 0
            board[r][c], board[r + 2][c - 2] = board[r + 2][c - 2], board[r][c]

            find_moves(board, r + 2, c - 2, igrac, novi_dosad, False, moves)

            board[r + 1][c - 1] = pojeden
            board[r][c], board[r + 2][c - 2] = board[r + 2][c - 2], board[r][c]
    if igrac == 2:
        if prvi_potez:
            if in_bounds(r - 1, c - 1) and board[r - 1][c - 1] == 0:
                moves.append([(r - 1, c - 1)])

            if in_bounds(r - 1, c + 1) and board[r - 1][c + 1] == 0:
                moves.append([(r - 1, c + 1)])

        if in_bounds(r - 2, c - 2) and (board[r - 1][c - 1] == 1 or board[r - 1][c - 1] == 3) and board[r - 2][
            c - 2] == 0:
            novi_dosad = dosad.copy()
            novi_dosad.append((r - 2, c - 2))
            moves.append(novi_dosad)

            pojeden = board[r - 1][c - 1]
            board[r - 1][c - 1] = 0
            board[r - 2][c - 2], board[r][c] = board[r][c], board[r - 2][c - 2]

            find_moves(board, r - 2, c - 2, igrac, novi_dosad, False, moves)

            board[r - 1][c - 1] = pojeden
            board[r - 2][c - 2], board[r][c] = board[r][c], board[r - 2][c - 2]

        if in_bounds(r - 2, c + 2) and (board[r - 1][c + 1] == 1 or board[r - 1][c + 1] == 3) and board[r - 2][
            c + 2] == 0:
            novi_dosad = dosad.copy()
            novi_dosad.append((r - 2, c + 2))
            moves.append(novi_dosad)

            pojeden = board[r - 1][c + 1]
            board[r - 1][c + 1] = 0
            board[r - 2][c + 2], board[r][c] = board[r][c], board[r - 2][c + 2]

            find_moves(board, r - 2, c + 2, igrac, novi_dosad, False, moves)

            board[r - 1][c + 1] = pojeden
            board[r - 2][c + 2], board[r][c] = board[r][c], board[r - 2][c + 2]

    if board[r][c] == 3:
        if prvi_potez:
            if in_bounds(r - 1, c - 1) and board[r - 1][c - 1] == 0:
                moves.append([(r - 1, c - 1)])

            if in_bounds(r - 1, c + 1) and board[r - 1][c + 1] == 0:
                moves.append([(r - 1, c + 1)])

        if in_bounds(r - 2, c - 2) and (board[r - 1][c - 1] == 2 or board[r - 1][c - 1] == 4) and board[r - 2][
            c - 2] == 0:
            novi_dosad = dosad.copy()
            novi_dosad.append((r - 2, c - 2))
            moves.append(novi_dosad)

            pojeden = board[r - 1][c - 1]
            board[r - 1][c - 1] = 0
            board[r - 2][c - 2], board[r][c] = board[r][c], board[r - 2][c - 2]

            find_moves(board, r - 2, c - 2, igrac, novi_dosad, False, moves)

            board[r - 1][c - 1] = pojeden
            board[r - 2][c - 2], board[r][c] = board[r][c], board[r - 2][c - 2]

        if in_bounds(r - 2, c + 2) and (board[r - 1][c + 1] == 2 or board[r - 1][c + 1] == 4) and board[r - 2][
            c + 2] == 0:
            novi_dosad = dosad.copy()
            novi_dosad.append((r - 2, c + 2))
            moves.append(novi_dosad)

            pojeden = board[r - 1][c + 1]
            board[r - 1][c + 1] = 0
            board[r][c], board[r - 2][c + 2] = board[r - 2][c + 2], board[r][c]

            find_moves(board, r - 2, c + 2, igrac, novi_dosad, False, moves)

            board[r - 1][c + 1] = pojeden
            board[r][c], board[r - 2][c + 2] = board[r - 2][c + 2], board[r][c]
    if board[r][c] == 4:
        if prvi_potez:
            if in_bounds(r + 1, c + 1) and board[r + 1][c + 1] == 0:
                moves.append([(r + 1, c + 1)])

            if in_bounds(r + 1, c - 1) and board[r + 1][c - 1] == 0:
                moves.append([(r + 1, c - 1)])

        if in_bounds(r + 2, c + 2) and (board[r + 1][c + 1] == 1 or board[r + 1][c + 1] == 3) and board[r + 2][
            c + 2] == 0:
            novi_dosad = dosad.copy()
            novi_dosad.append((r + 2, c + 2))
            moves.append(novi_dosad)

            pojeden = board[r + 1][c + 1]
            board[r + 1][c + 1] = 0
            board[r][c], board[r + 2][c + 2] = board[r + 2][c + 2], board[r][c]

            find_moves(board, r + 2, c + 2, igrac, novi_dosad, False, moves)

            board[r + 1][c + 1] = pojeden
            board[r][c], board[r + 2][c + 2] = board[r + 2][c + 2], board[r][c]

        if in_bounds(r + 2, c - 2) and (board[r + 1][c - 1] == 1 or board[r + 1][c - 1] == 3) and board[r + 2][
            c - 2] == 0:
            novi_dosad = dosad.copy()
            novi_dosad.append((r + 2, c - 2))
            moves.append(novi_dosad)

            pojeden = board[r + 1][c - 1]
            board[r + 1][c - 1] = 0
            board[r][c], board[r + 2][c - 2] = board[r + 2][c - 2], board[r][c]

            find_moves(board, r + 2, c - 2, igrac, novi_dosad, False, moves)

            board[r + 1][c - 1] = pojeden
            board[r][c], board[r + 2][c - 2] = board[r + 2][c - 2], board[r][c]


def play_move(potez, board, pojed):
    if len(potez) == 0:
        print("len(potez) == 0 u play_move")
        print_board(board)
        exit(5)

    r = potez[0][0]
    c = potez[0][1]

    pojed.append((r, c, board[r][c]))

    for tup in range(1, len(potez)):
        r2 = potez[tup][0]
        c2 = potez[tup][1]

        if (abs(r2 - r) + abs(c2 - c)) == 4:
            pojed.append((r + (r2 - r) // 2, c + (c2 - c) // 2, board[r + (r2 - r) // 2][c + (c2 - c) // 2]))
            board[r + (r2 - r) // 2][c + (c2 - c) // 2] = 0  # uklanjam pojedenog

        pojed.append((r2, c2, board[r2][c2]))
        board[r2][c2] = board[r][c]

        board[r][c] = 0
        r = r2
        c = c2
    if (r == 0 or r == 7) and board[r][c] <= 2:
        board[r][c] += 2


def restore_board(board, pojed):
    for tup in pojed:
        board[tup[0]][tup[1]] = tup[2]


def hashuj(board, player):
    ret = 0
    mod = 1000000007
    pret = 1
    d = 5
    for r in range(8):
        for c in range(8):
            ret = (ret + (board[r][c] * pret) % mod) % mod
            pret = (pret * d) % mod

    if player == 1:
        return ret
    else:
        return -ret


def minimax(board, depth, max_depth, maximizing_player, player, alpha, beta, opcija,
            tren_time):  # depth je dubina, mp True/False, player = 1 ili 2
    if time.time() - tren_time > EXECTIME:
        return value_of_board(board)

    if depth == 0 or state_of_board(board):
        return value_of_board(board)

    hash_value = hashuj(board, player)

    global moves
    potezi = []

    if hash_value in dikt:          # imam vec izracunate moguce poteze
        potezi = dikt[hash_value]
    else:
        for r in range(8):
            for c in range(8):
                if player == 1 and (board[r][c] == 1 or board[r][c] == 3):
                    moves = []
                    find_moves(board, r, c, player, [], True, moves)
                    for move in moves:
                        potezi.append([(r, c)] + move)
                if player == 2 and (board[r][c] == 2 or board[r][c] == 4):
                    moves = []
                    find_moves(board, r, c, player, [], True, moves)
                    for move in moves:
                        potezi.append([(r, c)] + move)
        dikt[hash_value] = potezi

    if time.time() - tren_time > EXECTIME:
        return value_of_board(board)

    ima_jedenja = False
    for potez in potezi:
        if abs(potez[0][0] - potez[1][0]) + abs(potez[0][1] - potez[1][1]) == 4:
            ima_jedenja = True
            break

    if maximizing_player:
        value = -INF-10
    else:
        value = INF+10

    best_potez = []

    for potez in potezi:
        if len(potez) == 0:
            continue
        if ima_jedenja and opcija == '1' and (abs(potez[0][0] - potez[1][0]) + abs(potez[0][1] - potez[1][1]) == 2):
            continue  # preskacem potez koji nema jedenja u sebi

        pojeden = []
        play_move(potez, board, pojeden)

        tren_value = minimax(board, depth - 1, max_depth, not maximizing_player, opposite_player(player), alpha, beta,
                             opcija, tren_time)

        if maximizing_player:
            if tren_value > value:
                value = tren_value
                best_potez = potez
            if tren_value == value and state_of_board(board) > value:
                best_potez = potez
            alpha = max(alpha, value)
        else:
            if tren_value < value:
                value = tren_value
                best_potez = potez
            if tren_value == value and state_of_board(board) < value:
                best_potez = potez

            beta = min(beta, value)
        '''if depth == max_depth:
            print("tren value: ", tren_value, " best_value: ", value)
            print("Best potez: ", best_potez)'''

        restore_board(board, pojeden)
        if beta <= alpha:
            break

        if time.time() - tren_time > EXECTIME:
            break

    if depth == max_depth:
        '''print("\nDostupni potezi:")
        for potez in potezi:
            print(potez)
        print("_"*10)
        print("Best potez", best_potez, end=' ')'''
        pojeden = []
        play_move(best_potez, board, pojeden)

    return value
