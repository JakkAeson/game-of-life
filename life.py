import os
import random
import time

def iterate(world):
    next_world = []
    for row_index, row in enumerate(world):
        next_world.append([])
        for col_index, _ in enumerate(row):
            next_world[row_index].append(check_cell(world, row_index, col_index))

    return next_world

def check_cell(world, world_row, world_col):
    neighbour_count = 0
    for i in [-1, 0, 1]:
        row = wrap(world_row + i, 0, len(world) - 1)
        for j in [-1, 0 ,1]:
            col = wrap(world_col + j, 0, len(world[0]) - 1)
            if i != 0 or j != 0:
                neighbour_count += world[row][col]

    if (world[world_row][world_col] == 1) and (neighbour_count in [2, 3]):
        return 1
    elif (world[world_row][world_col] == 0) and (neighbour_count == 3):
        return 1
    else:
        return 0

def print_world(world, generation, population, clear):
    world_string = ''
    for row in world:
        for cell in row:
            world_string += '█' if cell == 1 else ' '
        world_string += '\n'

    if clear:
        os.system('CLS')

    print(world_string)
    print(f'Generation {generation}, population {population}')
    print('Press CTRL-C to stop')

    if not clear:
        print('=' * len(world[0]))

def wait_next_tick(speed):
    time.sleep(1/speed)

def create_cell(chance):
    return 1 if random.random() <= chance else 0

def wrap(value, lower, upper):
    return upper if value < lower else lower if value > upper else value

def life():
    clear_terminal_each_generation = True # this works on Windows, not sure on other systems
    cell_chance = 0.2
    speed = 10
    w = 100
    h = 20
    
    world = [[create_cell(cell_chance) for _ in range(w)] for _ in range(h)]
    population = sum(map(sum, world)) # sum each row in world, then sum all of those sums
    stagnant_count = 0
    generation = 0
    prev_pop = 0
    
    try:
        while True:
            print_world(world, generation, population, clear_terminal_each_generation)

            if population <= 0:
                print('The game has ended.')
                break
            elif stagnant_count >= 10:
                print('The final shape has been achieved.')
                break

            world = iterate(world)
            generation += 1
            population = sum(map(sum, world))

            if population == prev_pop:
                stagnant_count += 1
            else:
                stagnant_count = 0
            prev_pop = population

            wait_next_tick(speed)
    except KeyboardInterrupt: # press Ctrl-C to stop
        pass

if __name__ == '__main__':
    life()
    input('Press Enter to exit.')
