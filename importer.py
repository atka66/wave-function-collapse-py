#!/usr/bin/python
from PIL import Image, ImageTk

def checkNeighbourCorners(a, b):
    if a == '':
        a = '___'
    if b == '':
        b = '___'
    if a[-1] != b[0]:
        print(f"WARNING - neighbours have mismatching corners: ([{a}]-[{b}])")

def addAtlasSub(image, neighbours):
    #for i in range(len(neighbours) - 1):
    #    checkNeighbourCorners(neighbours[i], neighbours[i + 1])
    #checkNeighbourCorners(neighbours[-1], neighbours[0])
    return {"img": ImageTk.PhotoImage(image), "neighbours": neighbours}

def addSub(imagePath, tileSize, neighbours):
    image = Image.open(imagePath).resize((tileSize, tileSize), resample=0)
    return {"img": ImageTk.PhotoImage(image), "neighbours": neighbours}

def loadNonAtlas(pathRoot, tileSize):
    tileDefs = []
    tileDefs.append(addSub(f"{pathRoot}tile_0.png", tileSize, ['', '', '', '']))
    tileDefs.append(addSub(f"{pathRoot}tile_1.png", tileSize, ['A', '', 'A', '']))
    tileDefs.append(addSub(f"{pathRoot}tile_2.png", tileSize, ['', 'A', '', 'A']))
    tileDefs.append(addSub(f"{pathRoot}tile_3.png", tileSize, ['A', 'A', '', '']))
    tileDefs.append(addSub(f"{pathRoot}tile_4.png", tileSize, ['', 'A', 'A', '']))
    tileDefs.append(addSub(f"{pathRoot}tile_5.png", tileSize, ['', '', 'A', 'A']))
    tileDefs.append(addSub(f"{pathRoot}tile_6.png", tileSize, ['A', '', '', 'A']))
    tileDefs.append(addSub(f"{pathRoot}tile_7.png", tileSize, ['A', 'A', 'A', 'A']))
    tileDefs.append(addSub(f"{pathRoot}tile_8.png", tileSize, ['A', 'A', '', 'A']))
    tileDefs.append(addSub(f"{pathRoot}tile_9.png", tileSize, ['A', 'A', 'A', '']))
    tileDefs.append(addSub(f"{pathRoot}tile_10.png", tileSize, ['', 'A', 'A', 'A']))
    tileDefs.append(addSub(f"{pathRoot}tile_11.png", tileSize, ['A', '', 'A', 'A']))
    return tileDefs

def getCropSize(x, y, tileSize):
    return (x * tileSize, y * tileSize, (x + 1) * tileSize, (y + 1) * tileSize)

def loadAtlas(atlasPath, tileSize):
    tileDefs = []

    ATLAS_TILES_X = 12
    ATLAS_TILES_Y = 4
    atlasImage = Image.open(atlasPath).resize((tileSize * ATLAS_TILES_X, tileSize * ATLAS_TILES_Y), resample=0)
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(0, 0, tileSize)), ['', '', '_A_', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(0, 1, tileSize)), ['_A_', '', '_A_', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(0, 2, tileSize)), ['_A_', '', '', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(0, 3, tileSize)), ['', '', '', '']))

    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(1, 0, tileSize)), ['', '_A_', '_A_', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(1, 1, tileSize)), ['_A_', '_A_', '_A_', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(1, 2, tileSize)), ['_A_', '_A_', '', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(2, 0, tileSize)), ['', '_A_', '_A_', '_A_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(2, 1, tileSize)), ['_A_', '_A_', '_A_', '_A_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(2, 2, tileSize)), ['_A_', '_A_', '', '_A_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(3, 0, tileSize)), ['', '', '_A_', '_A_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(3, 1, tileSize)), ['_A_', '', '_A_', '_A_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(3, 2, tileSize)), ['_A_', '', '', '_A_']))

    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(1, 3, tileSize)), ['', '_A_', '', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(2, 3, tileSize)), ['', '_A_', '', '_A_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(3, 3, tileSize)), ['', '', '', '_A_']))

    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(4, 0, tileSize)), ['AA_', '_A_', '_A_', '_AA']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(4, 1, tileSize)), ['_A_', '_AA', 'AA_', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(4, 2, tileSize)), ['_AA', 'AA_', '_A_', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(4, 3, tileSize)), ['_A_', '_A_', '_AA', 'AA_']))

    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(5, 0, tileSize)), ['', '_AA', 'AA_', '_A_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(5, 1, tileSize)), ['_AA', 'AAA', 'AAA', 'AA_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(5, 2, tileSize)), ['AAA', 'AAA', 'AA_', '_AA']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(5, 3, tileSize)), ['_AA', 'AA_', '', '_A_']))

    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(6, 0, tileSize)), ['', '_A_', '_AA', 'AA_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(6, 1, tileSize)), ['AA_', '_AA', 'AAA', 'AAA']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(6, 2, tileSize)), ['AAA', 'AA_', '_AA', 'AAA']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(6, 3, tileSize)), ['AA_', '_A_', '', '_AA']))

    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(7, 0, tileSize)), ['_AA', 'AA_', '_A_', '_A_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(7, 1, tileSize)), ['_A_', '', '_AA', 'AA_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(7, 2, tileSize)), ['AA_', '', '_A_', '_AA']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(7, 3, tileSize)), ['_A_', '_AA', 'AA_', '_A_']))

    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(8, 0, tileSize)), ['', '_AA', 'AA_', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(8, 1, tileSize)), ['_AA', 'AAA', 'AA_', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(8, 2, tileSize)), ['_AA', 'AAA', 'AA_', '_A_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(8, 3, tileSize)), ['_AA', 'AA_', '', '']))

    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(9, 0, tileSize)), ['_A_', '_AA', 'AAA', 'AA_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(9, 1, tileSize)), ['_AA', 'AA_', '_AA', 'AA_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(9, 2, tileSize)), ['AAA', 'AAA', 'AAA', 'AAA']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(9, 3, tileSize)), ['AAA', 'AA_', '', '_AA']))

    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(10, 0, tileSize)), ['', '_AA', 'AAA', 'AA_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(10, 1, tileSize)), ['', '', '', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(10, 2, tileSize)), ['AA_', '_AA', 'AA_', '_AA']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(10, 3, tileSize)), ['AAA', 'AA_', '_A_', '_AA']))

    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(11, 0, tileSize)), ['', '', '_AA', 'AA_']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(11, 1, tileSize)), ['AA_', '_A_', '_AA', 'AAA']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(11, 2, tileSize)), ['AA_', '', '_AA', 'AAA']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(11, 3, tileSize)), ['AA_', '', '', '_AA']))

    return tileDefs

def createAtlasMetaSub(tileSize, tl, tr, bl, br):
    halfTile = int(tileSize / 2)
    sub = Image.new("RGB", (tileSize, tileSize))
    sub.paste(tl, (0, 0))
    sub.paste(tr, (halfTile, 0))
    sub.paste(bl, (0, halfTile))
    sub.paste(br, (halfTile, halfTile))
    return sub

def loadAtlasMeta(atlasMetaPath, tileSize, inward, outward):
    tileDefs = []

    halfTile = tileSize / 2
    ATLAS_META_TILES_X = 6
    ATLAS_META_TILES_Y = 1
    atlasMetaImage = Image.open(atlasMetaPath).resize((tileSize * ATLAS_META_TILES_X, tileSize * ATLAS_META_TILES_Y), resample=0)

    tlcurve = atlasMetaImage.crop((0, 0, halfTile, halfTile))
    trcurve = atlasMetaImage.crop((halfTile, 0, halfTile * 2, halfTile))
    blcurve = atlasMetaImage.crop((0, halfTile, halfTile, halfTile * 2))
    brcurve = atlasMetaImage.crop((halfTile, halfTile, halfTile * 2, halfTile * 2))
    tlver = atlasMetaImage.crop((halfTile * 2, 0, halfTile * 3, halfTile))
    trver = atlasMetaImage.crop((halfTile * 3, 0, halfTile * 4, halfTile))
    blver = atlasMetaImage.crop((halfTile * 2, halfTile, halfTile * 3, halfTile * 2))
    brver = atlasMetaImage.crop((halfTile * 3, halfTile, halfTile * 4, halfTile * 2))
    tlhor = atlasMetaImage.crop((halfTile * 4, 0, halfTile * 5, halfTile))
    trhor = atlasMetaImage.crop((halfTile * 5, 0, halfTile * 6, halfTile))
    blhor = atlasMetaImage.crop((halfTile * 4, halfTile, halfTile * 5, halfTile * 2))
    brhor = atlasMetaImage.crop((halfTile * 5, halfTile, halfTile * 6, halfTile * 2))
    tlcor = atlasMetaImage.crop((halfTile * 6, 0, halfTile * 7, halfTile))
    trcor = atlasMetaImage.crop((halfTile * 7, 0, halfTile * 8, halfTile))
    blcor = atlasMetaImage.crop((halfTile * 6, halfTile, halfTile * 7, halfTile * 2))
    brcor = atlasMetaImage.crop((halfTile * 7, halfTile, halfTile * 8, halfTile * 2))
    tlemp = atlasMetaImage.crop((halfTile * 8, 0, halfTile * 9, halfTile))
    tremp = atlasMetaImage.crop((halfTile * 9, 0, halfTile * 10, halfTile))
    blemp = atlasMetaImage.crop((halfTile * 8, halfTile, halfTile * 9, halfTile * 2))
    bremp = atlasMetaImage.crop((halfTile * 9, halfTile, halfTile * 10, halfTile * 2))
    tlfil = atlasMetaImage.crop((halfTile * 10, 0, halfTile * 11, halfTile))
    trfil = atlasMetaImage.crop((halfTile * 11, 0, halfTile * 12, halfTile))
    blfil = atlasMetaImage.crop((halfTile * 10, halfTile, halfTile * 11, halfTile * 2))
    brfil = atlasMetaImage.crop((halfTile * 11, halfTile, halfTile * 12, halfTile * 2))

    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcurve, trcurve, blver, brver), [f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlver, trver, blver, brver), [f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlver, trver, blcurve, brcurve), [f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcurve, trcurve, blcurve, brcurve), [f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcurve, trhor, blver, brcor), [f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlver, trcor, blver, brcor), [f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlver, trcor, blcurve, brhor), [f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlhor, trhor, blcor, brcor), [f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, trcor, blcor, brcor), [f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, trcor, blhor, brhor), [f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlhor, trcurve, blcor, brver), [f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, trver, blcor, brver), [f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, trver, blhor, brcurve), [f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcurve, trhor, blcurve, brhor), [f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlhor, trhor, blhor, brhor), [f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlhor, trcurve, blhor, brcurve), [f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, trcor, blcor, brcor), [f'{inward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{inward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlver, trcor, blver, bremp), [f'{outward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlver, tremp, blver, brcor), [f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, trcor, blemp, brcor), [f'{outward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlhor, trhor, blcor, bremp), [f'{outward}{outward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, tremp, blemp, bremp), [f'{outward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, tremp, blcor, bremp), [f'{inward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{inward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, tremp, blhor, brhor), [f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlhor, trhor, blemp, brcor), [f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, trcor, blemp, bremp), [f'{inward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{inward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, tremp, blemp, brcor), [f'{inward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{inward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, trcor, blhor, brhor), [f'{inward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{inward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, tremp, blcor, brcor), [f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, trver, blemp, brver), [f'{outward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, trver, blcor, brver), [f'{inward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{inward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, trcor, blcor, bremp), [f'{outward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcurve, trhor, blver, bremp), [f'{outward}{outward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlver, tremp, blver, bremp), [f'{outward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, tremp, blcor, bremp), [f'{outward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlver, tremp, blcurve, brhor), [f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, trcor, blemp, bremp), [f'{outward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlcor, tremp, blemp, brcor), [f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, tremp, blemp, bremp), [f'{inward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{inward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, tremp, blhor, brhor), [f'{inward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{inward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlhor, trhor, blemp, bremp), [f'{outward}{outward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{inward}', f'{inward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlfil, trfil, blfil, brfil), [f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, trcor, blcor, bremp), [f'{inward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{inward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, tremp, blcor, brcor), [f'{inward}{inward}{inward}', f'{inward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{inward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlhor, trcurve, blemp, brver), [f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{outward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, trcor, blemp, brcor), [f'{inward}{inward}{outward}', f'{outward}{inward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{inward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, trver, blemp, brver), [f'{inward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{inward}', f'{inward}{inward}{inward}']))
    tileDefs.append(addAtlasSub(createAtlasMetaSub(tileSize, tlemp, trver, blhor, brcurve), [f'{inward}{inward}{outward}', f'{outward}{outward}{outward}', f'{outward}{outward}{outward}', f'{outward}{inward}{inward}']))
    return tileDefs

def loadAtlasDungeon(atlasPath, tileSize):
    tileDefs = []
    atlasImage = Image.open(atlasPath).resize((tileSize * 4, tileSize * 4), resample=0)
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(0, 0, tileSize)), ['', '', '', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(1, 0, tileSize)), ['', 'A', '', 'A']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(2, 0, tileSize)), ['A', '', 'A', '']))

    #tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(0, 1, tileSize)), ['A', '', '', '']))
    #tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(1, 1, tileSize)), ['', 'A', '', '']))
    #tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(2, 1, tileSize)), ['', '', 'A', '']))
    #tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(3, 1, tileSize)), ['', '', '', 'A']))

    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(0, 2, tileSize)), ['A', 'A', '', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(1, 2, tileSize)), ['', 'A', 'A', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(2, 2, tileSize)), ['', '', 'A', 'A']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(3, 2, tileSize)), ['A', '', '', 'A']))

    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(0, 3, tileSize)), ['A', 'A', 'A', '']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(1, 3, tileSize)), ['', 'A', 'A', 'A']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(2, 3, tileSize)), ['A', '', 'A', 'A']))
    tileDefs.append(addAtlasSub(atlasImage.crop(getCropSize(3, 3, tileSize)), ['A', 'A', '', 'A']))
    return tileDefs