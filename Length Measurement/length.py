import numpy as np
import csv
import matplotlib.pyplot as plt

# read in length info with corresponding index
indecies = []
length = []
with open("length_only.txt") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    for row in csv_reader:
        indecies.append(int(row[0].split(":")[0]))
        length.append(float(row[0].split(":")[1]))

#print(indecies)
#print(length)
#print("before removing outliers: (scale: m)")
#print("standard length: 0.32")
#print("mean: "+str(round(np.mean(length), 3)))
#print("standard deviation: "+str(round(np.std(length), 3)))
 
# as a standard reference
idx = np.arange(106)
len = 0.32*np.ones(106)

plt.figure()
plt.subplot(1,2,1)
plt.plot(indecies, length, 'ro')
plt.plot(idx, len, 'b')
plt.xlabel('indecies for images')
plt.ylabel('length/m')
plt.title('before removing outliers')

# remove outliers
length_new = []
indecies_new = []
for i in range (np.shape(length)[0]):
    if length[i] < 0.4:
        length_new.append(length[i])
        indecies_new.append(indecies[i])

#print("after removing outliers: (scale: m)")
#print("standard length: 0.32")
#print("mean: "+str(round(np.mean(length_new), 3)))
#print("standard deviation: "+str(round(np.std(length_new), 3)))

# save mean and standard deviation after removing outliers
f = open("length_info.txt", mode = 'w')
f.write("before removing outliers: (scale: m)\n")
f.write("standard length: 0.32\n")
f.write("mean: "+str(round(np.mean(length), 3))+"\n")
f.write("standard deviation: "+str(round(np.std(length), 3))+"\n")
f.write("\n")
f.write("after removing outliers: (scale: m)\n")
f.write("standard length: 0.32\n")
f.write("mean: "+str(round(np.mean(length_new), 3))+"\n")
f.write("standard deviation: "+str(round(np.std(length_new), 3))+"\n")

plt.subplot(1,2,2)
plt.plot(indecies_new, length_new, 'ro')
plt.plot(idx, len, 'b')
plt.xlabel('indecies for images')
plt.ylabel('length/m')
plt.title('after removing outliers')

plt.suptitle('Fish Length for Images')
plt.savefig('fish_length_result.png')
plt.show()

