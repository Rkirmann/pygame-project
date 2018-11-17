"""
kasutatud näidise peale ehitatud

Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

From:
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py

Explanation video: http://youtu.be/QplXBw_NK5Y

Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
kasutatud näidis - http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py - kasutatud näidis
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/

"""

import pygame
import random
import copy
import math
# Global constants
skoor= 0
astmeid = 4
tase = 1
myntejaanud = -1
save = 1
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800



class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """
    paremale = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
                     pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
                     pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
    vasakule = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
                pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
                pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
    # animatsiooni muutuja
    loesamm = 0


    # -- Methods
    def __init__(self):
        """ Constructor function """


        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.



        self.image = pygame.image.load('standing.png')


        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None


    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        for block in block_hit_list:

            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left

            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        #korja mynte
        mynt_hit_list = pygame.sprite.spritecollide(self, self.level.mynt_list, True)
        global skoor
        global myntejaanud
        for block2 in mynt_hit_list:
            skoor += 1
            myntejaanud -= 1
            print(myntejaanud)


        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        #korja mynte
        mynt_hit_list = pygame.sprite.spritecollide(self, self.level.mynt_list, True)
        for block2 in mynt_hit_list:
            skoor += 1
            myntejaanud -= 1
            print(myntejaanud)

        # animeeri
        if self.change_x > 0:
            if self.loesamm < 9:
                self.image = self.paremale[self.loesamm]
                self.loesamm += 1
            else:
                self.loesamm = 0

        elif self.change_x < 0:

            if self.loesamm < 9:
                self.image = self.vasakule[self.loesamm]
                self.loesamm += 1
            else:
                self.loesamm = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:



    def go_left(self):
        """ Called when the user hits the left arrow. """

        self.change_x = -6


    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):

        """ Called when the user lets off the keyboard. """
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()

        self.image = pygame.image.load('plat1.png')


        self.rect = self.image.get_rect()

class Mynt(pygame.sprite.Sprite):
    """ myndid"""

    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.image.load('standing3.png')


        self.rect = self.image.get_rect()
class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.mynt_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # How far this world has been scrolled left/right
        self.world_shift = 0

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.mynt_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.mynt_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for mynt in self.mynt_list:
            mynt.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

    def shift_worldy(self, shift_y):
        """ scrolli y suunas """

        self.world_shift += shift_y

        for platform in self.platform_list:
            platform.rect.y += shift_y

        for mynt in self.mynt_list:
            mynt.rect.y += shift_y

        for enemy in self.enemy_list:
            enemy.rect.y += shift_y

class Level_00(Level):
    """ Definition for level 0. """
    global myntejaanud
    def __init__(self, player):
        """ Create level 0. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000
        myntejaanud = -1


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
    global myntejaanud
    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -3000

        #geneb automaatselt levelid
        level = []
        platformid = 0
        x = 250
        y = 800
        a = [210, 70, 250, 800]
        global astmeid
        global myntejaanud

        while platformid < astmeid:
            if platformid == 0:
                level.append(a)
            else:
                x += random.choice([-250,250])
                y += random.choice([-150,150])
                level.append([210,70,x,y])
            platformid += 1

        #genereerib myndid juhuslikult
        self.myndid = []
        for i in level:
            if level.index(i) != 0:
                myndid_choice = random.choice([1, 1, 0])
                if myndid_choice == 1:
                    a = copy.deepcopy(level[level.index(i)])
                    self.myndid.append(a)
                    a[3] -= 50
                    a[2] += 40
        myntejaanud = len(self.myndid)


        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        #lisa myndid
        for mynt in self.myndid:
            block2 = Mynt(mynt[0], mynt[1])
            block2.rect.x = mynt[2]
            block2.rect.y = mynt[3]
            block2.player = self.player
            self.mynt_list.add(block2)

# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("meie mäng")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(Level_00(player))
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))

    # Set the current level
    current_level_no = 1
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    #kell
    text2 = 'Skoor: '
    text3 = 'Level: '
    counter, text = 30, 'Aega jäänud: 30'
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)

    #globalid
    global skoor
    global tase
    global astmeid
    global myntejaanud
    global save

    # -------- Main Program Loop -----------
    while not done:


        for event in pygame.event.get():
            # kell
            text2 = 'Skoor: ' + str(skoor) if 0 < 1 else 'next level!'
            text3 = 'Level: ' + str(tase) #if 0 < 1 else 'next level!'
            if event.type == pygame.USEREVENT:

                counter -= 1
                text = 'Aega jäänud: '+ str(counter) if counter > 0 else 'Aeg läbi!'

            if counter == 0:
                # savi skoor
                if save == 1:
                    toplevel = tase
                    topskoor = skoor
                    with open('topskoor.txt') as f:
                        f = f.read().split(" ")
                    if int(f[2]) < topskoor:
                        fail = open('topskoor.txt', 'w')
                        print('topskoor', toplevel, topskoor)
                        top = 'Top skoor: ' + str(topskoor) + ' level: ' + str(toplevel)
                        fail.write(top)
                        fail.close()
                    save = 0
                tase = 1
                astmeid = 4
                skoor = 0
                current_level_no = 0
                current_level = level_list[current_level_no]
                player.level = current_level

            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    #takistab hüpates liikumist
                    if player.change_y == 0:
                        player.go_left()
                if event.key == pygame.K_RIGHT:
                    if player.change_y == 0:
                        player.go_right()
                if event.key == pygame.K_UP:
                    #hüppab ainult ühes suunas
                    if player.change_x == 6:
                        player.jump()
                        player.go_right()
                    if player.change_x == -6:
                        player.jump()
                        player.go_left()
                    else:
                        player.jump()
                if event.key == pygame.K_r:
                    #takistab hüpates liikumist
                    skoor = 0
                    tase = 1
                    astmeid = 4
                    save = 1
                    main()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 700:
            diffx = player.rect.right - 700
            player.rect.right = 700
            current_level.shift_world(-diffx)
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diffx = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diffx)
        # scrolli y suunas
        if player.rect.top >= 120:
            diffy = player.rect.top - 120
            player.rect.top = 120
            current_level.shift_worldy(-diffy)
        if player.rect.bottom <= 500:
            diffy = 500 - player.rect.bottom
            player.rect.bottom = 500
            current_level.shift_worldy(diffy)


        # kui üle piiri läheb, alustab uuesti
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120

            if current_level_no < len(level_list) - 1:
                # level 0
                #savi skoor
                if save == 1:
                    toplevel = tase
                    topskoor = skoor
                    with open('topskoor.txt') as f:
                        f = f.read().split(" ")
                    if int(f[2]) < topskoor:
                        fail = open('topskoor.txt', 'w')
                        print('topskoor', toplevel, topskoor)
                        top = 'Top skoor: ' + str(topskoor) + ' level: ' + str(toplevel)
                        fail.write(top)
                        fail.close()
                    save = 0
                tase = 1
                astmeid = 4
                skoor = 0
                current_level_no =0
                current_level = level_list[current_level_no]
                player.level = current_level

        #uus level
        if myntejaanud == 0:
            astmeid += 1
            tase +=1
            main()


        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        if current_level_no != 0:
            screen.blit(font.render(text, True, (0, 0, 0)), (32, 48)) #kell
            screen.blit(font.render(text2, True, (0, 0, 0)), (400, 48))  # skoor
            screen.blit(font.render(text3, True, (0, 0, 0)), (600, 48))  # level
        #kirjuta/näita top skoori
        if current_level_no == 0:
            screen.blit(font.render('Mäng läbi! Vajuta "R"', True, (0, 0, 0)), (200, 400))  # ded
            with open('topskoor.txt') as fail:
                fail = fail.read()
            screen.blit(font.render(fail, True, (0, 0, 0)), (200, 300))  # top
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == "__main__":
    main()