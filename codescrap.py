
s1 = set([1,2,3,4])
s2 = set([1,6,7,4])
print(s2.difference(s1))

"""

pygame.font.init()
FONT = pygame.font.SysFont(None, 25)

def draw_text(str, color):
    text = FONT.render(str, True, color)
    WIN.blit( text, [ WIDTH/2 , WIDTH/2 ] )

def pause():
    paused = True

    while paused:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_2:
                    paused == False
                    break
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

    WIN.fill(BLACK)
    draw_text("Paused", WHITE, -100, size="large")
    draw_text("Press ESC to continue or Q to quit.", WHITE, 25)
    pygame.display.update()
"""

"""
    if event.key == pygame.K_ESCAPE:
        pause()
"""
