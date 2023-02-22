import sys
sys.path.append("../stuff")
import os
import random
import g2d
import pygame
import actor
from actor import Actor, Arena

##############################################################################

#WARNING: THIS GAME WAS INTENDED TO BE DIFFICULT... PLAY IT AT YOUR OWN RISK...

#...have fun...

##############################################################################

def You_Lose(end_num):
    endings = ["stuff/Mean end.jpg","stuff/Mean end 2.jpg","stuff/Mean end 3.jpg",
                    "stuff/Mean end 4.jpg","stuff/Mean end 5.jpg","stuff/Mean end 6.jpg",
                    "stuff/Mean end 7.jpg","stuff/Mean end 8.jpg","stuff/Mean end 9.jpg",
                    "stuff/Goodest of boys.jpg"]
    return str(endings[end_num])

def Sound(pick):            #to call in-game sound effects
    pygame.init()
    pygame.mixer.init()
    s1 = pygame.mixer.Sound("audio/Life_Up.ogg")
    s2 = pygame.mixer.Sound("audio/SplatFX.ogg")
    s3 = pygame.mixer.Sound("audio/Yee.ogg")
    s4 = pygame.mixer.Sound("audio/Splash.ogg")
    s5 = pygame.mixer.Sound("audio/Swallow.ogg")
    s6 = pygame.mixer.Sound("audio/Coin.ogg")
    if pick == "Life":
        s1.play()
    if pick == "Splat":
        s2.play()
    if pick == "Yee":
        s3.play()
    if pick == "Splash":
        s4.play()
    if pick == "Swallow":
        s5.play()
    if pick == "Coin":
        s6.play()

class Check(Actor):            #to draw those useless purple bars
    def __init__(self, x, y):
        self._x, self._y = x, y
        self._w, self._h = 398, 32
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass
        
    def position(self):
        return self._x, self._y, 640, self._h
        
    def symbol(self):
        return 0, 119, self._w, self._h

class Victory_Lily(Actor):            #to define the victory waterlilies
    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._w, self._h = 30, 31
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 248, 162, 26, 25

class Winning_Frog(Actor):            #to fix a frog on a waterlily
    def __init__(self, arena, x, y, pick):
        self._x, self._y = x, y
        self._w, self._h = 29, 29
        self._pick = pick
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        if self._pick == "frog":
            return 12, 369, 22, 16
        if self._pick == "toad":
            return 272, 380, 23, 19

class Bonus(Actor):            #there is a 1/45 possibility of spawning an extra life
    def __init__(self, arena, x, y, pick):   #I thought it is a quite balanced ratio
        self._x, self._y = x, y
        self._w, self._h = 23, 23
        self._pick = pick
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        if isinstance(other, Frog):
            Sound("Swallow")
            Sound("Life")
            self._x, self._y = 1000, 1000

    def position(self):
        return self._x, self._y, self._w, self._h

    def spawn():
        y_list = [317, 349, 382, 414, 447]
        food = ["apple", "banana", "cherry", "pizza", "watermelon"]
        k = random.randint(0, 45)
        x = random.randint(0, 615)
        y = random.randint(0,4)
        pick = random.randint(0,4)
        if k == 22:
            Bonus(arena, x, y_list[y], food[pick])

    def symbol(self):
        if self._pick == "apple":
            return 286, 163, 18, 20
        if self._pick == "banana":
            return 312, 165, 20, 18
        if self._pick == "cherry":
            return 282, 195, 24, 25
        if self._pick == "pizza":
            return 315, 194, 28, 28
        if self._pick == "watermelon":
            return 345, 167, 26, 26

class Water(Actor):            #it initializes the water... (oh, really?)
    def __init__(self):
        self._x, self._y = 0, 120
        self._w, self._h = 398, 32
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass
        
    def position(self):
        return self._x, self._y, 640, 160
        
    def symbol(self):
        return 0, 517, self._w, self._h

class Raft(Actor):            #the rafts change with different "picks"
    def __init__(self, arena, x, y, dx, pick):
        self._x, self._y = x, y
        self._pick = pick
        self._dx = dx
        self._arena = arena
        self._down = False
        self._counter = 0
        self._time = random.randint(30,33)  #this random number was given to make the turtles descend with different times
        if self._pick == "long":
            self._w, self._h = 178, 20
        elif self._pick == "medium":
            self._w, self._h = 117, 20
        elif self._pick == "short":
            self._w, self._h = 85, 20
        elif self._pick == "turtle":
            self._w, self._h = 35, 22
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        margin, width = arena_w // 4, arena_w * 1.55
        self._x += self._dx
        if self._x < -margin:
            self._x += width
        if self._x >= arena_w + margin:
            self._x -= width

    def collide(self, other):
        pass

    def position(self):
        return self._x, self._y, self._w, self._h

    def speed(self):
        return self._dx

    def turtle_down(self):
        return self._down

    def symbol(self):
        if self._pick == "long":
            return 7, 166, self._w, self._h
        elif self._pick == "medium":
            return 7, 198, self._w, self._h
        elif self._pick == "short":
            return 7, 230, self._w, self._h
        elif self._pick == "turtle":            #this is the turtle animation: it goes down, it waits a bit and then emerges
            while self._counter//4 <= self._time:
                self._counter += 1
                if self._counter//4 == 1 or 15 <= self._counter//4 < self._time:
                    return 15, 408, 30, 21
                if self._counter//4 == 2 or self._counter//4 == 14:
                    return 54, 408, 30, 21
                if self._counter//4 == 3 or self._counter//4 == 13:
                    return 94, 408, 30, 21
                if self._counter//4 == 4 or self._counter//4 == 12:
                    return 134, 408, 30, 21
                if self._counter//4 == 5 or self._counter//4 == 11:
                    self._down = False
                    return 179, 408, 30, 21
                if 5<self._counter//4<11 :
                    self._down = True
                    return 331, 275, 30, 21
                if self._counter//4 == self._time:
                    self._counter=0
    
class Car(Actor):
    def __init__(self, arena, x, y, dx, pick):
        self._x, self._y = x, y
        self._pick = pick
        self._dx = dx
        self._arena = arena
        self._counter = 0
        if self._pick == "RC":
            self._w, self._h = 23, 23
        elif self._pick == "Yellow_RC":  #I preferred repeating this codelines
            self._w, self._h = 23, 23    #in order to make the sprites selection
        elif self._pick == "Truck":      #in "def symbol()" a bit clearer (same thing in Raft class)
            self._w, self._h = 44, 17
        elif self._pick == "Bulldozer":
            self._w, self._h = 22, 20
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        margin, width = arena_w // 4, arena_w * 1.5
        self._x += self._dx
        if self._x < -margin:
            self._x += width
        if self._x >= arena_w + margin:
            self._x -= 2*width

    def collide(self, other):
        pass

    def position(self):
        return self._x, self._y, self._w, self._h

    def speed(self):
        return self._dx

    def symbol(self):
        if self._pick == "RC":
            return 46, 265, self._w, self._h
        elif self._pick == "Yellow_RC":
            return 82, 264, self._w, self._h
        elif self._pick == "Truck":
            return 106, 302, self._w, self._h
        elif self._pick == "Bulldozer":
            if self._counter // 2 == 0:
                self._counter += 1
                return 11, 301, self._w, self._h
            if self._counter // 2== 1:
                self._counter += 1
                return 42, 301, self._w, self._h
            if self._counter // 2 == 2:
                self._counter = 0
                return 73, 301, self._w, self._h
            
class Snake(Actor):            #I chose to create it with a really high speed because, well... it's a snake...
    def __init__(self, arena, x, y):
        self._arena = arena
        self._x, self._y = x, y
        self._w, self._h = 50, 22
        self._counter = 0
        self._dx = -12
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        margin, width = arena_w // 4, arena_w * 4
        self._x += self._dx
        if self._x < -margin:
            self._x += width

    def collide(self, other):
        pass

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        if self._counter//3 == 0:
            self._counter += 1
            return 184, 226, 37, 11
        if self._counter//3 == 1:
            self._counter += 1
            return 185, 251, 36, 14
        if self._counter//3 == 2:
            self._counter += 1
            return 184, 276, 37, 17
        if self._counter//3 == 3:
            self._counter = 0
            return 185, 304, 36, 14

class Frog(Actor):            #and this is the main character, at last...
    def __init__(self, arena, x, y, pick):
        self._x, self._y = x, y
        self._w, self._h = 23, 23
        self._pick = pick
        self._half_x, self._half_y = self._x + 11, self._y + 11
        self._last_x, self._last_y = None, None
        self._splat = False
        self._speed = 8
        self._dx, self._dy = 0, 0
        self._raft = None
        self._count = 0
        self._arena = arena
        self._direction = 1
        self._in_movement = False
        self._die = False
        self._LIVES = 5
        self._winning_frogs = 0
        self._winning_toads = 0
        self._winners = 0
        self._VICTORY = False
        self._random = random.randint(0,9)
        arena.add(self)
        
    def move(self):
        arena_w, arena_h = self._arena.size()
        if self._count > 0:
            self._y += self._dy
            if self._y < 93:
                self._y = 92
            elif self._y > 490:
                self._y = 476

            self._x += self._dx
            if self._x < 0:
                self._x = 0
            elif self._x > arena_w - self._w:
                self._x = arena_w - self._w
            self._count -= 1
        elif self._raft != None:
            self._x += self._raft.speed()
        self._raft = None

                #1:UP - 2:RIGHT - 3:DOWN - 4:LEFT
                    #Their order was determined clockwise
                #I prefer thinking with integers
    
    def go_up(self):
        if self._die == False:
            if self._count == 0:
                Bonus.spawn()
                self._count = 4
                self._dx, self._dy = 0, -self._speed
                self._direction = 1 #UP
                self._in_movement = True
                self._splat = False

    def go_right(self):
        if self._die == False:
            if self._count == 0:
                Bonus.spawn()
                self._count = 4
                self._dx, self._dy = +self._speed, 0
                self._direction = 2 #RIGHT
                self._in_movement = True
                self._splat = False
                if self._raft != None:
                    self._dx, self._dy = abs(self._dx)+self._raft.speed(), 0

    def go_down(self):
        if self._die == False:
            if self._count == 0:
                Bonus.spawn()
                self._count = 4
                self._dx, self._dy = 0, +self._speed
                self._direction = 3 #DOWN
                self._in_movement = True
                self._splat = False

    def go_left(self):
        if self._die == False:
            if self._count == 0:
                Bonus.spawn()
                self._count = 4
                self._dx, self._dy = -self._speed, 0
                self._direction = 4 #LEFT
                self._in_movement = True
                self._splat = False
                if self._raft != None:
                    self._dx, self._dy = -abs(self._dx + self._raft.speed()), 0

    def stay(self):
        self._in_movement = False
        pass
        
    def collide(self, other):            #here is listed every possible collision
        arena_w, arena_h = self._arena.size()
        if isinstance(other, Raft) and self._count == 0:
            xR = other.position()[0]
            wR = other.position()[2]
            turtle_collide = other.turtle_down()
            if xR <= self._x + 11 < xR + wR and turtle_collide == False:
                self._raft = other
            if self._x < 0:
                self._x = 0
            if self._x > arena_w - self._w:
                self._x = arena_w - self._w
        
        if isinstance(other, Water) and self._count == 0 and self._raft == None:
            Sound("Splash")
            self._LIVES -= 1
            if self._pick == "frog":
                self._x, self._y = 348, 476
            if self._pick == "toad":
                self._x, self._y = 316, 476
            self._direction = 1
            self._dx, self._dy = 0, 0
            if self._LIVES == 0:
                self._die = True

        if isinstance(other, Winning_Frog):
            self._LIVES -= 1
            if self._pick == "frog":
                self._x, self._y = 348, 476
            if self._pick == "toad":
                self._x, self._y = 316, 476
            self._direction = 1
            self._dx, self._dy = 0, 0
            if self._LIVES  == 0:
                self._die = True

        if isinstance(other, Victory_Lily) and self._count == 0:
            xW = other.position()[0]
            yW = other.position()[1]
            if self._pick == "frog" and not isinstance(other, Winning_Frog):
                Winning_Frog(arena, xW, yW, "frog")
                self._winning_frogs += 1
                self._x, self._y = 348, 476
                Sound("Yee")
            if self._pick == "toad" and not isinstance(other, Winning_Frog):
                Winning_Frog(arena, xW, yW, "toad")
                self._winning_toads += 1
                self._x, self._y = 316, 476
                Sound("Yee")

        if isinstance(other, Bonus):    #I limited the number of lives to 7
            if self._LIVES < 7:
                self._LIVES += 1
            
        if isinstance(other, Snake):
            self._LIVES -= 1
            if self._pick == "frog":
                self._x, self._y = 348, 476
            if self._pick == "toad":
                self._x, self._y = 316, 476
            self._direction = 1
            self._dx, self._dy = 0, 0
            if self._LIVES  == 0:
                self._die = True
        
        if isinstance(other, Car):
            self._LIVES -= 1
            self._splat = True
            self._last_x, self._last_y = self._x, self._y
            if self._pick == "frog":
                self._x, self._y = 348, 476
            if self._pick == "toad":
                self._x, self._y = 316, 476
            self._direction = 1
            self._dx, self._dy = 0, 0
            Sound("Splat")
            if self._LIVES == 0:
                self._die = True
               
    def position(self):
        return self._x, self._y, self._w, self._h

    def death(self):
        return self._die

    def splat(self):
        return self._splat, self._last_x, self._last_y

    def lives_counter(self):
        return self._LIVES

    def VICTORY(self):
        if self._winning_frogs == 3 or self._winning_toads == 3:
            self._VICTORY = True
        return self._VICTORY, self._winning_frogs, self._winning_toads

    def ending_screen(self):
        return self._random
        
    def symbol(self):
        if self._pick == "frog":
            if not self._in_movement:
                if self._direction == 1:
                    return 12, 369, 22, 16
                if self._direction == 2:
                    return 13, 334, 16, 22
                if self._direction == 3:
                    return 80, 369, 22, 16
                if self._direction == 4:
                    return 82, 335, 16, 22
                
            if self._in_movement:
                if self._direction == 1:
                    return 46, 366, 21, 24
                if self._direction == 2:
                    return 43, 335, 24, 21
                if self._direction == 3:
                    return 114, 366, 21, 24
                if self._direction == 4:
                    return 112, 338, 24, 21
                
        if self._pick == "toad":
            if not self._in_movement:
                if self._direction == 1:
                    return 272, 380, 23, 19
                if self._direction == 2:
                    return 236, 407, 19, 23
                if self._direction == 3:
                    return 315, 340, 23, 19
                if self._direction == 4:
                    return 315, 407, 19, 23
                
            if self._in_movement:
                if self._direction == 1:
                    return 274, 339, 23, 26
                if self._direction == 2:
                    return 270, 409, 26, 23
                if self._direction == 3:
                    return 314, 374, 26, 23
                if self._direction == 4:
                    return 348, 409, 23, 26
            
##################

arena = Arena(640, 560)

def create_rafts():            #this method creates random rafts
    variant = ["long", "medium", "short", "turtle"]
    lenghts = [178, 117, 85, 35]
    y = [129,160,191,222,252]
    for i in range(0,5):
        x=0
        speed = random.randint(1,2)
        if i==1 or i==3:
            speed = -speed
            for t in range(3):
                for q in range(3):
                    x += lenghts[3]
                    raft = Raft(arena, x , y[i], speed, variant[3])
                x += lenghts[3] + random.randint(150, 200)
        else:
            for t in range(0,3):
                selection = random.randint(0,2)
                x += lenghts[selection] + random.randint(150, 200)
                raft = Raft(arena, x , y[i], speed, variant[selection])

def create_cars():            #and this creates random cars instead
    variant = ["RC", "Yellow_RC", "Truck", "Bulldozer"]
    lenghts = [23, 23, 44, 22]
    y = [317, 349, 382, 414, 447]
    for i in range(0,5):
        x = 0
        selection = random.randint(0,3)
        if selection == 0 or selection == 3:
            speed = random.randint(1,2)
        else:
            speed = random.randint(-2,-1)
        for t in range(5):
            x += lenghts[selection] + random.randint(120,150)
            car = Car(arena, x , y[i], speed, variant[selection])

Water()            #here Actors are initialized
Check(0, 280)
Check(0, 471)
create_rafts()
create_cars()
for i in range(49,562, 128):
    Victory_Lily(arena, i, 88)
Snake(arena, -30, 285)
frog = Frog(arena, 348, 476, "frog")            #I called them "frog" and "toad" to simplify the code
toad = Frog(arena, 316, 476, "toad")
sprites = g2d.load_image("stuff/frogger_sprites.png")

def update():
    arena.move_all()
    background = g2d.load_image("stuff/frogger_bg.png")
    
    death_frog = frog.death()
    frog_check_splat = frog.splat()[0]
    frog_splat_x, frog_splat_y = frog.splat()[1], frog.splat()[2]
    lives_number_frog = frog.lives_counter()
    frog_splat_sprite = g2d.load_image("stuff/frog_splat_sprite.png")

    death_toad = toad.death()
    toad_check_splat = toad.splat()[0]
    toad_splat_x, toad_splat_y = toad.splat()[1], toad.splat()[2]
    lives_number_toad = toad.lives_counter()
    toad_splat_sprite = g2d.load_image("stuff/toad_splat_sprite.png")

    VICTORY_1 = frog.VICTORY()[0]
    VICTORY_2 = toad.VICTORY()[0]

    P1 = str(frog.VICTORY()[1])
    P2 = str(toad.VICTORY()[2])

    ending_screen = frog.ending_screen()
  
    if not death_frog and not death_toad:
        g2d.fill_canvas((0, 0, 0))
        lives_frog_image = g2d.load_image("stuff/frog_lives.png")
        lives_toad_image = g2d.load_image("stuff/toad_lives.png")
        g2d.draw_image(background, (0,40))
        
        k = 0
        for i in range(lives_number_frog - 1):
            g2d.draw_image(lives_frog_image,(600 - k, 525))
            k += 28
            
        k = 0
        for i in range(lives_number_toad - 1):
            g2d.draw_image(lives_toad_image,(17 + k, 525))
            k += 28

        if frog_check_splat:
            g2d.draw_image(frog_splat_sprite, (frog_splat_x, frog_splat_y))

        if toad_check_splat:
            g2d.draw_image(toad_splat_sprite, (toad_splat_x, toad_splat_y))
            
        for a in arena.actors():
            g2d.draw_image_clip(sprites, a.position(), a.symbol())

        if VICTORY_1:
            pygame.mixer.music.stop()
            pygame.time.wait(2000)
            Win = g2d.load_image("stuff/Frog Win.jpg")
            g2d.draw_image(Win, (0,0))
        if VICTORY_2:
            pygame.mixer.music.stop()
            pygame.time.wait(2000)
            Win = g2d.load_image("stuff/Toad Win.jpg")
            g2d.draw_image(Win, (0,0))

        if not VICTORY_1 and not VICTORY_2:
            txt_1 = "Frog:   " + P1
            txt_2 = "Toad:   " + P2
            g2d.draw_text_centered(txt_1, (255, 255, 255), (100, 30), 50)
            g2d.draw_text_centered(txt_2, (255, 255, 255), (540, 30), 50)
            g2d.draw_text_centered("< Lives >", (255, 255, 255), (320, 535), 30)

    if death_frog or death_toad:
        pygame.mixer.music.stop()
        ending = You_Lose(ending_screen)    #to draw a random surprise ending
        game_over = g2d.load_image(ending)
        pygame.time.wait(1000)
        g2d.fill_canvas((0,0,0))
        g2d.draw_image(game_over, (0,0))
        
def keydown(code):
    if code == "ArrowUp":
        frog.go_up()
    elif code == "ArrowDown":
        frog.go_down()
    elif code == "ArrowLeft":
        frog.go_left()
    elif code == "ArrowRight":
        frog.go_right()
        
    if code == "KeyW":
        toad.go_up()
    elif code == "KeyS":
        toad.go_down()
    elif code == "KeyA":
        toad.go_left()
    elif code == "KeyD":
        toad.go_right()
    
def keyup(code):
    if code == "ArrowUp":
        frog.stay()
    elif code == "ArrowDown":
        frog.stay()
    elif code == "ArrowLeft":
        frog.stay()
    elif code == "ArrowRight":
        frog.stay()
        
    if code == "KeyW":
        toad.stay()
    elif code == "KeyS":
        toad.stay()
    elif code == "KeyA":
        toad.stay()
    elif code == "KeyD":
        toad.stay()

def main():
    xWINDOW, yWINDOW = 560, 200         #these set the window position
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xWINDOW, yWINDOW)
    
    pygame.mixer.init()
    x, y = 247, 324
    g2d.init_canvas((x, y))
    test = g2d.load_image("stuff/Insert coin.png")
    g2d.draw_image(test, (0,0))
    coin = False
    while not coin:
        g2d.update_canvas()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if test.get_rect().collidepoint(x, y):
                    Sound("Coin")
                    coin = True

    xWINDOW, yWINDOW = 363, 104         #and these set the window position too
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xWINDOW, yWINDOW)
    
    pygame.time.wait(1500)
    g2d.init_canvas(arena.size())
    instructions = g2d.load_image("stuff/Starting Screen.jpg")
    g2d.draw_image(instructions, (0,0))
    g2d.handle_keyboard(keydown, keyup)
    
    menu = True
    while menu:            #this cycle initializes different soundtracks with a user-prompt
        g2d.update_canvas()
        pygame.mixer.music.load("audio/Start Menu.mp3")
        pygame.mixer.music.play(-1)
        music = g2d.prompt("""

    Choose a soundtrack (insert the number):\n\n

    1) Enraging - To raise your fighting spirit\n
    2) Enjoyable - To enjoy your experience\n
    3) Relaxing - To calm down your nerves...\n
    \t...seriously, calm down\n
    4) No Music - Because you're a bad person

    """)

        if music == "1":
            pygame.mixer.music.load("audio/Tension.mp3")
            pygame.mixer.music.play(-1)
            confirm = g2d.prompt("""
#############################
#############################
#############################
#############################
#############################
#############################

######Are you sure about that??####
##########      <y/n>          #######

#############################
#############################
#############################""")
            if confirm == "y" or confirm == "yes" or confirm == "Yes":
                pygame.mixer.music.stop()
                pygame.mixer.music.load("audio/Enraging.mp3")
                menu = False
        if music == "2":
            pygame.mixer.music.load("audio/Enjoyable.mp3")
            menu = False
        if music == "3":
            pygame.mixer.music.load("audio/Relaxing.mp3")
            menu = False
        if music == "4":
            pygame.mixer.music.stop()
            menu = False
        if music == None:
            g2d.exit()
        
    g2d.fill_canvas((0,0,0))
    g2d.update_canvas()
    pygame.time.wait(500)
    if music != "4":
        pygame.mixer.music.play(-1)
    g2d.main_loop(update, 1000 // 60)

main()

##Credits:
##
##   Music by Toby Fox: Undertale, Megaman and Kirby
##
##Special Thanks To:
##
##  - Tomamic, who taught me Python programming
##
##  - Zonto, who inspired me with some hilarious stuff
##
##   ...and to everyone who cheered on me!
##
## _______  __   __  _______    _______  __    _  ______  
##|       ||  | |  ||       |  |       ||  |  | ||      | 
##|_     _||  |_|  ||    ___|  |    ___||   |_| ||  _    |
##  |   |  |       ||   |___   |   |___ |       || | |   |
##  |   |  |   _   ||    ___|  |    ___||  _    || |_|   |
##  |   |  |  | |  ||   |___   |   |___ | | |   ||       |
##  |___|  |__| |__||_______|  |_______||_|  |__||______| 
