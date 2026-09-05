import pygame, pytmx,pyscroll
from animation import AnimateSprite
class Entity(AnimateSprite):

    def __init__(self,name, x, y):
        super().__init__(name)
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

    def save_location(self): self.old_position = self.position.copy()
   
   
    def move_right(self):
        self.change_animation("right")
        self.position[0]+=self.speed        

    def move_left(self):
        self.change_animation('left')
        self.position[0]-=self.speed
          
    def move_up(self):
        self.change_animation('up')
        self.position[1]-=self.speed      
    
    def move_down(self):
        self.change_animation('down')
        self.position[1]+=self.speed
        
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.update()


class Player(Entity):
    def __init__(self):
        super().__init__('player',0,0)
        self.__speed=0

    def get_speed(self):
        return self.__speed

class Boss(Entity):
    def __init__(self,name,nb_points,battu=[]):
        super().__init__(name,0,0)
        self.nb_points=nb_points
        self.points=[]
        self.battu=list()
        self.__name=name
        self.speed=1
        self.current_point=0

    def get_name(self):
        return self.__name
   
    def move(self):
        current_point=self.current_point
        target_point=self.current_point+1

        if target_point>=self.nb_points:
            target_point=0
       
        current_rect=self.points[current_point]
        target_rect=self.points[target_point]
  
        if current_rect.y< target_rect.y and abs(current_rect.x - target_rect.x)<3:
            self.move_down()
        elif current_rect.y>target_rect.y and abs(current_rect.x-target_rect.x)<3:
            self.move_up()
        elif current_rect.x>target_rect.x and abs(current_rect.y-target_rect.y)<3:
            self.move_left()
        elif current_rect.x<target_rect.x and abs(current_rect.y-target_rect.y)<3:
            self.move_right()   

        if self.rect.colliderect(target_rect):
            self.current_point=target_point   


    def teleport_spawn(self):
        location=self.points[self.current_point]
        self.position[0]=location.x
        self.position[1]=location.y
        self.save_location()

    def load_points(self,tmx_data):
        for num in range(1,self.nb_points+1):
            point=tmx_data.get_object_by_name(f'{self.__name}_path{num}')
            rect=pygame.Rect(point.x,point.y,point.width,point.height)
            self.points.append(rect)

    def ajoute(self,name,valeur):
        self.battu.append((name,valeur))

from dataclasses import dataclass

@dataclass
class Portal:
    from_world:str
    origin_point:str
    target_world:str
    teleport_point:str


@dataclass
class Map:
    name:str
    walls:list[pygame.Rect]
    group:pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals:list[Portal]
    npcs:list[Boss]

tab_map=['world','bossrue','bossforet','ice','bossfire']
class MapManager:
    def __init__(self,screen,player):
        self.maps=dict()
        self.screen=screen
        self.player=player
        self.players=Player()
        self.current_map=tab_map
        
        self.register_map('world',portals=[
            Portal(from_world='world',origin_point='enter_rue',target_world='rue',teleport_point='spawn_rue'),
            Portal(from_world='world',origin_point='enter_fire',target_world='fire',teleport_point='spawn_fire'),
            Portal(from_world='world',origin_point='enter_foret',target_world='foret',teleport_point='spawn_foret'),
            Portal(from_world='world',origin_point='enter_ice',target_world='ice',teleport_point='spawn_ice')
        ])
        self.register_map('rue',portals=[
            Portal(from_world='rue',origin_point='exit_rue',target_world='world',teleport_point='enter_rue_exit'),
            Portal(from_world='rue',origin_point='enter_bossrue',target_world='bossrue',teleport_point='spawn_bossrue')
        ])
        self.register_map('ice',portals=[
            Portal(from_world='ice',origin_point='exit_ice',target_world='world',teleport_point='enter_ice_exit')
        ],npcs=[
            Boss('boss',nb_points=2),
        ])
        self.register_map('fire',portals=[
            Portal(from_world='fire',origin_point='exit_fire',target_world='world',teleport_point='enter_fire_exit'), 
            Portal(from_world='fire',origin_point='enter_bossfire',target_world='bossfire',teleport_point='spawn_bossfire')
        ])
        self.register_map('foret',portals=[
            Portal(from_world='foret',origin_point='exit_foret',target_world='world',teleport_point='enter_foret_exit'), 
            Portal(from_world='foret',origin_point='enter_bossforet',target_world='bossforet',teleport_point='spawn_bossforet')
        ])
        self.register_map('bossfire',portals=[
            Portal(from_world='bossfire',origin_point='exit_bossfire',target_world='fire',teleport_point='enter_bossfire_exit')     
        ],npcs=[
            Boss('boss',nb_points=2),
        ])
        self.register_map('bossforet',portals=[
            Portal(from_world='bossforet',origin_point='exit_bossforet',target_world='foret',teleport_point='enter_bossforet_exit')     
        ],npcs=[
            Boss('boss',nb_points=2),
        ])
        self.register_map('bossrue',portals=[
            Portal(from_world='bossrue',origin_point='exit_bossrue',target_world='rue',teleport_point='enter_bossrue_exit')     
        ],npcs=[
            Boss('boss',nb_points=2),
        ])
        self.teleport_player('player')
        self.teleport_npcs()

    def check_collisions(self):
        for portal in self.get_map().portals:
            if portal.from_world==self.current_map[0]:
                point=self.get_object(portal.origin_point)
                rect=pygame.Rect(point.x,point.y,point.width,point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal=portal
                    self.current_map[0]=portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        for sprite in self.get_group().sprites():
            if type(sprite) is Boss:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed=0
                else:
                    sprite.speed=1
            if sprite.feet.collidelist(self.get_walls())>-1:
                sprite.move_back()

    def teleport_player(self,name):
        point=self.get_object(name)
        self.player.position[0]=point.x
        self.player.position[1]=point.y
        self.player.save_location()

    def register_map(self,name,portals=[],npcs=[]):
       tmx_data = pytmx.util_pygame.load_pygame(f'{name}.tmx')
       map_data = pyscroll.data.TiledMapData(tmx_data)
       map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
       map_layer.zoom = 2

       walls = []
       for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
       group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
       group.add(self.player)

       for npc in npcs:
            group.add(npc)

       self.maps[name]=Map(name,walls,group,tmx_data,portals,npcs)

    def get_map(self):return self.maps[self.current_map[0]]
    def get_group(self):return self.get_map().group
    def get_walls(self):return self.get_map().walls
    def get_object(self,name):return self.get_map().tmx_data.get_object_by_name(name) 
    def teleport_npcs(self):
        for map in self.maps:
            map_data=self.maps[map]
            npcs=map_data.npcs
            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()


    def draw(self):  
        self.get_group().draw(self.screen)    
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()


