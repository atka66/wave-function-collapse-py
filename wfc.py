#!/usr/bin/python

from datetime import datetime
import random
import tkinter as tk
from importer import *

# direction idxs: 0 - UP; 1 - RIGHT; 2 - DOWN; 3 - LEFT

TILE_DEFS = []

MAP = []
MAP_WIDTH = 30
MAP_HEIGHT = 20
TILE_SIZE = 32

def resetMap():
    now = datetime.now()
    MAP.clear()
    for _ in range(MAP_HEIGHT):
        mapRow = []
        for _ in range(MAP_WIDTH):
            mapRow.append({"collapsed": '', "values": [i for i in range(len(TILE_DEFS))]})
        MAP.append(mapRow)
    
    collapseAt(random.randrange(MAP_WIDTH), random.randrange(MAP_HEIGHT), random.randrange(len(TILE_DEFS)))

    elapsedTime = datetime.now() - now
    #print(f"map has been reset - {elapsedTime}")
    return elapsedTime

def collapseAt(x, y, value):
    MAP[y][x]["values"] = [value]
    MAP[y][x]["collapsed"] = 'A'

    expectedAbove = TILE_DEFS[value]["neighbours"][0][::-1]
    if y - 1 >= 0 and not MAP[y - 1][x]["collapsed"]:
        forbiddenAboveTiles = [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][2] != expectedAbove]
        MAP[y - 1][x]["values"] = [e for e in MAP[y - 1][x]["values"] if e not in forbiddenAboveTiles]

    expectedBelow = TILE_DEFS[value]["neighbours"][2][::-1]
    if y + 1 < MAP_HEIGHT and not MAP[y + 1][x]["collapsed"]:
        forbiddenBelowTiles = [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][0] != expectedBelow]
        MAP[y + 1][x]["values"] = [e for e in MAP[y + 1][x]["values"] if e not in forbiddenBelowTiles]
    
    expectedRight = TILE_DEFS[value]["neighbours"][1][::-1]
    if x + 1 < MAP_WIDTH and not MAP[y][x + 1]["collapsed"]:
        forbiddenRightTiles = [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][3] != expectedRight]
        MAP[y][x + 1]["values"] = [e for e in MAP[y][x + 1]["values"] if e not in forbiddenRightTiles]
    
    expectedLeft = TILE_DEFS[value]["neighbours"][3][::-1]
    if x - 1 >= 0 and not MAP[y][x - 1]["collapsed"]:
        forbiddenLeftTiles = [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][1] != expectedLeft]
        MAP[y][x - 1]["values"] = [e for e in MAP[y][x - 1]["values"] if e not in forbiddenLeftTiles]

def findLeastValuesPos():
    leastValuesN = len(TILE_DEFS) + 1
    withSameValues = []
    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            cell = MAP[i][j]
            if not cell["collapsed"]:
                valuesN = len(cell["values"])
                if valuesN == leastValuesN:
                    withSameValues.append([j, i])
                elif valuesN < leastValuesN:
                    leastValuesN = valuesN
                    withSameValues = [[j, i]]
    
    if len(withSameValues) < 1:
        return []
    
    return random.choice(withSameValues)

def isMapCollapsed():
    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            if MAP[i][j]["collapsed"] == '':
                return ''
    return 'A'

def collapseMap(root, canvas, showInbetween):
    now = datetime.now()

    while(not isMapCollapsed()):
        pos = findLeastValuesPos()
        if len(pos) < 2:
            print("WARNING - somehow could not find candidate for collapsing")
            break
        x = pos[0]
        y = pos[1]
        values = MAP[y][x]["values"]
        if not values:
            #print(f"WARNING - contradiction occurred at position ({x},{y})")
            #MAP[y][x]["values"] = [-1]
            #MAP[y][x]["collapsed"] = 'A'
            resetMap()
        else:
            collapseAt(x, y, random.choice(values))

            if showInbetween:
                updateCanvasTile(canvas, y, x)
                root.update()
    
    elapsedTime = datetime.now() - now
    print(f"map has collapsed - {elapsedTime}")
    return elapsedTime

def benchmarkMap(root, canvas, showInbetween, showIndividual, benchmarkRuns):
    if not benchmarkRuns.isdigit():
        print("ERROR - must provide benchmark runs as integer")
        return
    
    print(f"benchmarking map collapsing ({benchmarkRuns} times)")
    now = datetime.now()
    totalRuntime = datetime.now()
    for i in range(int(benchmarkRuns)):
        totalRuntime += resetMap()
        if showInbetween:
            updateCanvas(root, canvas)
        totalRuntime += collapseMap(root, canvas, showInbetween)
        if showIndividual:
            updateCanvas(root, canvas)
    print(f"benchmarking finished - {totalRuntime - now}")

def benchmarkButtonAction(root, canvas, showInbetween, showIndividual, benchmarkRuns):
    benchmarkMap(root, canvas, showInbetween, showIndividual, benchmarkRuns)
    updateCanvas(root, canvas)

def collapseButtonAction(root, canvas, showInbetween):
    updateCanvas(root, canvas)
    resetMap()
    updateCanvas(root, canvas)
    collapseMap(root, canvas, showInbetween)
    updateCanvas(root, canvas)

def buildInterface(frame, root, canvas):
    showInbetweenVar = tk.IntVar(value=1)
    showInbetweenCb = tk.Checkbutton(frame, text="Show inbetween", variable=showInbetweenVar)
    showInbetweenCb.pack()
    collapseButton = tk.Button(frame, text="Collapse", width=20, command=lambda: collapseButtonAction(root, canvas, showInbetweenVar.get()))
    collapseButton.pack()
    benchmarkRunsVar = tk.StringVar(value="5")
    benchmarkRunsEntry = tk.Entry(frame, textvariable=benchmarkRunsVar)
    benchmarkRunsEntry.pack()
    showIndividualVar = tk.IntVar(value=1)
    showIndividualCb = tk.Checkbutton(frame, text="Show individual", variable=showIndividualVar)
    showIndividualCb.pack()
    benchmarkButton = tk.Button(frame, text=f"Benchmark", width=20, command=lambda: benchmarkButtonAction(root, canvas, showInbetweenVar.get(), showIndividualVar.get(), benchmarkRunsVar.get()))
    benchmarkButton.pack()

def updateCanvasTile(canvas, i, j):
    value = MAP[i][j]["values"][0]
    if value < 0:
        canvas.create_rectangle(j * TILE_SIZE, i * TILE_SIZE, (j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE, fill="red")
    else:
        image = TILE_DEFS[value]["img"]
        canvas.create_image(j * TILE_SIZE, i * TILE_SIZE, image=image, anchor=tk.NW)

def updateCanvas(root, canvas):
    canvas.delete("all")
    if MAP:
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                if MAP[i][j]["collapsed"]:
                    updateCanvasTile(canvas, i, j)
            
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
    buildInterface(frame, root, canvas)
    return root

def main():
    window = buildWindow()
    #TILE_DEFS.extend(loadNonAtlas("img/ts/", TILE_SIZE))
    #TILE_DEFS.extend(loadAtlas("img/atlas/ts_dirt.png", TILE_SIZE))
    TILE_DEFS.extend(loadAtlasMeta("img/atlasmeta/ts_beach.png", TILE_SIZE, "W", "B"))
    #TILE_DEFS.extend(loadAtlasMeta("img/atlasmeta/ts_field.png", TILE_SIZE, "B", "F"))
    #TILE_DEFS.extend(loadAtlasMeta("img/atlasmeta/ts_snow.png", TILE_SIZE, "S", "F"))
    window.mainloop()

if __name__ == '__main__':
    main()