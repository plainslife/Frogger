import pygame 

class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_rect(topleft = pos)

        # another rect inside the original rect to display to overlapp when colliding with other objects
        self.hitbox = self.rect.inflate(0,-self.rect.height / 2) # needed to be created with all the objects to collide to

class LongSprite(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-self.rect.width * 0.8,-self.rect.height / 2)
        self.hitbox.bottom = self.rect.bottom - 10