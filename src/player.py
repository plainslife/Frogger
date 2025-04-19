import pygame,sys
from os import walk # walk through the specific file and give its path and name

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)

        # images for animation
        self.import_assests()
        self.frame_index = 0
        self.status = "up"
        self.animation_speed = 10
        
        #self.image = self.animation[self.frame_index]
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 200

        # collisions
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(0,-self.rect.height / 2)

    def collision(self,direction):
        if direction == "horizontal":
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite,"name") and sprite.name == "car":
                        pygame.quit()
                        sys.exit()
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx # update also the rect to prevent the screen from wobbling
                        self.pos.x = self.hitbox.centerx
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
        if direction == "vertical":
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite,"name") and sprite.name == "car":
                        pygame.quit()
                        sys.exit()
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def import_assests(self):

        # better import
        self.animations = {}

        # to get a dictionary with a key and its values are the surfaces
        for index,folder in enumerate(walk("graphics/player")):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2]):
                    path = f"{folder[0]}/{file_name}"
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split("/")[-1]
                    self.animations[key].append(surf)

    def move(self,dt):

        # normalize a vector -> the lenght of a vector is going to be 1, in order to get the consistent speed regardless of the movement
        if self.direction.magnitude() != 0: # .magnitude() -> is the way to get the length of a vector
            self.direction = self.direction.normalize()

        # horizontal movement + collision
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = (round(self.pos.x)) # for the collision
        self.rect.centerx = self.hitbox.centerx # for the position
        self.collision("horizontal")

        # vertical movement + collision
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = (round(self.pos.y)) # for the collision
        self.rect.centery = self.hitbox.centery # for the position
        self.collision("vertical") 

        # self.pos += self.direction * self.speed * dt 
        # self.rect.center = (round(self.pos.x),round(self.pos.y))

    def input(self):
        keys = pygame.key.get_pressed() # will return a list of all the keyboard keys

        # horizontal input
        if keys[pygame.K_RIGHT]:
            self.status = "right"
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.status = "left"
            self.direction.x = -1
        else:
            self.direction.x = 0

        # vertical input
        if keys[pygame.K_UP]:
            self.status = "up"
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.status = "down"
            self.direction.y = 1
        else: 
            self.direction.y = 0

    # animate the player
    def animate(self, dt):
        current_animation = self.animations[self.status]

        if self.direction.magnitude() != 0: # player is moving

            if self.frame_index < 1: # when moving start at frame 1
                self.frame_index = 1
            else: # delay before next animation
                self.frame_index += self.animation_speed * dt

            # reset frame index when it is that last index
            if self.frame_index >= len(current_animation):
                self.frame_index = 1 # frame 0 is for not moving

        else: # player is not moving set the frame to 0 where the player image is standing
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    # limit the area where the player can move
    def restrict(self):
         if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2 # this is whre the positon where the player can move
            self.hitbox.left = 640
            self.rect.left = 640
         if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.left = 2560
         if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery

    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.restrict()

                  
