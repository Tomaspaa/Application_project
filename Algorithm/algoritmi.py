import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

'''
def laskeEtaisyys(p1, p2):
    
    p1 = np.array([1, 1, 1])
    p2 = np.array([2, 2, 2])

    etaisyys = np.sqrt(np.sum((p1 - p2) ** 2))
    etaisyys2 = np.linalg.norm(p1 - p2)
    
    print("Etäisyys manuaalisesti laskettuna:", etaisyys)
    print("Etäisyys np.linalg.norm -funktiolla:", etaisyys2)

laskeEtaisyys('p1', 'p2')
'''

file_path = 'C:\python\Sovellusprojekti_S23\\vastaanotetut_datat.txt'
data = np.loadtxt(file_path, usecols=(6, 7, 8))
print(data)
data = data.reshape((-1, 3)) 
numOfrows = len(data)

centralpoints = 6
max_values = np.max(data, axis=0)
min_values = np.min(data, axis=0)

randomPoints = (max_values - min_values) * np.random.rand(centralpoints, 3) + min_values

CumSum = np.zeros((centralpoints, 3))
Counts = np.zeros((1, centralpoints))
Distances = np.zeros((1, centralpoints))

for point in data:
    distances = np.linalg.norm(randomPoints - point, axis=1)

    winner = np.argmin(distances)

    CumSum[winner] += point
    Counts[0, winner] += 1


randomPoints = CumSum / Counts.reshape(-1, 1)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(data[:, 0], data[:, 1], data[:, 2], c='r', marker='o', label='Data')
ax.scatter(randomPoints[:, 0], randomPoints[:, 1], randomPoints[:, 2], c='b', marker='x', s=200, label='Keskipisteet')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.legend()

plt.show()
print("Keskipisteet", randomPoints)
print("Counts", Counts)
print("Distances", distances)
print("cum sum", CumSum)


for i in range(numOfrows):
    distances = np.linalg.norm(randomPoints - data[i], axis=1)
    winner = np.argmin(distances)

    Counts[0, winner] += 1
    CumSum[winner] += data[i]

