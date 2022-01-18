import csv
from math import sqrt

def k_nearest_manhattan(dataset, labels, test_labels, k, uf ):
    priority_queue = []

    for i in range(len(dataset[0])):
        dist = 0
        for j in range(len(dataset)):
            if uf[j] == True:
                dist += abs(float(dataset[j][i])-float(test_labels[j]))
        if len(priority_queue) < k:
            priority_queue.append([dist, labels[i]])
        elif priority_queue[-1][0] > dist:
            priority_queue[-1] = [dist, labels[i]]
        else:
            continue

        for j in range(1, len(priority_queue)):
            if priority_queue[-j][0] < priority_queue[-(j+1)][0]:
                temp = priority_queue[-j]
                priority_queue[-j] = priority_queue[-(j+1)]
                priority_queue[-(j+1)] = temp
            else:
                break

    one_count = 0
    zero_count = 0

    for xxx in priority_queue:
        if int(xxx[1]) == 0:
            zero_count += 1
        else:
            one_count += 1

    if zero_count > one_count:
        return 0
    return 1

def k_nearest_euclidian(dataset, labels, test_labels, k, uf ):
    priority_queue = []

    for i in range(len(dataset[0])):
        dist = 0
        for j in range(len(dataset)):
            if uf[j] == True:
                dist += (abs(float(dataset[j][i])-float(test_labels[j])))**2
        dist = sqrt(dist)
        if len(priority_queue) < k:
            priority_queue.append([dist, labels[i]])
        elif priority_queue[-1][0] > dist:
            priority_queue[-1] = [dist, labels[i]]
        else:
            continue

        for j in range(1, len(priority_queue)):
            if priority_queue[-j][0] < priority_queue[-(j+1)][0]:
                temp = priority_queue[-j]
                priority_queue[-j] = priority_queue[-(j+1)]
                priority_queue[-(j+1)] = temp
            else:
                break

    one_count = 0
    zero_count = 0

    for xxx in priority_queue:
        if int(xxx[1]) == 0:
            zero_count += 1
        else:
            one_count += 1

    if zero_count > one_count:
        return 0
    return 1

def eval(test_features, train_features, train_labels, k, use_features, prnt):
    conf_matrix = [[0,0],[0,0]]
    for i in range(len(test_features)):
        result = k_nearest_euclidian(train_features, train_labels,
                                     test_features[i], k, use_features)

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

                results.append(result)

    if prnt:
        print("Confusion Matrix:")
        print(conf_matrix[0][0], conf_matrix[0][1])
        print(conf_matrix[1][0], conf_matrix[1][1])

    trues = conf_matrix[0][0] + conf_matrix[1][1]
    total = conf_matrix[0][0] + conf_matrix[0][1] + conf_matrix[1][0] + conf_matrix[1][1]
    acc = trues / total

    if prnt:
        print("Accuracy:", str(acc*100) + "%")
    return acc


k = 9
#use_features = [False, True, False, True, True, False, True, False]

train_f = open('diabetes_train_features.csv')
train_l = open('diabetes_train_labels.csv')

csvreader = csv.reader(train_l)
next(csvreader)
train_labels = []

for row in csvreader:
    train_labels.append(row[1])

train_l.close()

train_f = open('diabetes_train_features.csv')
csvreader = csv.reader(train_f)

#train_features[i] = feature number i
train_features = [[],[],[],[],[],[],[],[]]

next(csvreader)
for row in csvreader:
    i = 0
    for f in row[1:]:
        train_features[i].append(f)
        i += 1

train_f.close()

## TEST
test_l = open('diabetes_test_labels.csv')
csvreader = csv.reader(test_l)
next(csvreader)

test_labels = []
for row in csvreader:
    test_labels.append(row[1])

test_l.close()

test_f = open('diabetes_test_features.csv')
csvreader = csv.reader(test_f)
headers = next(csvreader)[1:]

test_features = []

for row in csvreader:
    test_features.append(row[1:])

test_f.close()
results = []

use_features = [True, True, True, True, True, True, True, True]

print("Without Elimination")
maxAcc = eval(test_features, train_features, train_labels, k, use_features, True)
print()

print("Elimination Starts")
print()

flag = True
while flag:
    flag = False
    for j in range(len(use_features)):
        if use_features[j] == False:
            continue

        use_features[j] = False

        result = eval(test_features, train_features, train_labels, k, use_features, False)
        if result > maxAcc:
            maxAcc = result
            flag = True
        else:
            use_features[j] = True

#print("Max:", maxAcc)
#print(use_features)
print("Best Result")
best_acc = eval(test_features, train_features, train_labels, k, use_features, True)

print("Eliminated:")
for i in range(len(use_features)):
    if use_features[i] == False:
        print(headers[i])
