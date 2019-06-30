import colours
import random
import pygame
import map_generator
import maptiles
import math
import logging
from controls import Controls
from vector import Vector
from nodes import Node
from player import Player
from team import Team

logger = logging.getLogger(__name__)

number_of_source_nodes = 1
number_of_teams = 2
number_of_nodes = 20
number_of_players = 4

CONTROLS = [
    {"up": pygame.K_UP,"down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "space": pygame.K_SPACE},
    {"up": pygame.K_w,"down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "space": pygame.K_e},
    {"up": pygame.K_t,"down": pygame.K_g, "left": pygame.K_f, "right": pygame.K_h, "space": pygame.K_y},
    {"up": pygame.K_i,"down": pygame.K_k, "left": pygame.K_j, "right": pygame.K_l, "space": pygame.K_o}
]


def generate_basic(width, height):
    mapGen = map_generator.MapGenerator((width, height), maptiles.TILESIZE)
    block_map = mapGen.generate_block_map(10)
    world = maptiles.MapTiles(block_map, mapGen.numX, mapGen.numY)

    teams = []
    nodes = []
    for t in range(number_of_teams):
        colour = colours.TEAM_COLOURS[t]
        team = Team(f"Team {t}", colour)
        node = Node(True,False,Vector(world.width*random.random(), world.height*random.random()))
        node.team = team
        team.node = node
        teams.append(team)
        nodes.append(node)

    for i in range(number_of_nodes):
        check_seed = False
        while check_seed == False:        
            x = random.random() * world.width
            y = random.random() * world.height
            check_seed = check_boundary(x, y, 15, world)
        nodes.append(Node(False,False,Vector(x, y)))
           
    for i in range(number_of_source_nodes):
        check_seed = False
        while check_seed == False:
            x = random.random() * world.width
            y = random.random() * world.height
            check_seed = check_boundary(x, y, 15, world)
        nodes.append(Node(True,True,Vector(x, y)))

    players = []
    t = 0

    for i in range(number_of_players):
        joystick = None
        if (i>=number_of_players-pygame.joystick.get_count()):
            joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
            joysticks[i-(number_of_players-pygame.joystick.get_count())].init()
            joystick = joysticks[i-(number_of_players-pygame.joystick.get_count())]
        controls = Controls(CONTROLS[i],joystick)
        team = teams[t]
        t += 1
        if t >= len(teams):
            t = 0
        players.append(Player(f"Player {i}",team,controls))

    return {
        "nodes": nodes,
        "teams": teams,
        "players": players,
        "world": world
    }

def check_boundary(x, y, width, world):
    row = []
    row.append(math.floor((y - width)/ maptiles.TILESIZE))
    row.append(math.floor((y + width)/ maptiles.TILESIZE))

    column = []
    column.append(math.floor((x - width)/ maptiles.TILESIZE))
    column.append(math.floor((x + width)/ maptiles.TILESIZE))

    checkrow = 0
    while checkrow < 2:
        checkcolumn = 0
        while checkcolumn < 2 :
            if world.access_map[column[checkrow]][row[checkcolumn]] != 15:
                return True
            checkcolumn += 1
        checkrow +=1
    return False
