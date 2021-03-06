import time
import tracemalloc
import psutil
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
        else: #this is the base sequence
            if baseSeq != "":
                #print(baseSeq)
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

    for i in range(1, m+1): # 1 to m
        for j in range(1, n+1): # 1 to n 
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
    
    
    
    
    #print("X: ", X_sol)
    #print("Y: ", Y_sol)
    return X_sol, Y_sol
    


def process_memory():
    process = psutil.Process()
    mem_info = process.memory_info()
    mem = mem_info.rss/(1024)
    return mem

def main():

    
    filename = sys.argv[1]
    inputSeq = parseInputfile(filename)
    #print(inputSeq[0])
    #print(inputSeq[1])

    X = inputSeq[0]
    Y = inputSeq[1]

    
    #X="ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG"

    #Y="TATTATTATACGCTATTATACGCGACGCGGACGCGTATACGCTATTATACGCGACGCGGACGCG"
    

    gap_pen = 30
    
    #start timer and memory 
    t0 = time.time()
    mem_before = process_memory()
    X_sol, Y_sol = basic_seq_align(X, Y, gap_pen)
    mem_after = process_memory()
    t1 = time.time()
    totalTime = t1-t0
    print("Lenght of m+n", len(X_sol+Y_sol))

    if(len(X_sol) >= 50):
        X_sol_start = X_sol[ 0 : 50 ]
        X_sol_end = X_sol[-50:]
    else:
        X_sol_start = X_sol
        X_sol_end = X_sol
    if(len(Y_sol) >= 50):
        Y_sol_start = Y_sol[ 0 : 50 ]
        Y_sol_end = Y_sol[-50:]
    else:
        Y_sol_start = Y_sol
        Y_sol_end = Y_sol

    #X_sol1 , Y_sol2 = basic_seq_align(X, Y, gap_pen)

    f = open("output.txt", "w")
    f.write(X_sol_start + " " + X_sol_end + "\n")
    f.write(Y_sol_start + " " + Y_sol_end +  "\n")
    f.write(str(checkMinAlign(X_sol, Y_sol, gap_pen) / 1.0) + "\n" )
    f.write(str(totalTime) + "\n")
    f.write(str(mem_after-mem_before) + "\n")
    f.close()
    
    #print("memory", mem_after - mem_before)
    #print("total time ", totalTime, " seconds")
    #print("cost of alignment: ", checkMinAlign(X_sol, Y_sol, gap_pen))



if __name__ == "__main__":

    main()
   