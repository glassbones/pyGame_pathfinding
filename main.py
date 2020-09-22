
import pygame




def main(win, width, preset = None, scale = 60):
    ROWS = scale
    grid = set_grid(ROWS, width, preset)
    find_branches(win, grid, ROWS, width)
    start = None
    target = None
    seen = set()
    all_cells = all_cells_of(grid)
    counter = Counter(0)

    run = True
    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                if not start and cell != target:
	                start = cell
	                start.set_start()

                elif not target and cell != start:
	                target = cell
	                target.set_target()

                elif cell != target and cell != start:
	                cell.set_active()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
	            pos = pygame.mouse.get_pos()
	            row, col = get_clicked_pos(pos, ROWS, width)
	            cell = grid[row][col]
	            cell.set_inactive()
	            if cell == start:
		            start = None
	            elif cell == target:
		            target = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start:
                    # current position is circuit flag
                    circuit_flag = start
                    branch_flags = []

                    while len(seen) != len(all_cells):
                        
                        start.set_is_seen()
                        seen.add(start)
                        print(f'start is {start.x} , {start.y}')
                        # if branch flag at current position remove it
                        branch_flags = [ _ for _ in branch_flags if _ != start ]
                        # if 2 or more current neighbors are untraveled nodes branch flag here
                        unseen = [neighbor for neighbor in start.neighbors if not neighbor.is_seen]
                        if len(unseen) > 1: branch_flags.append(start)
                        # if 2 or more current neighbors are untraveled circuit nodes circuit flag here
                        unseen_circuit_cells = [neighbor for neighbor in unseen if not neighbor.is_branch and not neighbor.is_seen]
                        if len(unseen_circuit_cells) > 1: circuit_flag = start

                        # if no untraveled neighbors, target is last branch flag
                        print(f'unseen = {[neighbor.x for neighbor in start.neighbors if not neighbor.is_seen]}')
                        if unseen == []:
                            if branch_flags != []:
                                target = branch_flags[-1]
                            elif branch_flags == []:
                                # if no branch flag return to circuit flag
                                if target != start:
                                    target = circuit_flag
                                # if current position is circuit flag maze should be complete ???????????
                                if target == start:
                                    print('this shouldn\'t print unless everything is explored') 
                        
                        # if any neighbor is untraveled branch node target is that node pick node farther from last circuit flag
                        print(f'unseen = {[neighbor.x for neighbor in start.neighbors if not neighbor.is_seen]}')
                        if unseen != []:
                            unseen_branch_cells = [neighbor for neighbor in unseen if neighbor.is_branch]
                            # this is not optimal, need a tie breaker function that travels shortest dead end first
                            print(f'unseen branches = {[neighbor for neighbor in unseen if neighbor.is_branch]}')
                            if unseen_branch_cells != []: target = unseen_branch_cells[0]
                            else:
                                print(f'unseen circuits = {[neighbor for neighbor in unseen if not neighbor.is_branch]}')
                                # if any neighbor is untraveled circuit node target pick optimal path
                                if len(unseen_circuit_cells) == 4: target = circuit_compare(circuit_compare(unseen_circuit_cells[0],unseen_circuit_cells[1]), circuit_compare(unseen_circuit_cells[2],unseen_circuit_cells[3]))
                                if len(unseen_circuit_cells) == 3: target = circuit_compare(unseen_circuit_cells[0],unseen_circuit_cells[1],unseen_circuit_cells[2])
                                if len(unseen_circuit_cells) == 2: target = circuit_compare(unseen_circuit_cells[0],unseen_circuit_cells[1])
                                else: target = unseen_circuit_cells[0]

                        if len(unseen) == 1: target = unseen[0]

                        for row in grid:
                            for cell in row:
                                cell.update_neighbors(grid)
                        print(f'target is {target.x} , {target.y}')
                        algorithm(lambda: draw(win, grid, ROWS, width), grid, start, target, counter)

                        start = target
                        start.color = ORANGE
                        target = None
                
                
                print(f'step count = {counter.count}')
                print(len(all_cells))
                print(len(seen))


                if event.key == pygame.K_c:
                    start = None
                    target = None
                    grid = set_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH, cell_graph)