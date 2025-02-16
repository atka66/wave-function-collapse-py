#!/usr/bin/python
from datetime import datetime
import random
import tkinter as tk
from PIL import Image, ImageTk

# direction idxs: 0 - UP; 1 - RIGHT; 2 - DOWN; 3 - LEFT

ATLAS_PATH = "img/atlas_ts1/ts_dirt.png"

TILE_DEFS = []

MAP = []
MAP_WIDTH = 20
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
    MAP[y][x]["values"] = value
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
    pos = [-1, -1]
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
            print(f"WARNING - contradiction occurred at position ({x},{y})")
            MAP[y][x]["values"] = -1
            MAP[y][x]["collapsed"] = 'A'
            break
        collapseAt(x, y, random.choice(MAP[y][x]["values"]))
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
    value = MAP[i][j]["values"]
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

def checkNeighbourCorners(a, b):
    if a == '':
        a = '___'
    if b == '':
        b = '___'
    if a[-1] != b[0]:
        print(f"WARNING - neighbours have mismatching corners: ([{a}]-[{b}])")

def addAtlasSub(atlasImage, x, y, neighbours):
    for i in range(len(neighbours) - 1):
        checkNeighbourCorners(neighbours[i], neighbours[i + 1])
    checkNeighbourCorners(neighbours[-1], neighbours[0])
    TILE_DEFS.append({"img": ImageTk.PhotoImage(atlasImage.crop((x * TILE_SIZE, y * TILE_SIZE, (x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE))), "neighbours": neighbours})

def addSub(imagePath, neighbours):
    image = Image.open(imagePath).resize((TILE_SIZE, TILE_SIZE), resample=0)
    TILE_DEFS.append({"img": ImageTk.PhotoImage(image), "neighbours": neighbours})

def loadNonAtlas():
    TILE_DEFS.clear()
    addSub("img/ts1/tile_0.png", ['', '', '', ''])
    addSub("img/ts1/tile_1.png", ['A', '', 'A', ''])
    addSub("img/ts1/tile_2.png", ['', 'A', '', 'A'])
    addSub("img/ts1/tile_3.png", ['A', 'A', '', ''])
    addSub("img/ts1/tile_4.png", ['', 'A', 'A', ''])
    addSub("img/ts1/tile_5.png", ['', '', 'A', 'A'])
    addSub("img/ts1/tile_6.png", ['A', '', '', 'A'])
    addSub("img/ts1/tile_7.png", ['A', 'A', 'A', 'A'])
    addSub("img/ts1/tile_8.png", ['A', 'A', '', 'A'])
    addSub("img/ts1/tile_9.png", ['A', 'A', 'A', ''])
    addSub("img/ts1/tile_10.png", ['', 'A', 'A', 'A'])
    addSub("img/ts1/tile_11.png", ['A', '', 'A', 'A'])

def loadAtlas():
    ATLAS_TILES_X = 12
    ATLAS_TILES_Y = 4
    atlasImage = Image.open(ATLAS_PATH).resize((TILE_SIZE * ATLAS_TILES_X, TILE_SIZE * ATLAS_TILES_Y), resample=0)
    TILE_DEFS.clear()
    addAtlasSub(atlasImage, 0, 0, ['', '', '_A_', ''])
    addAtlasSub(atlasImage, 0, 1, ['_A_', '', '_A_', ''])
    addAtlasSub(atlasImage, 0, 2, ['_A_', '', '', ''])
    addAtlasSub(atlasImage, 0, 3, ['', '', '', ''])
    
    addAtlasSub(atlasImage, 1, 0, ['', '_A_', '_A_', ''])
    addAtlasSub(atlasImage, 1, 1, ['_A_', '_A_', '_A_', ''])
    addAtlasSub(atlasImage, 1, 2, ['_A_', '_A_', '', ''])
    addAtlasSub(atlasImage, 2, 0, ['', '_A_', '_A_', '_A_'])
    addAtlasSub(atlasImage, 2, 1, ['_A_', '_A_', '_A_', '_A_'])
    addAtlasSub(atlasImage, 2, 2, ['_A_', '_A_', '', '_A_'])
    addAtlasSub(atlasImage, 3, 0, ['', '', '_A_', '_A_'])
    addAtlasSub(atlasImage, 3, 1, ['_A_', '', '_A_', '_A_'])
    addAtlasSub(atlasImage, 3, 2, ['_A_', '', '', '_A_'])

    addAtlasSub(atlasImage, 1, 3, ['', '_A_', '', ''])
    addAtlasSub(atlasImage, 2, 3, ['', '_A_', '', '_A_'])
    addAtlasSub(atlasImage, 3, 3, ['', '', '', '_A_'])

    addAtlasSub(atlasImage, 4, 0, ['AA_', '_A_', '_A_', '_AA'])
    addAtlasSub(atlasImage, 4, 1, ['_A_', '_AA', 'AA_', ''])
    addAtlasSub(atlasImage, 4, 2, ['_AA', 'AA_', '_A_', ''])
    addAtlasSub(atlasImage, 4, 3, ['_A_', '_A_', '_AA', 'AA_'])

    addAtlasSub(atlasImage, 5, 0, ['', '_AA', 'AA_', '_A_'])
    addAtlasSub(atlasImage, 5, 1, ['_AA', 'AAA', 'AAA', 'AA_'])
    addAtlasSub(atlasImage, 5, 2, ['AAA', 'AAA', 'AA_', '_AA'])
    addAtlasSub(atlasImage, 5, 3, ['_AA', 'AA_', '', '_A_'])

    addAtlasSub(atlasImage, 6, 0, ['', '_A_', '_AA', 'AA_'])
    addAtlasSub(atlasImage, 6, 1, ['AA_', '_AA', 'AAA', 'AAA'])
    addAtlasSub(atlasImage, 6, 2, ['AAA', 'AA_', '_AA', 'AAA'])
    addAtlasSub(atlasImage, 6, 3, ['AA_', '_A_', '', '_AA'])

    addAtlasSub(atlasImage, 7, 0, ['_AA', 'AA_', '_A_', '_A_'])
    addAtlasSub(atlasImage, 7, 1, ['_A_', '', '_AA', 'AA_'])
    addAtlasSub(atlasImage, 7, 2, ['AA_', '', '_A_', '_AA'])
    addAtlasSub(atlasImage, 7, 3, ['_A_', '_AA', 'AA_', '_A_'])

    addAtlasSub(atlasImage, 8, 0, ['', '_AA', 'AA_', ''])
    addAtlasSub(atlasImage, 8, 1, ['_AA', 'AAA', 'AA_', ''])
    addAtlasSub(atlasImage, 8, 2, ['_AA', 'AAA', 'AA_', '_A_'])
    addAtlasSub(atlasImage, 8, 3, ['_AA', 'AA_', '', ''])

    addAtlasSub(atlasImage, 9, 0, ['_A_', '_AA', 'AAA', 'AA_'])
    addAtlasSub(atlasImage, 9, 1, ['_AA', 'AA_', '_AA', 'AA_'])
    addAtlasSub(atlasImage, 9, 2, ['AAA', 'AAA', 'AAA', 'AAA'])
    addAtlasSub(atlasImage, 9, 3, ['AAA', 'AA_', '', '_AA'])

    addAtlasSub(atlasImage, 10, 0, ['', '_AA', 'AAA', 'AA_'])
    addAtlasSub(atlasImage, 10, 1, ['', '', '', ''])
    addAtlasSub(atlasImage, 10, 2, ['AA_', '_AA', 'AA_', '_AA'])
    addAtlasSub(atlasImage, 10, 3, ['AAA', 'AA_', '_A_', '_AA'])

    addAtlasSub(atlasImage, 11, 0, ['', '', '_AA', 'AA_'])
    addAtlasSub(atlasImage, 11, 1, ['AA_', '_A_', '_AA', 'AAA'])
    addAtlasSub(atlasImage, 11, 2, ['AA_', '', '_AA', 'AAA'])
    addAtlasSub(atlasImage, 11, 3, ['AA_', '', '', '_AA'])

def main():
    window = buildWindow()
    #loadNonAtlas()
    loadAtlas()
    window.mainloop()

if __name__ == '__main__':
    main()