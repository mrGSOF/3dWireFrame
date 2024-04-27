def createNet(N, M, dN, dM) -> dict:
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

    jsonObject = {"scale":100.0,
                  "points_xyz": points,
                  "connections": lines}
    return(jsonObject)

if __name__ == "__main__":
    import json
    with open("objects/net.json", "w") as f:
        json.dump(createNet(5,5,1,1), f)