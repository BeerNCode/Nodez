import math
import random

class MapGenerator:

    numX = None
    numY = None
    
    def __init__(self, screenSize, tileSize):
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]

        tileSizeFloat = float(tileSize)

        self.numX = int(math.ceil(screenWidth/tileSizeFloat))
        self.numY = int(math.ceil(screenHeight/tileSizeFloat))

    def generate(self, numFeatures):
        output = [[0] * self.numY for _ in range(self.numX)]
        
        n = numFeatures
        while (n != 0):
            for tile in self.getRandomTilesForFeature():
                if (output[tile[0]][tile[1]] == 0):
                    output[tile[0]][tile[1]] = -1
            n-=1

        return self.transform_map(output)

    def getRandomTilesForFeature(self):
        x = random.randint(0, self.numX-1)
        y = random.randint(0, self.numY-1)

        featureTiles = []
        featureTiles.append((x,y))

        dir = self.get_direction()
        while (dir != 0):
            if (dir % 2 == 0):
                x += dir - 3
            else:
                y += dir - 2

            if (x < 0 or x >= self.numX):
                break
            elif (y < 0 or y >= self.numY):
                break
            else:
                featureTiles.append((x, y))
        
        return featureTiles
    
    def get_direction(self):
        return random.randint(0, 4)

    def transform_map(self, map_tiles):
        output = [[0] * self.numY for i in range(self.numX)]

        max_x = self.numX - 1
        max_y = self.numY - 1

        for ix in range(self.numX):
            for iy in range(self.numY):
                if (map_tiles[ix][iy] < 0):
                    output[ix][iy] = 15
                    continue
                
                if (iy == 0 or map_tiles[ix][iy-1] < 0):
                    output[ix][iy] += 8
                if (ix == max_x or map_tiles[ix+1][iy] < 0):
                    output[ix][iy] += 4
                if (iy == max_y or map_tiles[ix][iy+1] < 0):
                    output[ix][iy] += 2
                if (ix == 0 or map_tiles[ix-1][iy] < 0):
                    output[ix][iy] += 1
        
        return list(map(lambda col: list(map(self.transform_value, col)), output))

    def transform_value(self, val):
        output = ''
        if (val & 8 == 8): output += 'X'
        else: output += 'O'
        if (val & 4 == 4): output += 'X'
        else: output += 'O'
        if (val & 2 == 2): output += 'X'
        else: output += 'O'
        if (val & 1 == 1): output += 'X'
        else: output += 'O'
        return output