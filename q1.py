def transpose(X):
    return [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]

def multiply(X, Y):
    if k <= 10:
        return [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)] for X_row in X]

    X_row = X[0]
    return [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)]]



# Get k from command line argument
import sys

if len(sys.argv) == 1:
    print("Wrong number of arguments. Call with k.")
    exit()
k = int(sys.argv[1])

# Read data
import csv
class OK(Exception): pass
data = []
for i in range(2304):
    data.append([])
file = open('images.csv')
csvreader = csv.reader(file)
next(csvreader)

for row in csvreader:
    for i in range(len(row)):
        data[i].append(int(row[i]))
file.close()
print("Data extracted from csv")

#Show
tr_data = transpose(data)
from PIL import Image

image = Image.new(mode="L", size=(48, 48))
image.putdata(tr_data[0])
image.show()

# Mean center
means = []
for feature in data:
    mean = sum(feature)/len(feature)

    for x in range(len(feature)):
        feature[x]-= mean
    means.append(mean)
print("Data is mean centered")

#####################################################################################
# Covariance matrix computation
def covariance(x, y):
    n = len(x)
    summ = 0
    # means of x and y are 0
    # since they are mean centered
    for i in range(n):
        summ += x[i]*y[i]
    return summ/n

covariance_matrix = []
for i in data:
    new_row = []
    for j in data:
        new_row.append(covariance(i,j))
    covariance_matrix.append(new_row)
print("Covariance matrix computed")

# Write covariance matrix to file
with open("cov_mat.csv","w+") as my_csv:
    csv_writer = csv.writer(my_csv,delimiter=',')
    csv_writer.writerows(covariance_matrix)
print("Written to file")
####################################################################################
# Read covariance matrix from file
covariance_matrix = []
file = open('cov_mat.csv')
csvreader = csv.reader(file)

for row in csvreader:
    r = []
    for cell in row:
        #print(cell)
        r.append(float(cell))
    covariance_matrix.append(r)

print("Readed covariance matrix from file")

# Eigenvalues and Eigenvectors computation
import numpy as np
from numpy.linalg import eig

values, vectors = eig(np.array(covariance_matrix))

print("Computed eigenvalues and eigenvectors")

# Calculate feature vector
feature_vector = []
for i in range(len(values)):
    if len(feature_vector) < k:
        feature_vector.append([values[i], vectors[i]])
    elif values[i] > feature_vector[-1][0]:
        feature_vector[-1] = [values[i], vectors[i]]
    for j in range(len(feature_vector)-1, 0, -1):
        #print(j)
        if feature_vector[j] > feature_vector[j-1]:
            temp = feature_vector[j]
            feature_vector[j] = feature_vector[j-1]
            feature_vector[j-1] = temp
        else:
            break

correct_sorted_vectors = []

try:
    for i in range(len(values)):
        for j in feature_vector:
            if j[0] == values[i]:
                correct_sorted_vectors.append(j)
                if len(correct_sorted_vectors) == k:
                    raise OK
except OK:
    pass

#feature_vector = correct_sorted_vectors
print("Calculated feature vector")

# Calculate PVEs

print('PVEs:')

total_variance = 0
sumvar = 0
for i in range(len(covariance_matrix)):
    total_variance += covariance_matrix[i][i]

for i in range(len(feature_vector)):
    result = feature_vector[i][0] * 100 / total_variance
    if k == 10:
        print(result)
    sumvar += result
print("Sum PVE", sumvar)
for i in range(len(feature_vector)):
    feature_vector[i] = feature_vector[i][1]

# Compress


# print(len(data),len(data[0]))
# print(len(feature_vector),len(feature_vector[0]))

tr_feature = transpose(feature_vector)
tr_data = transpose(data)

# print(len(tr_data), len(tr_data[0]))
# print(len(tr_feature), len(tr_feature[0]))

result = multiply(tr_data, tr_feature)
tr_result = transpose(result)

print(len(result), len(result[0]))

print("Compression done")

# Reconstruct data

reconstructed_data = multiply(result, feature_vector)

# print(len(means))
# print(len(reconstructed_data))
# print(len(reconstructed_data[0]))

for i in range(len(reconstructed_data)):
    for j in range(len(reconstructed_data[i])):
        reconstructed_data[i][j] += means[j]

print("Reconstruction done")

# print(reconstructed_data[0][:5])
# print(reconstructed_data[1][:5])
# print(reconstructed_data[2][:5])
# print(reconstructed_data[3][:5])

image = Image.new(mode="L", size=(48, 48))
image.putdata(reconstructed_data[0])
image.show()
