import time
import tracemalloc
import sys

# Define meaning of OPT solution:
# OPT solution is the minimum cost alignment of 2 strings: X = "X1X2X3...Xm" and Y = "Y1Y2Y3...Yn"

# Define meaning of value of OPT solution:
# Value of OPT(m,n) = the minimum cost of the optimal alignment between X = "X1X2X3...Xm" and Y = "Y1Y2Y3...Yn"

# Define subproblems:
# Either (Xm,Yn) is in the OPT solution or not. If (Xm,Yn) is not in OPT solution, either 1) Xm is matched with a gap (Xm is "mismatched") or 2) Yn is matched with a gap (Yn is "mismatched")

# Recursive Definition of the subproblems
# if (Xm,Yn) is in OPT:
# OPT(m,n) = OPT(m-1,n-1) + MISMATCH(Xm,Yn)  #--> MISMATCH(char a,char b) function outputs the mismatch cost between letters a and b
# if Xm is mismatched:
# OPT(m,n) = OPT(m-1,n) + GAP_PEN
# if Yn is mismatched:
# OPT(m,n) = OPT(m,n-1) + GAP_PEN

# Recursive Definition of OPT(m,n)
# OPT(m,n) = min((OPT(m-1,n-1) + MISMATCH(Xm,Yn)),
#                (OPT(m-1,n) + GAP_PEN),
#                (OPT(m,n-1) + GAP_PEN))
#


# Compute Values of 2d array OPT (mxn)

#  m___________
#   |_|_|_|_|S|    <--------This row represents opt cost between Y1....Ym and
#   |_|_|_|_|_|
#   |_|_|_|_|_|
#   |_|_|_|_|_|
#   0         n

# order of iteration:
#   3)  ---->S
#   2)  ----->
#   1)  ----->


# We will go left to right, computing row by row starting from the bottom row

def parseInputfile(fileName):
    with open(fileName) as f:
        lines = f.read().splitlines()
    f.close()

    X = ""
    Y = ""
    baseSeq = ""
    for i in lines:
        if i.isnumeric():
            first = baseSeq[:int(i) + 1]
            second = baseSeq[int(i) + 1:]
            baseSeq = first + baseSeq + second
        else:  # this is the base sequence
            if baseSeq != "":
                # print(baseSeq)
                X = baseSeq
            baseSeq = i

    Y = baseSeq
    return X, Y


def MISMATCH(x, y):
    Dict = {'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
            'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
            'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
            'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}}
    return Dict[x][y]


def checkMinAlign(X, Y, gap_pen):
    i = len(X)
    cost = 0
    while (i > 0):
        if (X[i-1] == '_' or Y[i-1] == '_'):
            cost = cost + gap_pen
        else:
            cost = cost + MISMATCH(X[i-1], Y[i-1])
        i = i - 1
    return cost


# this gives us the optimal split point (index) of Y
def find_opt_Y_split(X, Y, gap_pen):

    m = len(X)
    n = len(Y)
    print("X in OPT SPLIT:",X)
    print("Finding OPT SPLIT For Y:", Y)
    
    # define 2d list OPT
    OPT = []
    # DOUBLE CHECK: INITIALZIED SMALL 2D GRID (2 by n+1)
    for i in range(2):
        OPT.append([])
        for j in range(n+1):
            OPT[i].append(0)

    # initialize necessary locations of OPT array
    # special note! in OPT grid, we reserve 0th row/col for "" and ""; the 1st row/col for "x1" and "y1";
    for i in range(0, 2):
        OPT[i][0] = i*gap_pen 

    for j in range(0, n+1):
        OPT[0][j] = j*gap_pen


    # compute value of OPT solution BOTTOM UP; the value we want will be found somewhere in the last row (OPT[1], since only 2 rows)

    # for i in range(1, m+1):  # 1 to m
    #     i = (i % 2)
    #     for j in range(1, n+1):  # 1 to n
    #         # DOUBLE-CHECK: OVERWRITING PREVIOUS ROW WE DONT NEED ANYORE; MAY NEED TO CHECK THIS; COULD BE WRONG
    #         # string is indexed by zero; to access ith character, subtract i-1
    #         OPT[i][j] = min((OPT[i-1][j-1] + MISMATCH(X[i-1], Y[j-1])),
    #                         (OPT[i-1][j] + gap_pen), (OPT[i][j-1] + gap_pen))
    #     # DOUBLE CHECK: REPLACING ROW 1 WITH CONTENTS OF ROW 2 BECAUSE WE DONT NEED ROW 2 ANYMORE
    #     for k in range(n+1):
    #         OPT[i-1][k] = OPT[i][k]   
    
    for i in range(1, m+1):  # 1 to m
        OPT[1][0] = i*gap_pen
        for j in range(1, n+1):  # 1 to n
            # DOUBLE-CHECK: OVERWRITING PREVIOUS ROW WE DONT NEED ANYORE; MAY NEED TO CHECK THIS; COULD BE WRONG
            # string is indexed by zero; to access ith character, subtract i-1
            OPT[1][j] = min((OPT[0][j-1] + MISMATCH(X[i-1], Y[j-1])),
                            (OPT[0][j] + gap_pen), (OPT[1][j-1] + gap_pen))
        # DOUBLE CHECK: REPLACING ROW 1 WITH CONTENTS OF ROW 2 BECAUSE WE DONT NEED ROW 2 ANYMORE
        for k in range(n+1):
            OPT[0][k] = OPT[1][k] 

   
    return OPT[1]


def basic_seq_align(X, Y, gap_pen):

    m = len(X)
    n = len(Y)
    # define 2d list OPT
    OPT = []
    for i in range(m+1):
        OPT.append([])
        for j in range(n+1):
            OPT[i].append(0)

    # initialize necessary locations of OPT array
    # special note! in OPT grid, we reserve 0th row/col for "" and ""; the 1st row/col for "x1" and "y1"; the 2nd row/col for "x1x2" and "y1y2"
    for i in range(0, m+1):
        OPT[i][0] = i*gap_pen

    for j in range(0, n+1):
        OPT[0][j] = j*gap_pen

    # compute value of OPT solution BOTTOM UP; optimal value will be found at OPT[m][n]

    for i in range(1, m+1):  # 1 to m
        for j in range(1, n+1):  # 1 to n
            # string is indexed by zerp; to access ith character, subtract i-1
            OPT[i][j] = min((OPT[i-1][j-1] + MISMATCH(X[i-1], Y[j-1])),
                            (OPT[i-1][j] + gap_pen), (OPT[i][j-1] + gap_pen))

    # Build optimal solution TOP DOWN
    i = m
    j = n

    X_sol = ""
    Y_sol = ""

    while (i > 0 and j > 0):
        # compare OPT[i][j] with 1) OPT[i-1][j] (if Xm is mismatched), 2) OPT[i][j-1] (if Yn is mismatched), 3) OPT[i-1][j-1] (if (Xm,Yn) is in our optimal solution
        if OPT[i][j] == OPT[i-1][j] + gap_pen:
            # Xi is mismatched with gap, append gap to end of Y_sol and Xi to end of X_sol
            X_sol = X[i-1] + X_sol
            Y_sol = '_' + Y_sol
            i = i - 1
            # print("X: ", X_sol)
            # print("Y: ", Y_sol)
        elif OPT[i][j] == OPT[i][j-1] + gap_pen:
            # Yj is mismatched with gap, append gap to end of X_sol and Yj to end of Y_sol
            Y_sol = Y[j-1] + Y_sol
            X_sol = '_' + X_sol
            j = j - 1
            # print("X: ", X_sol)
            # print("Y: ", Y_sol)
        elif OPT[i][j] == OPT[i-1][j-1] + MISMATCH(X[i-1], Y[j-1]):
            # (Xi,Yj) is in our optimal solution; append Xi to X_sol and Yj to Y_sol
            X_sol = X[i-1] + X_sol
            Y_sol = Y[j-1] + Y_sol
            i = i - 1
            j = j - 1
            # print("X: ", X_sol)
            # print("Y: ", Y_sol)

    while (i > 0):
        X_sol = X[i-1] + X_sol
        Y_sol = '_' + Y_sol
        i = i - 1
    while (j > 0):
        Y_sol = Y[j-1] + Y_sol
        X_sol = '_' + X_sol
        j = j - 1

    # print("X: ", X_sol)
    # print("Y: ", Y_sol)
    return X_sol, Y_sol



def divideAndConquer(X, Y, GAP_PEN):
    # base case
    if (len(X)<=2 or len(Y)<=2):
        return basic_seq_align(X, Y, GAP_PEN)
    else:
        print("X before split:", X)
        print("Y before split:", Y)
        
        # split X in equal halves
        Xleft = X[:len(X)//2]
        Xright = X[len(X)//2:]
       
    
        # Find optimal split point for Y
        
        # Find minimum cost alignments between Xleft and "Y1", "Y1Y2", "Y1Y2Y3",...., "Y1Y2Y3..Yk"
        
        opt_row1 = find_opt_Y_split(Xleft, Y, GAP_PEN)
        # opt_row1[K] = min cost of alignment between Xleft and "Y1....YK"                                                               
        print(opt_row1)   
        
        # Find minimum cost alignments between Xright_reversed and "Yk", "YkYk-1", ...., "Yk...Y3Y2Y1"
        Xright_reversed = Xright[::-1]
        Yreversed = Y[::-1]
        
        # opt_row1[n-K] = min cost of alignment between Xright and "YK+1....Yn"
        opt_row2 = find_opt_Y_split(Xright_reversed, Yreversed, GAP_PEN)
        print(opt_row2)
        
        # Find optimal split point that gives us the smallest cost                                                        
        minCost = 100000000
        opt_split_pt = 0                                                             
        for i in range(len(opt_row1)):
            # To find cost of alignment of splitting Y at split point K, get opt_row1[K] + opt_row[n-K]
                    # opt_row1[K] = min cost of alignment between Xleft and "Y1....YK"
                    # opt_row1[n-K] = min cost of alignment between Xright and "YK+1....Yn"
            j = len(opt_row1) - i - 1
            if (minCost > opt_row1[i] + opt_row2[j]):
                minCost = opt_row1[i] + opt_row2[j]
                opt_split_pt = i
        
        
        # Split Y at optimal split point
        Yleft, Yright = Y[:opt_split_pt], Y[opt_split_pt:]
        
        # DEBUG: Print out left and right halves of X and Y after splitting
        print("Xleft: ", Xleft)
        print("Yleft: ", Yleft)
        print("Xright: ", Xright)
        print("Yright: ", Yright)
        print("")
     
        # Recursive calls on both segment halves (left half of X with left half of Y, right half of X with right half of Y)
        X_sol1, Y_sol1 = divideAndConquer(Xleft, Yleft, GAP_PEN)
        X_sol2, Y_sol2 = divideAndConquer(Xright, Yright, GAP_PEN)
        # Combine Step: Concatenate the Alignments we get from both halves
        return X_sol1 + X_sol2, Y_sol1 + Y_sol2




def main():

    t0 = time.time()
    tracemalloc.start()

    filename = sys.argv[1]
    inputSeq = parseInputfile(filename)
   
    X = inputSeq[0]
    Y = inputSeq[1]
    # X = "ATCGATCGATCGATCG"
    # Y = "ATCGATCGATCGATCG"
    
    print("Original X: ", X)
    print("Original Y: ", Y)
    
    # DIVIDE AND CONQUER

    # Conquer (This step requires DP!!!): Find the optimal alignment between 1) left segments (X1 and Y1),  and 2) right segments (X2 and Y2)
    # Combine: Concatenate the two optimal alignments found above

    # What is base case? one of the segment's length == 0
    # Then you just add gaps to match the other segment

    # For conquer step above, we need to use DP to find the optimal split point for Y (to cut into Y1 and Y2)

    # X="ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG"

    # Y="TATTATTATACGCTATTATACGCGACGCGGACGCGTATACGCTATTATACGCGACGCGGACGCG"

    
    
    gap_pen = 30

    # start timer and memory
    X_sol, Y_sol = divideAndConquer(X, Y, gap_pen)

    X_sol1 , Y_sol2 = basic_seq_align(X, Y, gap_pen)
    print("          Correct  X Allignment: ", X_sol1)
    print("          Correct  Y Allignment: ", Y_sol2)
    
    print("Our current Memory X Allignment: ", X_sol)
    print("Our current Memory Y Allignment: ", Y_sol)
    t1 = time.time()
    totalTime = t1-t0
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    total = 0
    for stat in top_stats:
        print(stat)
        total += stat.size
    print(total)
    print("total time ", totalTime, " seconds")
    print("cost of correct alignment: ", checkMinAlign(X_sol1, Y_sol2, gap_pen))
    print("cost of our memory  alignment: ", checkMinAlign(X_sol, Y_sol, gap_pen))


if __name__ == "__main__":

    main()
