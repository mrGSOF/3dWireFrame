import math
from Lib3D import Lib3D as L

def net(N=1000, M=1000, dN=100, dM=100) -> dict:
    points = []
    lines = []
    for x in range(N):
        points.append([0, x*dN, 0])
        points.append([M*dM, x*dN, 0])
        
        lines.append([(x*2), (x*2)+1])

    for y in range(M):
        points.append([y*dN, 0, 0])
        points.append([y*dM, N*dN, 0])

        lines.append([N*2+(y*2), N*2+(y*2)+1])

    jsonObject = L.dataToDict(points, lines)
    return(jsonObject)

def sphere(radius, resolution=10):
    points = []
    lines = []

    # Create points
    for i in range(resolution):
        theta = i * math.pi / (resolution - 1)
        for j in range(resolution * 2):
            phi = j * 2 * math.pi / (resolution * 2)
            x = radius * math.sin(theta) * math.cos(phi)
            y = radius * math.sin(theta) * math.sin(phi)
            z = radius * math.cos(theta)
            points.append((x, y, z))

    # Create lines
    for i in range(resolution - 1):
        for j in range(resolution * 2):
            p1 = i * resolution * 2 + j
            p2 = i * resolution * 2 + (j + 1) % (resolution * 2)
            p3 = ((i + 1) * resolution * 2 + j) % (len(points))
            p4 = ((i + 1) * resolution * 2 + (j + 1) % (resolution * 2)) % (len(points))
            lines.extend([(p1, p2), (p1, p3), (p2, p4)])

    # Connect the last row
    for j in range(resolution * 2):
        p1 = (resolution - 1) * resolution * 2 + j
        p2 = (resolution - 1) * resolution * 2 + (j + 1) % (resolution * 2)
        lines.append((p1, p2))

    return(L.dataToDict(points, lines))

if __name__ == "__main__":
    print(len(sphere(1000, 25)))
