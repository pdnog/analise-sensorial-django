import numpy as np
import itertools
def transposeMatrix(m):
    return [[ m[row][col] for col in range(0,width) ] for row in range(0,height) ]
    
matriz = [[1,2,3],[4,5,6]]
""""a = np.array(matriz)
b = a.transpose()
print(b)
"""

print(list(itertools.zip_longest(*matriz)))

