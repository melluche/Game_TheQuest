import pygame, sys
from pygame import mixer
from button import Button
from game import Game
 
pygame.init()

SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Menu")
mixer.music.load("Backgrounds/song_animal_crossing.wav")
mixer.music.play(-1)

BG = pygame.image.load("assets/Background.jpg")

def get_font(size): 
    return pygame.font.Font("assets/laquete.ttf", size)

def play():
    while True:
        game=Game()
        game.run()
        pygame.display.update()

def enigme():
    while True:
        ENIGME_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        ENIGME_TEXT = get_font(45).render("1=up,2=right,3=down,4=left", True, "Black")

        ENIGME_RECT = ENIGME_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(ENIGME_TEXT, ENIGME_RECT)

        ENIGME_BACK = Button(image=None, pos=(640, 460), text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        ENIGME_BACK.changeColor(ENIGME_MOUSE_POS)
        ENIGME_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ENIGME_BACK.checkForInput(ENIGME_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def credits():
    while True:
        CREDITS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        CREDITS_TEXT = get_font(45).render("Mellyna et Kelvish ont tout fait et les deux autres le design (donc pas grand chose)", True, "Black")

        CREDITS_RECT = CREDITS_TEXT.get_rect(center=(960, 540))
        SCREEN.blit(CREDITS_TEXT, CREDITS_RECT)

        CREDITS_BACK = Button(image=None, pos=(860, 690), text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        CREDITS_BACK.changeColor(CREDITS_MOUSE_POS)
        CREDITS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CREDITS_BACK.checkForInput(CREDITS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(150).render("La Quete", True, "#000066")
        MENU_RECT = MENU_TEXT.get_rect(center=(960, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play_Rect.png"), pos=(960, 400), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        ENIGME_BUTTON = Button(image=pygame.image.load("assets/Play_Rect.png"), pos=(960, 550), 
                            text_input="ENIGME", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        CREDITS_BUTTON = Button(image=pygame.image.load("assets/Play_Rect.png"), pos=(960, 700), 
                            text_input="CREDITS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit_Rect.png"), pos=(960, 850), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, ENIGME_BUTTON, QUIT_BUTTON,CREDITS_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if ENIGME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    enigme()
                if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    credits()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
