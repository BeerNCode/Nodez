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

        return output

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