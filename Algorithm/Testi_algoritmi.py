import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
'''
def createdata(L,K):
    data = np.zeros((L, 3))
    samanlaisia = int (L/6)
    print("samanlaisia =", samanlaisia)

    for x in range(0,samanlaisia):
        data[x,:] = np.array([1200,1500,1500])

    for x in range(samanlaisia,2*samanlaisia):
        data[x,:] = np.array([1800,1500,1500])    

    for x in range(2*samanlaisia,3*samanlaisia):
        data[x,:] = np.array([1500,1200,1500])     

    for x in range(3*samanlaisia,4*samanlaisia):
        data[x,:] = np.array([1500,1800,1500]) 

    for x in range(4*samanlaisia,5*samanlaisia):
        data[x,:] = np.array([1500,1500,1200]) 

    for x in range(5*samanlaisia,6*samanlaisia):
        data[x,:] = np.array([1500,1500,1800])     

    kohina = K*np.random.randn(L,3)
    yhdistetty = data + kohina
    return yhdistetty
'''
def algoritmi(data1, centralpoints, iterations):

    max_values = np.max(data1, axis=0)
    min_values = np.min(data1, axis=0)

    randomPoints = (max_values - min_values) * np.random.rand(centralpoints, 3) + min_values

    for _ in range(iterations):
        CumSum = np.zeros((centralpoints, 3))
        Counts = np.zeros((1, centralpoints))

        for point in data1:
            distances = np.linalg.norm(randomPoints - point, axis=1)

            winner = np.argmin(distances)

            CumSum[winner] += point
            Counts[0, winner] += 1
            #print("random points1", randomPoints)
            #print("cumsum", CumSum)
            #print("counts", Counts)
            for i in range(centralpoints):
                if Counts[0, i] > 0:
                    randomPoints[i] = CumSum[i] / Counts[0, i]
                else:
                    randomPoints[i] = (max_values - min_values) * np.random.rand(1, 3) + min_values
    return randomPoints

#data1 = createdata(L=300, K=20)

file_path = 'C:\python\Sovellusprojekti_S23\\vastaanotetut_datat.txt'
data1 = np.loadtxt(file_path, dtype ='int',usecols=(6, 7, 8))
#data1 = data1.reshape((-1, 3)) 
print(data1)
centralpoints = 6
algoritmi_iterations = 20
numOfrows = len(data1)

lopulliset_keskipisteet = algoritmi(data1, centralpoints, algoritmi_iterations)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(data1[:, 0], data1[:, 1], data1[:, 2], c='r', marker='o', label='Data')
ax.scatter(lopulliset_keskipisteet[:, 0], lopulliset_keskipisteet[:, 1], lopulliset_keskipisteet[:, 2], c='b', marker='x', s=200, label='Keskipisteet')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.legend()

sorted_indices = np.argsort((lopulliset_keskipisteet[:, 0]))
lopulliset_keskipisteet = lopulliset_keskipisteet[sorted_indices]

plt.show()
#print("lopulliset Keskipisteet", lopulliset_keskipisteet)

tiedostonimi = 'keskipisteet.h'

with open(tiedostonimi, 'w') as tiedosto:
    tiedosto.write('int CP[{}][3]={{\n'.format(len(lopulliset_keskipisteet)))

    for i, keskipisteet in enumerate(lopulliset_keskipisteet):
        tiedosto.write('{{{},{},{}}}, // keskipiste {}, missa x={}, y={}, z={}\n'.format(
            int(keskipisteet[0]), int(keskipisteet[1]), int(keskipisteet[2]),
            i + 1, int(keskipisteet[0]), int(keskipisteet[1]), int(keskipisteet[2])
        ))

    tiedosto.write('};\n')

print("Tiedosto", tiedostonimi, "luotu onnistuneesti.")
maxValueIndex = np.max(lopulliset_keskipisteet, axis=1)   
 
print("Max values of row are at following columns :")
print(maxValueIndex)
print (np.lexsort((lopulliset_keskipisteet[:, 1], lopulliset_keskipisteet[:, 0])))




