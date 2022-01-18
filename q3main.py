import sys

def print_matrix(mat):
    print("-------")
    for i in mat:
        for ii in i:
            for iii in range(3 - len(str(ii))):
                print(" ", end = "")
            print(ii, end = " ")
        print()
    print("-------")

if len(sys.argv) < 2:
    print("Too few arguments") 
    exit()
elif len(sys.argv) > 3:
    print("Too many arguments") 
    exit()

a_inp = -1
try:
    q_no = int(sys.argv[1])
except:
    print("Invalid argument. Arguments must be integers.")
    exit()

if q_no < 1 or q_no > 4:
    print("Invalid question number. Question number must be <= 4 and >= 1.")
    exit()

if len(sys.argv) != 2:
    try:
        a_inp = int(sys.argv[2])
    except:
        print("Invalid argument. Arguments must be integers.")
        exit()

alpha = 0
if q_no == 3:
    if a_inp != -1:
        alpha = a_inp
    else:
        alpha = 1

vocab_len = 44020

Nspam = 0
Nnormal = 0

print("Taking y_train")
# Take y_train
file = open("y_train.csv", "r")

y_train = []
for x in file:
    y_train.append(int(x))
    if int(x) == 0:
        Nnormal += 1
    else:
        Nspam += 1

file.close()

N = Nspam + Nnormal

if q_no == 1:
    # Q 3.1
    print("There are" , N, "emails, where", Nspam, "of them are spams and", Nnormal, "of them are not")
    print("%" + str(100*Nspam/N), "spams and", "%" + str(100*Nnormal/N), "not spams")
    exit()

print("Taking vocabulary")
# Take the vocabulary
vocabulary = {}
file = open("vocabulary.txt", "r")

print("Taking x_train")
# Take x_train
x_train = [[int(u) for u in line.split(',')] for line in open("x_train.csv", "r")]

for x in file:
    line = x.split(",")
    vocabulary[line[0]] = int(line[1]) 
file.close()

print("Calculating MLE's")
# Calculate Tj's

Tjspam = []
Tjnormal = []

for i in range(vocab_len):
    sp = 0
    nm = 0
    for j in range(len(x_train)):
        number = x_train[j][i]
        if q_no == 4 and number > 0:
            number = 1
        if y_train[j] == 0:
            sp += number
        else:
            nm += number
    Tjspam.append(sp)
    Tjnormal.append(nm)

# Calculate Thetaj's
Thetajspam = []
Thetajnormal = []

spS = 0
nmS = 0
if q_no != 4:
    spS = sum(Tjspam)
    nmS = sum(Tjnormal)
else:
    spS = Nspam
    nmS = Nnormal
    
for i in range(vocab_len):
    Thetajspam.append((Tjspam[i]+ alpha) / (spS + alpha * vocab_len))
    Thetajnormal.append((Tjnormal[i]+alpha) / (nmS + alpha * vocab_len))

PIynormal = Nnormal/N
PIyspam = Nspam / N    


print("Taking x_test")

x_test = [[int(u) for u in line.split(',')] for line in open("x_test.csv", "r")]

print("Taking y_test")

# Take y_test
file = open("y_test.csv", "r")

y_test = []
for x in file:
    y_test.append(int(x))

file.close()
print("Testing results")

conf_matrix = [[0,0],[0,0]]
b = 0
for x in x_test:
    a = 0
    Pspam = PIyspam
    Pnormal = PIynormal
    for y in x:
        Pspam *= Thetajspam[a]**y
        Pnormal *= Thetajnormal[a]**y
        a += 1
    result = -1
    if Pspam >= Pnormal:
        result = 0
    else:
        result = 1

    if result == 1 and y_test[b] == 1:
        conf_matrix[0][0] += 1
    elif result == 1 and y_test[b] == 0:
        conf_matrix[0][1] += 1
    elif result == 0 and y_test[b] == 1:
        conf_matrix[1][0] += 1
    elif result == 0 and y_test[b] == 0:
        conf_matrix[1][1] += 1

    b += 1

true_count = conf_matrix[0][0] + conf_matrix[1][1]
false_count = conf_matrix[1][0] + conf_matrix[0][1]

print("----------------------------")
print("Results")
print("----------------------------")
print("Accuracy rate:", true_count * 100 / (true_count + false_count) )
print("Confusion matrix: ")
print_matrix(conf_matrix)

print("Number of wrong predictions:", false_count)
