import csv
import sys

# Pull Training Data

train_f = open('sms_train_features.csv')

csvreader = csv.reader(train_f)
next(csvreader)
train_features = []

for row in csvreader:
    train_features.append(row[1:])

train_f.close()


train_l = open('sms_train_labels.csv')
csvreader = csv.reader(train_l)
next(csvreader)
train_labels = []

N0 = 0
N1 = 0
for row in csvreader:
    train_labels.append(row[1])

    if int(row[1]) == 0:
        N0 += 1
    else:
        N1 += 1

N = N0 + N1
train_l.close()

if sys.argv[1] == "0":
    multinomial = False
elif sys.argv[1] == "1":
    multinomial = True
else:
    print("Invalid argument. Enter 0 for bernoulli, 1 for multinomial")
    exit()
counts = [] # Tjnormal, Tjspam
probabilities = []
sum_counts0 =  0
sum_counts1 =  0
for i in range(len(train_features[0])): # no of words
    zero_count = 0
    one_count = 0

    for j in range(len(train_features)):
        lbl = int(train_labels[j])
        if multinomial:
            if lbl == 0:
                zero_count += int(train_features[j][i])
            else:
                one_count += int(train_features[j][i])
        else:
            occ = int(train_features[j][i])
            if occ > 0:
                if lbl != 0:
                    zero_count += 1
                else:
                    one_count += 1

    counts.append([zero_count, one_count])
    total_count = zero_count + one_count
    sum_counts0 += zero_count
    sum_counts1 += one_count
    if total_count != 0:
        probabilities.append([zero_count/total_count, one_count/total_count])
    else:
        probabilities.append([0, 0])

# TEST
test_f = open('sms_test_features.csv')

csvreader = csv.reader(test_f)
next(csvreader)
test_features = []

for row in csvreader:
    test_features.append(row[1:])

test_f.close()


test_l = open('sms_test_labels.csv')
csvreader = csv.reader(test_l)
next(csvreader)
test_labels = []

for row in csvreader:
    test_labels.append(row[1])

test_l.close()

pi0 = N0/N
pi1 = N1/N

print(pi0, pi1)
conf_matrix = [[0,0],[0,0]]
#print(sum_counts0, sum_counts1)

if multinomial:
    for i in range(len(test_features)): # for each word in vocab
        thetaj0 = counts[i][0]/sum_counts0
        thetaj1 = counts[i][1]/sum_counts1
        #print(thetaj0, thetaj1)
        p0 = pi0
        p1 = pi1

        for j in range(len(test_features[i])):

            if multinomial:
                p0 *= thetaj0**int(test_features[i][j])
                p1 *= thetaj1**int(test_features[i][j])
            else:
                p0 *= thetaj0
                p1 *= thetaj1


        result = 0

        if p0 < p1:
            result = 1

        if result == 1:
            if int(test_labels[i]) == 1:
                conf_matrix[0][0] += 1 # TP
            else:
                conf_matrix[1][0] += 1 # FP
        else:
            if int(test_labels[i]) == 1:
                conf_matrix[0][1] += 1 # FN
            else:
                conf_matrix[1][1] += 1 # TN

    print("Confusion Matrix:")
    print(conf_matrix[0][0], conf_matrix[0][1])
    print(conf_matrix[1][0], conf_matrix[1][1])

    trues = conf_matrix[0][0] + conf_matrix[1][1]
    total = conf_matrix[0][0] + conf_matrix[0][1] + conf_matrix[1][0] + conf_matrix[1][1]
    acc = trues / total
    print("Accuracy:", str(acc*100) + "%")

else:
    noOfFeatures = 100

    while noOfFeatures <= 600:
        conf_matrix = [[0,0],[0,0]]
        for i in range(noOfFeatures): # for each word in vocab
            thetaj0 = counts[i][0]/sum_counts0
            thetaj1 = counts[i][1]/sum_counts1
            #print(thetaj0, thetaj1)
            p0 = pi0
            p1 = pi1

            for j in range(len(test_features[i])):

                if multinomial:
                    p0 *= thetaj0**int(test_features[i][j])
                    p1 *= thetaj1**int(test_features[i][j])
                else:
                    p0 *= thetaj0
                    p1 *= thetaj1


            result = 0

            if p0 < p1:
                result = 1

            if result == 1:
                if int(test_labels[i]) == 1:
                    conf_matrix[0][0] += 1 # TP
                else:
                    conf_matrix[1][0] += 1 # FP
            else:
                if int(test_labels[i]) == 1:
                    conf_matrix[0][1] += 1 # FN
                else:
                    conf_matrix[1][1] += 1 # TN

        print(noOfFeatures, "featues")
        print("Confusion Matrix:")
        print(conf_matrix[0][0], conf_matrix[0][1])
        print(conf_matrix[1][0], conf_matrix[1][1])

        trues = conf_matrix[0][0] + conf_matrix[1][1]
        total = conf_matrix[0][0] + conf_matrix[0][1] + conf_matrix[1][0] + conf_matrix[1][1]
        acc = trues / total
        print("Accuracy:", str(acc*100) + "%")
        noOfFeatures += 100
