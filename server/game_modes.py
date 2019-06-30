import colours
import random
import pygame
import math
import map_generator
import game_modes
import maptiles
from controls import Controls
from vector import Vector
from nodes import Node
from player import Player
from team import Team

number_of_source_nodes = 1
number_of_teams = 2
number_of_nodes = 20
number_of_players = 4



def generate_basic(width, height, controls):
    
    map_gen = map_generator.MapGenerator((width, height, 32))
    block_map = map_gen.generate_block_map(5)
    numX = map_gen.numX
    numY = map_gen.numY
#    numX = int(math.ceil(width/32.0))
#    numY = int(math.ceil(height/32.0))
#    block_map = [[0] * numY for _ in range(numX)]
#    for i in range(numX):
#        for j in range(numY):
#            if random.random() > 0.95:
#                block_map[i][j] = -1

    world = maptiles.MapTiles(block_map, numX, numY)

    teams = []
    nodes = []
    for t in range(number_of_teams):
        colour = colours.TEAM_COLOURS[t]
        team = Team(f"Team {t}", colour)
        node = Node(True,False,Vector(world.width*random.random(), world.height*random.random()), 100)
        node.team = team
        team.node = node
        teams.append(team)
        nodes.append(node)

    for i in range(number_of_nodes):
        x = random.random() * world.width
        y = random.random() * world.height
        r = random.random() * 100 + 50
        nodes.append(Node(False,False,Vector(x, y), r))

    for i in range(number_of_source_nodes):
        x = random.random() * world.width
        y = random.random() * world.height
        r = random.random() * 100 + 50
        nodes.append(Node(True,True,Vector(x, y), r))

    players = []
    t = 0
    for control in controls:
        team = teams[t]
        t += 1
        if t >= len(teams):
            t = 0
        players.append(Player(f"Player {i}", team, control))

    return {
        "nodes": nodes,
        "teams": teams,
        "players": players,
        "world": world
    }