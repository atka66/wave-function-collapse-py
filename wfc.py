#!/usr/bin/python

from datetime import datetime
import random
import tkinter as tk
from importer import *

# direction idxs: 0 - UP; 1 - RIGHT; 2 - DOWN; 3 - LEFT

TILE_DEFS = []

MAP = []
MAP_WIDTH = 100
MAP_HEIGHT = 50
TILE_SIZE = 16

def resetMap(border=True):
    now = datetime.now()
    MAP.clear()
    for _ in range(MAP_HEIGHT):
        mapRow = []
        for _ in range(MAP_WIDTH):
            mapRow.append({"collapsed": False, "values": [i for i in range(len(TILE_DEFS))]})
        MAP.append(mapRow)
    
    if border:
        for i in range(MAP_HEIGHT):
            collapseAt(0, i, 0)
            collapseAt(MAP_WIDTH - 1, i, 0)
        for i in range(MAP_WIDTH):
            collapseAt(i, 0, 0)
            collapseAt(i, MAP_HEIGHT - 1, 0)
    else:
        collapseAt(random.randrange(MAP_WIDTH), random.randrange(MAP_HEIGHT), random.randrange(len(TILE_DEFS)))

    elapsedTime = datetime.now() - now
    #print(f"map has been reset - {elapsedTime}")
    return elapsedTime

def removeForbidden(x, y, tileNeighbour, neighbourId):
    if 0 <= y and y < MAP_HEIGHT and 0 <= x and x < MAP_WIDTH and not MAP[y][x]["collapsed"]:
        expectedPattern = tileNeighbour[::-1]
        forbiddenTiles = [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][neighbourId] != expectedPattern]
        MAP[y][x]["values"] = [e for e in MAP[y][x]["values"] if e not in forbiddenTiles]

def collapseAt(x, y, value):
    MAP[y][x]["values"] = [value]
    MAP[y][x]["collapsed"] = True

    tileNeighbours = TILE_DEFS[value]["neighbours"]

    removeForbidden(x, y - 1, tileNeighbours[0], 2)
    removeForbidden(x, y + 1, tileNeighbours[2], 0)
    removeForbidden(x + 1, y, tileNeighbours[1], 3)
    removeForbidden(x - 1, y, tileNeighbours[3], 1)

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
            if not MAP[i][j]["collapsed"]:
                return ''
    return 'A'

def collapseMap(root, canvas, showInbetween, border):
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
            print(f"WARNING - contradiction occurred at position ({x},{y})")
            resetMap(border)
        else:
            collapseAt(x, y, random.choice(values))

            if showInbetween:
                updateCanvasTile(canvas, y, x)
                root.update()
    
    elapsedTime = datetime.now() - now
    print(f"map has collapsed - {elapsedTime}")
    return elapsedTime

def benchmarkMap(root, canvas, showInbetween, border, showIndividual, benchmarkRuns):
    if not benchmarkRuns.isdigit():
        print("ERROR - must provide benchmark runs as integer")
        return
    
    print(f"benchmarking map collapsing ({benchmarkRuns} times)")
    now = datetime.now()
    totalRuntime = datetime.now()
    for i in range(int(benchmarkRuns)):
        totalRuntime += resetMap(border)
        if showInbetween:
            updateCanvas(root, canvas)
        totalRuntime += collapseMap(root, canvas, showInbetween, border)
        if showIndividual:
            updateCanvas(root, canvas)
    print(f"benchmarking finished - {totalRuntime - now}")

def benchmarkButtonAction(root, canvas, showInbetween, border, showIndividual, benchmarkRuns):
    benchmarkMap(root, canvas, showInbetween, border, showIndividual, benchmarkRuns)
    updateCanvas(root, canvas)

def collapseButtonAction(root, canvas, showInbetween, border):
    updateCanvas(root, canvas)
    resetMap(border)
    updateCanvas(root, canvas)
    collapseMap(root, canvas, showInbetween, border)
    updateCanvas(root, canvas)

def buildInterface(frame, root, canvas):
    showInbetweenVar = tk.IntVar(value=1)
    showInbetweenCb = tk.Checkbutton(frame, text="Show inbetween", variable=showInbetweenVar)
    showInbetweenCb.pack()
    borderVar = tk.IntVar(value=1)
    borderCb = tk.Checkbutton(frame, text="Border", variable=borderVar)
    borderCb.pack()
    collapseButton = tk.Button(frame, text="Collapse", width=20, command=lambda: collapseButtonAction(root, canvas, showInbetweenVar.get(), borderVar.get()))
    collapseButton.pack()
    benchmarkRunsVar = tk.StringVar(value="1")
    benchmarkRunsEntry = tk.Entry(frame, textvariable=benchmarkRunsVar)
    benchmarkRunsEntry.pack()
    showIndividualVar = tk.IntVar(value=1)
    showIndividualCb = tk.Checkbutton(frame, text="Show individual", variable=showIndividualVar)
    showIndividualCb.pack()
    benchmarkButton = tk.Button(frame, text=f"Benchmark", width=20, command=lambda: benchmarkButtonAction(root, canvas, showInbetweenVar.get(), borderVar.get(), showIndividualVar.get(), benchmarkRunsVar.get()))
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
    #TILE_DEFS.extend(loadAtlasMeta("img/atlasmeta/ts_beach.png", TILE_SIZE, "W", "B"))
    #TILE_DEFS.extend(loadAtlasMeta("img/atlasmeta/ts_field.png", TILE_SIZE, "B", "F"))
    #TILE_DEFS.extend(loadAtlasMeta("img/atlasmeta/ts_snow.png", TILE_SIZE, "S", "F"))
    TILE_DEFS.extend(loadAtlasDungeon("img/atlasdungeon/ad_1.png", TILE_SIZE))
    window.mainloop()

if __name__ == '__main__':
    main()