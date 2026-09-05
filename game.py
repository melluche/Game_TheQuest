import pygame
from player import Player,MapManager,Boss
import csv

class Game:
    def __init__(self):
        # Affichage de la fenêtre
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("la quete")
        self.player = Player()
        self.boss=Boss('boss',2)
        self.map_manager= MapManager(self.screen,self.player)
        self.dialog_box=DialogBox()


    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def update(self):
        self.map_manager.update()

    def set_counter(self):
        L=[]
        with open('boss.csv','r') as csv.file:
            csv_reader=csv.reader(csv.file)
            next(csv_reader)
            for i in csv_reader:
                counter1=0
                counter2=0
                counter3=0
                counter4=0
                tab_map=['world','bossrue','bossforet','ice','bossfire']
                for m in range(0,len(tab_map)):
                    if self.map_manager.current_map[m]=="bossrue":
                        counter1+=4
                        i[2]=counter1
                        L.append(int(i[2]))
                    elif self.map_manager.current_map[m]=="ice":
                        counter2+=3
                        i[2]=counter2
                        L.append(int(i[2]))
                    elif self.map_manager.current_map[m]=="bossfire":
                        counter3+=2
                        i[2]=counter3
                        L.append(int(i[2]))
                    elif self.map_manager.current_map[m]=="bossforet":
                        counter4+=1
                        i[2]=counter4
                        L.append(int(i[2]))
                return L

    def tri(self,L):
        N = len(L)
        for n in range(1,N):
            cle = L[n]
            j = n-1
            while j>=0 and L[j] > cle:
                L[j+1] = L[j] 
                j = j-1
                L[j+1] = cle
        return L

    def reduce_speed(self):
        self.player.get_speed().__sub__(2)

    def aug_speed(self):
        self.player.get_speed().__add__(1)

    def run(self):
        clock = pygame.time.Clock()
        running=True
        while running :
            if running==True:
                self.player.speed=5
                self.reduce_speed()
                self.aug_speed()
                self.player.save_location()
                self.handle_input()
                self.update()
                self.set_counter()
                self.map_manager.draw()
                self.dialog_box.render(self.screen)
                pygame.display.flip()

                for event in pygame.event.get():
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        pygame.quit()
                    elif event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_SPACE:
                            self.dialog_box.execute()
                clock.tick(60)
            else:
                return self.run()

class DialogBox(Game,MapManager):
    X_POSITION=60
    Y_POSITION=470
    def __init__(self):
        self.player = Player()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.map_manager= MapManager(self.screen,self.player)
        self.box=pygame.image.load('dialogs/dialog_box.png')
        self.box=pygame.transform.scale(self.box,(700,100))
        self.__texts=[("Chemin à suivre:%s"%(self.tri(self.set_counter())))]
        self.text_index=0
        self.letter_index=0
        self.font=pygame.font.Font("dialogs/dialog_font.ttf",18)
        self.reading=False
        
    def get_text(self):
        return self.__texts

    def execute(self):
        if self.reading:
            self.next_text()
        else:
            self.reading=True
            self.text_index=0

    def render(self,screen):
        if self.reading:
            self.letter_index+=1
            if self.letter_index>=len(self.get_text()[self.text_index]):
                self.letter_index=self.letter_index
            screen.blit(self.box,(self.X_POSITION,self.Y_POSITION))
            text=self.font.render(self.get_text()[self.text_index][0:self.letter_index],False,(0,0,0))
            screen.blit(text,(self.X_POSITION+60,self.Y_POSITION+30))

    def next_text(self):
        self.text_index+=1
        self.letter_index=0
        if self.text_index>=len(self.get_text()):
            self.reading=False