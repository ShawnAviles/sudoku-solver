# Shawn Aviles 12/9/2021 
# notes on pygame gui
# base gui template (opens blank white window)
import pygame

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)

def draw_window():
    WIN.fill((WHITE))
    pygame.display.update()

def main():
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            draw_window()   
    pygame.quit()

# if statement only allows for code to be run from this file not if its imported
if __name__ == "__main__":    
    main()