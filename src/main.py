import pygame,sys
from settings import *
from player import Player
from car import Car
from random import choice,randint
from sprite import SimpleSprite,LongSprite

# customizing the draw method of the original group class
# add an offset which will be the player movement, draw/move all in the display surface -> to have a camera
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.bg = pygame.image.load("graphics/main/map.png").convert()
        self.fg = pygame.image.load("graphics/main/overlay.png").convert_alpha()

    def customize_draw(self):

        # change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2 
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # blit the background
        display_surf.blit(self.bg,-self.offset) # -> the self.offset should always be negative to have the camera move the opposite of the players movement

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): # self.sprites() -> accesses all of the sprites inside of the group, which is in the form of a list
            offset_pos = sprite.rect.topleft - self.offset
            display_surf.blit(sprite.image,offset_pos)

        display_surf.blit(self.fg,-self.offset)

# basic 
pygame.init()
display_surf = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()

# sprite groups
all_sprites = AllSprites()
obstacle_sprite = pygame.sprite.Group()
# sprite creation
player = Player((2062,3274),all_sprites,obstacle_sprite)

# timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer,50) # trigger the car_timer every 200 miliseconds
pos_list = []

# font
font = pygame.font.Font(None,50)
text_surf = font.render("VICTORY!",True,"white")
text_rect = text_surf.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

# music
music = pygame.mixer.Sound("audio/music.mp3")
music.play(loops = -1)

# sprite setup
for file_name, position_list in SIMPLE_OBJECTS.items():
    path = f"graphics/objects/simple/{file_name}.png"
    surf = pygame.image.load(path).convert_alpha()
    for pos in position_list:
        SimpleSprite(surf,pos,[all_sprites,obstacle_sprite])

for file_name, position_list in LONG_OBJECTS.items():
    path = f"graphics/objects/long/{file_name}.png"
    surf = pygame.image.load(path).convert_alpha()
    for pos in position_list:
        LongSprite(surf,pos,[all_sprites,obstacle_sprite])


# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # spawn a car every time car_time is called at a random positon
        if event.type == car_timer: 
            random_pos = choice(CAR_START_POSITIONS)

            # check if the random_pos is not doubled to prevent drawing the the cars at the same postion
            if random_pos not in pos_list:
                pos_list.append(random_pos)
                pos = (random_pos[0],random_pos[1] + randint(-8,8))
                Car(random_pos,[all_sprites,obstacle_sprite])

            # delete a random_pos if the pos_list contains 5 random_pos
            if len(pos_list) > 5:
                del pos_list[0]


    # delta time
    dt = clock.tick(FPS) / 1000


    if player.pos.y >= 1180:

        # update
        all_sprites.update(dt)

        # draw object
        all_sprites.customize_draw()

    else:
        display_surf.fill("teal")
        display_surf.blit(text_surf,text_rect)

    # draw the frames
    pygame.display.update()
