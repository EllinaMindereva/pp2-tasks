import pygame
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((800, 400))

font = pygame.font.SysFont("comicsansms", 20)

playlist = ["meow.mp3", "duck.mp3"]

player = MusicPlayer(playlist)
player.load()

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0, 0, 102))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.previous()
            elif event.key == pygame.K_q:
                running = False

    track = player.get_curr()

    text1 = font.render(f"Track: {track}", True, (255, 255, 255))
    text2 = font.render("P = play   S = stop    N = next track  B = previous track(back)    Q = quit", True, (51, 153, 255))
    screen.blit(text1, (20, 50))
    screen.blit(text2, (20, 120))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
