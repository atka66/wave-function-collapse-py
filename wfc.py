#!/usr/bin/python
import random
import tkinter as tk

# direction idxs: 0 - UP; 1 - RIGHT; 2 - DOWN; 3 - LEFT

TILE_DEFS = [
    {"src": "img/tile_0.png", "neighbours": [False, False, False, False]},
    {"src": "img/tile_1.png", "neighbours": [True, False, True, False]},
    {"src": "img/tile_2.png", "neighbours": [False, True, False, True]},
    {"src": "img/tile_3.png", "neighbours": [True, True, False, False]},
    {"src": "img/tile_4.png", "neighbours": [False, True, True, False]},
    {"src": "img/tile_5.png", "neighbours": [False, False, True, True]},
    {"src": "img/tile_6.png", "neighbours": [True, False, False, True]},
    {"src": "img/tile_7.png", "neighbours": [True, True, True, True]},
]

MAP = []
MAP_WIDTH = 40
MAP_HEIGHT = 40
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

def collapseAt(x, y, value):
    MAP[y][x]["values"] = value
    MAP[y][x]["collapsed"] = True

    expectedAbove = TILE_DEFS[value]["neighbours"][0]
    if y - 1 >= 0 and not MAP[y - 1][x]["collapsed"]:
        forbiddenAboveTiles = [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][2] != expectedAbove]
        MAP[y - 1][x]["values"] = [e for e in MAP[y - 1][x]["values"] if e not in forbiddenAboveTiles]

    expectedBelow = TILE_DEFS[value]["neighbours"][2]
    if y + 1 < MAP_HEIGHT and not MAP[y + 1][x]["collapsed"]:
        forbiddenBelowTiles = [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][0] != expectedBelow]
        MAP[y + 1][x]["values"] = [e for e in MAP[y + 1][x]["values"] if e not in forbiddenBelowTiles]
    
    expectedRight = TILE_DEFS[value]["neighbours"][1]
    if x + 1 < MAP_WIDTH and not MAP[y][x + 1]["collapsed"]:
        forbiddenRightTiles = [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][3] != expectedRight]
        MAP[y][x + 1]["values"] = [e for e in MAP[y][x + 1]["values"] if e not in forbiddenRightTiles]
    
    expectedLeft = TILE_DEFS[value]["neighbours"][3]
    if x - 1 >= MAP_WIDTH and not MAP[y][x - 1]["collapsed"]:
        forbiddenLeftTiles = [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][1] != expectedLeft]
        MAP[y][x - 1]["values"] = [e for e in MAP[y][x - 1]["values"] if e not in forbiddenLeftTiles]

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
    canvas = tk.Canvas(frame, height=MAP_HEIGHT * TILE_SIZE, width=MAP_WIDTH * TILE_SIZE)
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