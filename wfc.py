#!/usr/bin/python
from datetime import datetime
import random
import tkinter as tk
from PIL import Image, ImageTk

# direction idxs: 0 - UP; 1 - RIGHT; 2 - DOWN; 3 - LEFT

TILE_DEFS = []

MAP = []
MAP_WIDTH = 50
MAP_HEIGHT = 24
TILE_SIZE = 32
HALF_TILE = int(TILE_SIZE / 2)

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

def uncollapseAround(x, y):
    if y - 1 >= 0 and MAP[y - 1][x]["collapsed"]:
        uncollapseAt(x, y - 1)
    if y + 1 < MAP_HEIGHT and MAP[y + 1][x]["collapsed"]:
        uncollapseAt(x, y + 1)
    if x + 1 < MAP_WIDTH and MAP[y][x + 1]["collapsed"]:
        uncollapseAt(x + 1, y)
    if x - 1 >= 0 and MAP[y][x - 1]["collapsed"]:
        uncollapseAt(x - 1, y)
    uncollapseAt(x, y)

def uncollapseAt(x, y):
    MAP[y][x]["values"] = []
    MAP[y][x]["collapsed"] = ''

    if y - 1 >= 0 and MAP[y - 1][x]["collapsed"]:
        expectedAbove = TILE_DEFS[MAP[y - 1][x]["values"]]["neighbours"][0][::-1]
        MAP[y][x]["values"] += [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][2] == expectedAbove]
    
    if y + 1 < MAP_HEIGHT and MAP[y + 1][x]["collapsed"]:
        expectedBelow = TILE_DEFS[MAP[y + 1][x]["values"]]["neighbours"][2][::-1]
        MAP[y][x]["values"] += [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][0] == expectedBelow]
    
    if x + 1 < MAP_WIDTH and MAP[y][x + 1]["collapsed"]:
        expectedRight = TILE_DEFS[MAP[y][x + 1]["values"]]["neighbours"][1][::-1]
        MAP[y][x]["values"] += [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][3] == expectedRight]
    
    if x - 1 >= 0 and MAP[y][x - 1]["collapsed"]:
        expectedLeft = TILE_DEFS[MAP[y][x - 1]["values"]]["neighbours"][3][::-1]
        MAP[y][x]["values"] += [idx for idx, e in enumerate(TILE_DEFS) if e["neighbours"][1] == expectedLeft]

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
            uncollapseAround(x, y)
            print(f"WARNING - contradiction occurred at position ({x},{y})")
            #MAP[y][x]["values"] = -1
            #MAP[y][x]["collapsed"] = 'A'
            #break
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

def addAtlasSub(image, neighbours):
    for i in range(len(neighbours) - 1):
        checkNeighbourCorners(neighbours[i], neighbours[i + 1])
    checkNeighbourCorners(neighbours[-1], neighbours[0])
    TILE_DEFS.append({"img": ImageTk.PhotoImage(image), "neighbours": neighbours})

def addSub(imagePath, neighbours):
    image = Image.open(imagePath).resize((TILE_SIZE, TILE_SIZE), resample=0)
    TILE_DEFS.append({"img": ImageTk.PhotoImage(image), "neighbours": neighbours})

def loadNonAtlas(pathRoot):
    TILE_DEFS.clear()
    addSub(f"{pathRoot}tile_0.png", ['', '', '', ''])
    addSub(f"{pathRoot}tile_1.png", ['A', '', 'A', ''])
    addSub(f"{pathRoot}tile_2.png", ['', 'A', '', 'A'])
    addSub(f"{pathRoot}tile_3.png", ['A', 'A', '', ''])
    addSub(f"{pathRoot}tile_4.png", ['', 'A', 'A', ''])
    addSub(f"{pathRoot}tile_5.png", ['', '', 'A', 'A'])
    addSub(f"{pathRoot}tile_6.png", ['A', '', '', 'A'])
    addSub(f"{pathRoot}tile_7.png", ['A', 'A', 'A', 'A'])
    addSub(f"{pathRoot}tile_8.png", ['A', 'A', '', 'A'])
    addSub(f"{pathRoot}tile_9.png", ['A', 'A', 'A', ''])
    addSub(f"{pathRoot}tile_10.png", ['', 'A', 'A', 'A'])
    addSub(f"{pathRoot}tile_11.png", ['A', '', 'A', 'A'])

def getCropSize(x, y):
    return (x * TILE_SIZE, y * TILE_SIZE, (x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE)

def loadAtlas(atlasPath):
    TILE_DEFS.clear()
    ATLAS_TILES_X = 12
    ATLAS_TILES_Y = 4
    atlasImage = Image.open(atlasPath).resize((TILE_SIZE * ATLAS_TILES_X, TILE_SIZE * ATLAS_TILES_Y), resample=0)
    addAtlasSub(atlasImage.crop(getCropSize(0, 0)), ['', '', '_A_', ''])
    addAtlasSub(atlasImage.crop(getCropSize(0, 1)), ['_A_', '', '_A_', ''])
    addAtlasSub(atlasImage.crop(getCropSize(0, 2)), ['_A_', '', '', ''])
    addAtlasSub(atlasImage.crop(getCropSize(0, 3)), ['', '', '', ''])
    
    addAtlasSub(atlasImage.crop(getCropSize(1, 0)), ['', '_A_', '_A_', ''])
    addAtlasSub(atlasImage.crop(getCropSize(1, 1)), ['_A_', '_A_', '_A_', ''])
    addAtlasSub(atlasImage.crop(getCropSize(1, 2)), ['_A_', '_A_', '', ''])
    addAtlasSub(atlasImage.crop(getCropSize(2, 0)), ['', '_A_', '_A_', '_A_'])
    addAtlasSub(atlasImage.crop(getCropSize(2, 1)), ['_A_', '_A_', '_A_', '_A_'])
    addAtlasSub(atlasImage.crop(getCropSize(2, 2)), ['_A_', '_A_', '', '_A_'])
    addAtlasSub(atlasImage.crop(getCropSize(3, 0)), ['', '', '_A_', '_A_'])
    addAtlasSub(atlasImage.crop(getCropSize(3, 1)), ['_A_', '', '_A_', '_A_'])
    addAtlasSub(atlasImage.crop(getCropSize(3, 2)), ['_A_', '', '', '_A_'])

    addAtlasSub(atlasImage.crop(getCropSize(1, 3)), ['', '_A_', '', ''])
    addAtlasSub(atlasImage.crop(getCropSize(2, 3)), ['', '_A_', '', '_A_'])
    addAtlasSub(atlasImage.crop(getCropSize(3, 3)), ['', '', '', '_A_'])

    addAtlasSub(atlasImage.crop(getCropSize(4, 0)), ['AA_', '_A_', '_A_', '_AA'])
    addAtlasSub(atlasImage.crop(getCropSize(4, 1)), ['_A_', '_AA', 'AA_', ''])
    addAtlasSub(atlasImage.crop(getCropSize(4, 2)), ['_AA', 'AA_', '_A_', ''])
    addAtlasSub(atlasImage.crop(getCropSize(4, 3)), ['_A_', '_A_', '_AA', 'AA_'])

    addAtlasSub(atlasImage.crop(getCropSize(5, 0)), ['', '_AA', 'AA_', '_A_'])
    addAtlasSub(atlasImage.crop(getCropSize(5, 1)), ['_AA', 'AAA', 'AAA', 'AA_'])
    addAtlasSub(atlasImage.crop(getCropSize(5, 2)), ['AAA', 'AAA', 'AA_', '_AA'])
    addAtlasSub(atlasImage.crop(getCropSize(5, 3)), ['_AA', 'AA_', '', '_A_'])

    addAtlasSub(atlasImage.crop(getCropSize(6, 0)), ['', '_A_', '_AA', 'AA_'])
    addAtlasSub(atlasImage.crop(getCropSize(6, 1)), ['AA_', '_AA', 'AAA', 'AAA'])
    addAtlasSub(atlasImage.crop(getCropSize(6, 2)), ['AAA', 'AA_', '_AA', 'AAA'])
    addAtlasSub(atlasImage.crop(getCropSize(6, 3)), ['AA_', '_A_', '', '_AA'])

    addAtlasSub(atlasImage.crop(getCropSize(7, 0)), ['_AA', 'AA_', '_A_', '_A_'])
    addAtlasSub(atlasImage.crop(getCropSize(7, 1)), ['_A_', '', '_AA', 'AA_'])
    addAtlasSub(atlasImage.crop(getCropSize(7, 2)), ['AA_', '', '_A_', '_AA'])
    addAtlasSub(atlasImage.crop(getCropSize(7, 3)), ['_A_', '_AA', 'AA_', '_A_'])

    addAtlasSub(atlasImage.crop(getCropSize(8, 0)), ['', '_AA', 'AA_', ''])
    addAtlasSub(atlasImage.crop(getCropSize(8, 1)), ['_AA', 'AAA', 'AA_', ''])
    addAtlasSub(atlasImage.crop(getCropSize(8, 2)), ['_AA', 'AAA', 'AA_', '_A_'])
    addAtlasSub(atlasImage.crop(getCropSize(8, 3)), ['_AA', 'AA_', '', ''])

    addAtlasSub(atlasImage.crop(getCropSize(9, 0)), ['_A_', '_AA', 'AAA', 'AA_'])
    addAtlasSub(atlasImage.crop(getCropSize(9, 1)), ['_AA', 'AA_', '_AA', 'AA_'])
    addAtlasSub(atlasImage.crop(getCropSize(9, 2)), ['AAA', 'AAA', 'AAA', 'AAA'])
    addAtlasSub(atlasImage.crop(getCropSize(9, 3)), ['AAA', 'AA_', '', '_AA'])

    addAtlasSub(atlasImage.crop(getCropSize(10, 0)), ['', '_AA', 'AAA', 'AA_'])
    addAtlasSub(atlasImage.crop(getCropSize(10, 1)), ['', '', '', ''])
    addAtlasSub(atlasImage.crop(getCropSize(10, 2)), ['AA_', '_AA', 'AA_', '_AA'])
    addAtlasSub(atlasImage.crop(getCropSize(10, 3)), ['AAA', 'AA_', '_A_', '_AA'])

    addAtlasSub(atlasImage.crop(getCropSize(11, 0)), ['', '', '_AA', 'AA_'])
    addAtlasSub(atlasImage.crop(getCropSize(11, 1)), ['AA_', '_A_', '_AA', 'AAA'])
    addAtlasSub(atlasImage.crop(getCropSize(11, 2)), ['AA_', '', '_AA', 'AAA'])
    addAtlasSub(atlasImage.crop(getCropSize(11, 3)), ['AA_', '', '', '_AA'])

def createAtlasMetaSub(tl, tr, bl, br):
    sub = Image.new("RGB", (TILE_SIZE, TILE_SIZE))
    sub.paste(tl, (0, 0))
    sub.paste(tr, (HALF_TILE, 0))
    sub.paste(bl, (0, HALF_TILE))
    sub.paste(br, (HALF_TILE, HALF_TILE))
    return sub


def loadAtlasMeta(atlasMetaPath, inward, outward):
    #TILE_DEFS.clear()
    ATLAS_META_TILES_X = 6
    ATLAS_META_TILES_Y = 1
    atlasMetaImage = Image.open(atlasMetaPath).resize((TILE_SIZE * ATLAS_META_TILES_X, TILE_SIZE * ATLAS_META_TILES_Y), resample=0)

    tlcurve = atlasMetaImage.crop((0, 0, HALF_TILE, HALF_TILE))
    trcurve = atlasMetaImage.crop((HALF_TILE, 0, HALF_TILE * 2, HALF_TILE))
    blcurve = atlasMetaImage.crop((0, HALF_TILE, HALF_TILE, HALF_TILE * 2))
    brcurve = atlasMetaImage.crop((HALF_TILE, HALF_TILE, HALF_TILE * 2, HALF_TILE * 2))
    tlver = atlasMetaImage.crop((HALF_TILE * 2, 0, HALF_TILE * 3, HALF_TILE))
    trver = atlasMetaImage.crop((HALF_TILE * 3, 0, HALF_TILE * 4, HALF_TILE))
    blver = atlasMetaImage.crop((HALF_TILE * 2, HALF_TILE, HALF_TILE * 3, HALF_TILE * 2))
    brver = atlasMetaImage.crop((HALF_TILE * 3, HALF_TILE, HALF_TILE * 4, HALF_TILE * 2))
    tlhor = atlasMetaImage.crop((HALF_TILE * 4, 0, HALF_TILE * 5, HALF_TILE))
    trhor = atlasMetaImage.crop((HALF_TILE * 5, 0, HALF_TILE * 6, HALF_TILE))
    blhor = atlasMetaImage.crop((HALF_TILE * 4, HALF_TILE, HALF_TILE * 5, HALF_TILE * 2))
    brhor = atlasMetaImage.crop((HALF_TILE * 5, HALF_TILE, HALF_TILE * 6, HALF_TILE * 2))
    tlcor = atlasMetaImage.crop((HALF_TILE * 6, 0, HALF_TILE * 7, HALF_TILE))
    trcor = atlasMetaImage.crop((HALF_TILE * 7, 0, HALF_TILE * 8, HALF_TILE))
    blcor = atlasMetaImage.crop((HALF_TILE * 6, HALF_TILE, HALF_TILE * 7, HALF_TILE * 2))
    brcor = atlasMetaImage.crop((HALF_TILE * 7, HALF_TILE, HALF_TILE * 8, HALF_TILE * 2))
    tlemp = atlasMetaImage.crop((HALF_TILE * 8, 0, HALF_TILE * 9, HALF_TILE))
    tremp = atlasMetaImage.crop((HALF_TILE * 9, 0, HALF_TILE * 10, HALF_TILE))
    blemp = atlasMetaImage.crop((HALF_TILE * 8, HALF_TILE, HALF_TILE * 9, HALF_TILE * 2))
    bremp = atlasMetaImage.crop((HALF_TILE * 9, HALF_TILE, HALF_TILE * 10, HALF_TILE * 2))
    tlfil = atlasMetaImage.crop((HALF_TILE * 10, 0, HALF_TILE * 11, HALF_TILE))
    trfil = atlasMetaImage.crop((HALF_TILE * 11, 0, HALF_TILE * 12, HALF_TILE))
    blfil = atlasMetaImage.crop((HALF_TILE * 10, HALF_TILE, HALF_TILE * 11, HALF_TILE * 2))
    brfil = atlasMetaImage.crop((HALF_TILE * 11, HALF_TILE, HALF_TILE * 12, HALF_TILE * 2))

    addAtlasSub(createAtlasMetaSub(tlcurve, trcurve, blver, brver), [f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlver, trver, blver, brver), [f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlver, trver, blcurve, brcurve), [f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcurve, trcurve, blcurve, brcurve), [f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcurve, trhor, blver, brcor), [f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlver, trcor, blver, brcor), [f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlver, trcor, blcurve, brhor), [f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlhor, trhor, blcor, brcor), [f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, trcor, blcor, brcor), [f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, trcor, blhor, brhor), [f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlhor, trcurve, blcor, brver), [f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, trver, blcor, brver), [f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, trver, blhor, brcurve), [f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcurve, trhor, blcurve, brhor), [f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlhor, trhor, blhor, brhor), [f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlhor, trcurve, blhor, brcurve), [f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, trcor, blcor, brcor), [f'{inward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{inward}'])
    addAtlasSub(createAtlasMetaSub(tlver, trcor, blver, bremp), [f'{outward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlver, tremp, blver, brcor), [f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, trcor, blemp, brcor), [f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlhor, trhor, blcor, bremp), [f'{outward}{outward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, tremp, blemp, bremp), [f'{outward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, tremp, blcor, bremp), [f'{inward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{inward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, tremp, blhor, brhor), [f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlhor, trhor, blemp, brcor), [f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, trcor, blemp, bremp), [f'{inward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{inward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, tremp, blemp, brcor), [f'{inward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{inward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, trcor, blhor, brhor), [f'{inward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{inward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, tremp, blcor, brcor), [f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, trver, blemp, brver), [f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, trver, blcor, brver), [f'{inward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{inward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, trcor, blcor, bremp), [f'{outward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcurve, trhor, blver, bremp), [f'{outward}{outward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlver, tremp, blver, bremp), [f'{outward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, tremp, blcor, bremp), [f'{outward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlver, tremp, blcurve, brhor), [f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, trcor, blemp, bremp), [f'{outward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlcor, tremp, blemp, brcor), [f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, tremp, blemp, bremp), [f'{inward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{inward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, tremp, blhor, brhor), [f'{inward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{inward}'])
    addAtlasSub(createAtlasMetaSub(tlhor, trhor, blemp, bremp), [f'{outward}{outward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlfil, trfil, blfil, brfil), [f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, trcor, blcor, bremp), [f'{inward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{inward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, tremp, blcor, brcor), [f'{inward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{inward}'])
    addAtlasSub(createAtlasMetaSub(tlhor, trcurve, blemp, brver), [f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, trcor, blemp, brcor), [f'{inward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{inward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, trver, blemp, brver), [f'{inward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{inward}'])
    addAtlasSub(createAtlasMetaSub(tlemp, trver, blhor, brcurve), [f'{inward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{inward}'])

def main():
    window = buildWindow()
    #loadNonAtlas("img/ts/")
    #loadAtlas("img/atlas/ts_dirt.png")
    loadAtlasMeta("img/atlasmeta/ts_beach.png", "W", "B")
    #loadAtlasMeta("img/atlasmeta/ts_field.png", "B", "F")
    #loadAtlasMeta("img/atlasmeta/ts_snow.png", "S", "F")
    window.mainloop()

if __name__ == '__main__':
    main()