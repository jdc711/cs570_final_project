

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
#   |_|_|_|_|S|
#   |_|_|_|_|_|
#   |_|_|_|_|_|
#   |_|_|_|_|_|
#   0         n

# order of iteration:
#   3)  ---->S
#   2)  ----->
#   1)  ----->


# We will go left to right, computing row by row starting from the bottom row

def MISMATCH(x, y):
    return 2



def basic_seq_align(X, Y, gap_pen):
    m = len(X)
    n = len(Y)
    # define 2d list OPT
    OPT = []
    for i in range(n):
        col = []
        OPT.append(col)

    # initialize necessary locations of OPT array
    for i in range(m):
        OPT[i][0] = i*gap_pen
    for j in range(n):
        OPT[0][j] = j*gap_pen

    # compute value of OPT solution BOTTOM UP; optimal value will be found at OPT[m][n]
    for i in range(1, m):
        for j in range(1, n):
            OPT[m][n] = min((OPT(m-1, n-1) + MISMATCH(X[m], Y[n])),
                            (OPT(m-1, n) + gap_pen), (OPT(m, n-1) + gap_pen))
    
    # Build optimal solution TOP DOWN
    i = m
    j = n
    
    X_sol = ""
    Y_sol = ""


    
    
    while (i >= 0 and j >= 0):
        # compare OPT[i][j] with 1) OPT[i-1][j] (if Xm is mismatched), 2) OPT[i][j-1] (if Yn is mismatched), 3) OPT[i-1][j-1] (if (Xm,Yn) is in our optimal solution
        if OPT[i][j] == OPT[i-1][j] + gap_pen:
            # Xi is mismatched with gap, append gap to end of X_sol
            X_sol = X_sol + '_'
            i = i - 1
        elif OPT[i][j] == OPT[i][j-1] + gap_pen:
            # Yj is mismatched with gap, append gap to end of Y_sol
            Y_sol = Y_sol + '_'
            j = j - 1
        elif OPT[i][j] == OPT[i-1][j-1]:
            # (Xi,Yj) is in our optimal solution; append Xi to X_sol and Yj to Y_sol
            X_sol = X_sol + X[i]
            Y_sol = Y_sol + Y[j]
            i = i - 1
            j = j - 1
        
        