import json
from stl import mesh

# Load the STL file
stl_file = 'objects/plane.stl'
your_mesh = mesh.Mesh.from_file(stl_file)

# Initialize lists for points and lines
points = []
lines = []

# Iterate over the vectors (triangles) in the mesh
for i in range(len(your_mesh.vectors)):
    vertexes = your_mesh.vectors[i].tolist()
    # Add the vertices (points) to the list
    for vertex in vertexes:
        points.append(vertex)
    
    # Add the edges (lines) to the list
    lines.append([i*3, i*3+1])
    lines.append([i*3+1, i*3+2])
    lines.append([i*3+2, i*3+0])

# Now you have a list of points and lines
objectDict = {"scale": 100.0,
              "points_xyz": points,
              "connections": lines}
with open("objects/stl.json", "w") as f:
    json.dump(objectDict, f)

if __name__ == "__main__":
    exit()
