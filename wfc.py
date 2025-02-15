#!/usr/bin/python
import random
import tkinter as tk

# directions: 0 - UP; 1 - RIGHT; 2 - DOWN; 3 - LEFT

TILE_DEFS = [
    {"src": "img/tile_0.png", "neighbors": []},
    {"src": "img/tile_1.png", "neighbors": [0, 2]},
    {"src": "img/tile_2.png", "neighbors": [1, 3]},
    {"src": "img/tile_3.png", "neighbors": [0, 1]},
    {"src": "img/tile_4.png", "neighbors": [1, 2]},
    {"src": "img/tile_5.png", "neighbors": [2, 3]},
    {"src": "img/tile_6.png", "neighbors": [0, 3]},
    {"src": "img/tile_7.png", "neighbors": [0, 1, 2, 3]},
]

MAP = []
MAP_WIDTH = 20
MAP_HEIGHT = 20
TILE_SIZE = 16

def resetMap(root, canvas):
    MAP.clear()
    for _ in range(MAP_HEIGHT):
        mapRow = []
        for _ in range(MAP_WIDTH):
            mapRow.append({"collapsed": False, "values": [i for i in range(len(TILE_DEFS))]})
        MAP.append(mapRow)
    print("map has been reset")
    updateCanvas(root, canvas)

def adjustNeighbour(x, y):
    # above neighbour
    pass

def collapseAt(x, y, value):
    MAP[y][x]["values"] = value
    MAP[y][x]["collapsed"] = True
    if y - 1 >= 0:
        adjustNeighbour(x, y - 1)

def findLeastValuesPos():
    posX = -1
    posY = -1
    leastValuesN = len(TILE_DEFS) + 1
    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            cell = MAP[i][j]
            if not cell["collapsed"]:
                valuesN = len(cell["values"])
                if valuesN < leastValuesN:
                    posX = j
                    posY = i
                    leastValuesN = valuesN
    
    if posX < 0 or posY < 0:
        return []
    
    return [posX, posY]

def isMapCollapsed():
    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            if MAP[i][j]["collapsed"] == False:
                return False
    return True

def collapseMap(root, canvas):
    print("map collapsing started")

    while(not isMapCollapsed()):
        pos = findLeastValuesPos()
        if len(pos) < 2:
            print("WARNING - somehow could not find candidate for collapsing")
            break
        x = pos[0]
        y = pos[1]
        collapseAt(x, y, random.choice(MAP[y][x]["values"]))

    print("map has collapsed")
    updateCanvas(root, canvas)

def buildButtons(frame, root, canvas):
    resetButton = tk.Button(frame, text="Reset", width=10, command=lambda: resetMap(root, canvas))
    resetButton.pack()
    collapseButton = tk.Button(frame, text="Collapse", width=10, command=lambda: collapseMap(root, canvas))
    collapseButton.pack()

def updateCanvas(root, canvas):
    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            if not MAP[i][j]["collapsed"]:
                canvas.create_rectangle(j * TILE_SIZE, i * TILE_SIZE, ((j + 1) * TILE_SIZE) - 1, ((i + 1) * TILE_SIZE) - 1, fill="gray", outline="white")
            else:
                image = TILE_DEFS[MAP[i][j]["values"]]["img"]
                canvas.create_image(j * TILE_SIZE, i * TILE_SIZE, image=image, anchor=tk.NW)
            
    root.update()

def buildCanvas(frame):
    canvas = tk.Canvas(frame, height=MAP_WIDTH * TILE_SIZE, width=MAP_HEIGHT * TILE_SIZE)
    canvas.pack()
    return canvas

def buildWindow():
    root = tk.Tk()
    frame = tk.Frame(root, relief="flat", borderwidth=10)
    frame.pack()
    canvas = buildCanvas(frame)
    buildButtons(frame, root, canvas)
    return root

def loadImages():
    for i in range(len(TILE_DEFS)):
        TILE_DEFS[i]["img"] = tk.PhotoImage(file=TILE_DEFS[i]["src"])

def main():
    window = buildWindow()
    loadImages()
    window.mainloop()

if __name__ == '__main__':
    main()