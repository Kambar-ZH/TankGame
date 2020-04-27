#Открываем библиотеки
import pygame
import math
import random
from images import *
from some_music import *

# Keys for tank1: movement - K_LEFT, K_RIGHT, K_UP, K_DOWN
#                 rotating barrel - K_k, K_l
#                 shooting - K_j

# Keys for tank2: movement - K_a, K_d, K_w, K_s
#                 rotating barrel - K_f, K_g
#                 shooting - K_SPACE
# Базовая сцена
class SceneBase:
    #Инициализация сцены
    def __init__(self):
        self.next = self
    #Обработка введенных данных
    def ProcessInput(self, events, pressed_keys, position_mouse):
        print("uh-oh, you didn't override this in the child class")
    #Реакция
    def Update(self, seconds):
        print("uh-oh, you didn't override this in the child class")
    #Отрисовка
    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")
    #Переход на новую сцену
    def SwitchToScene(self, next_scene):
        self.next = next_scene
    #Завершение программы
    def Terminate(self):
        self.SwitchToScene(None)
#Основная функция
def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height), 0, 0)

    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene != None:
        ms = clock.tick(fps)
        pygame.display.set_caption("Time: " + str(pygame.time.get_ticks() / 1000))
        seconds = ms / 1000

        pressed_keys = pygame.key.get_pressed()

        position_mouse = pygame.mouse.get_pos()
        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True

            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            
            if quit_attempt:
                active_scene.Terminate()
                
            else:
                filtered_events.append(event)

        active_scene.ProcessInput(filtered_events, pressed_keys, position_mouse)
        active_scene.Update(seconds)
        active_scene.Render(screen)
        
        active_scene = active_scene.next

        pygame.display.flip()
        

# The rest is code where you implement your game using the Scenes model

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.x = 100
        self.y1 = 200
        self.y2 = 300
        self.y3 = 400
        self.easterX = 300
        self.easterY = 300
        self.eastereggs = False
        self.rect_x = self.x - 10
        self.rect_y = self.y1
        self.choose_option = 1
    
    def ProcessInput(self, events, pressed_keys, position_mouse):
        for event in events:
            if ((position_mouse[0] > self.x and position_mouse[0] < self.x + 300) and (position_mouse[1] > self.y1 and position_mouse[1] < self.y1 + 50)):
                self.rect_y = self.y1
            elif ((position_mouse[0] > self.x and position_mouse[0] < self.x + 300) and (position_mouse[1] > self.y2 and position_mouse[1] < self.y2 + 50)):
                self.rect_y = self.y2
            elif ((position_mouse[0] > self.x and position_mouse[0] < self.x + 300) and (position_mouse[1] > self.y3 and position_mouse[1] < self.y3 + 50)):
                self.rect_y = self.y3

            if self.rect_y == self.y1 and ((event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN):
                self.SwitchToScene(GameSceneSingle())
            elif self.rect_y == self.easterY and ((event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) and self.eastereggs == True):
                soundTreck.play()
                self.SwitchToScene(DeveloperScene())
            elif self.rect_y == self.y2 and ((event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN):
                self.SwitchToScene(GameSceneMultiple())
            elif self.rect_y == self.y3 and ((event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN):
                self.SwitchToScene(None)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.eastereggs = True
                self.choose_option = 4
                self.ChooseOption()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.eastereggs = False
                self.choose_option = 2
                self.ChooseOption()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if self.choose_option > 1 and self.choose_option <= 3:
                    self.choose_option -= 1
                    self.ChooseOption()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if self.choose_option >= 1 and self.choose_option < 3:
                    self.choose_option += 1
                    self.ChooseOption()

    def ChooseOption(self):
        if self.choose_option == 1:
            self.rect_y = self.y1
            self.rect_x = self.x - 10
        elif self.choose_option == 2:
            self.rect_y = self.y2
            self.rect_x = self.x - 10
        elif self.choose_option == 3:
            self.rect_y = self.y3
            self.rect_x = self.x - 10
        elif self.choose_option == 4:
            self.rect_y = self.easterY
            self.rect_x = self.easterX
    def Update(self, seconds):
        pass
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (self.rect_x, self.rect_y, 300, 50), 10)
        font = pygame.font.SysFont('impact', 40)
        text = font.render('World of Tanks', 1, (65, 110, 220))
        screen.blit(text, (self.x, 100))

        font = pygame.font.SysFont('impact', 36)
        text1 = font.render('Singleplayer', 1, (255, 255, 255))
        screen.blit(text1, (self.x, self.y1))

        text2 = font.render('Multiplayer', 1, (255, 255, 255))
        screen.blit(text2, (self.x, self.y2))

        text3 = font.render('Quit the game', 1, (255, 255, 255))
        screen.blit(text3, (self.x, self.y3))
        if self.eastereggs == True:
            text4 = font.render('Easter Egg', 1, (65, 110, 220))
            screen.blit(text4, (self.easterX + 10, self.easterY))

class DeveloperScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.x = 300
        self.y = 500
        self.color = (255, 255, 255)
        self.color1 = (65, 110, 220)
        self.color2 = (100, 230, 15)

    def ProcessInput(self, events, pressed_keys, position_mouse):
        for event in events:
            if ((position_mouse[0] > 0 and position_mouse[0] < 1000) and (position_mouse[1] > 0 and position_mouse[1] < 600)):
                self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                self.color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                self.color2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                soundTreck.stop()
                self.SwitchToScene(TitleScene())
            
    def Update(self, seconds):
        pass
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, self.color, (self.x - 35, self.y, 450, 50), 10)
        font = pygame.font.SysFont('impact', 40)
        text = font.render('Thank You For Playing !', 1, self.color1)
        screen.blit(text, (self.x, self.y))
        text1 = font.render('Made by <Kambar Zhamauov>', 1, self.color2)
        screen.blit(text1, (250, 200))

class PauseScene(SceneBase):
    def __init__(self, parameter):
        SceneBase.__init__(self)
        self.parameter = parameter
        self.x = 100
        self.y1 = 200
        self.y2 = 300
        self.y3 = 400
        self.pauseY = 100
        self.rect_x = self.x - 10
        self.rect_y = self.y1
        self.choose_option = 1
    
    def ProcessInput(self, events, pressed_keys, position_mouse):
        for event in events:
            if ((position_mouse[0] > self.x and position_mouse[0] < self.x + 400) and (position_mouse[1] > self.y1 and position_mouse[1] < self.y1 + 50)):
                self.rect_y = self.y1
            elif ((position_mouse[0] > self.x and position_mouse[0] < self.x + 400) and (position_mouse[1] > self.y2 and position_mouse[1] < self.y2 + 50)):
                self.rect_y = self.y2
            elif ((position_mouse[0] > self.x and position_mouse[0] < self.x + 400) and (position_mouse[1] > self.y3 and position_mouse[1] < self.y3 + 50)):
                self.rect_y = self.y3

            if self.rect_y == self.y1 and ((event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN):
                if self.parameter == 1:
                    self.SwitchToScene(GameSceneSingle())
                else:
                    self.SwitchToScene(GameSceneMultiple())
            elif self.rect_y == self.y2 and ((event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN):
                self.SwitchToScene(TitleScene())
            elif self.rect_y == self.y3 and ((event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN):
                self.SwitchToScene(None)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if self.choose_option > 1 and self.choose_option <= 3:
                    self.choose_option -= 1
                    self.ChooseOption()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if self.choose_option >= 1 and self.choose_option < 3:
                    self.choose_option += 1
                    self.ChooseOption()

    def ChooseOption(self):
        if self.choose_option == 1:
            self.rect_y = self.y1
        elif self.choose_option == 2:
            self.rect_y = self.y2
        elif self.choose_option == 3:
            self.rect_y = self.y3

    def Update(self, seconds):
        pass
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (self.rect_x, self.rect_y, 400, 50), 10)

        font = pygame.font.SysFont('impact', 40)
        text = font.render('Pause', 1, (65, 110, 220))
        screen.blit(text, (self.x, self.pauseY))

        font = pygame.font.SysFont('impact', 36)
        text1 = font.render('Continue', 1, (255, 255, 255))
        screen.blit(text1, (self.x, self.y1))

        text2 = font.render('Back to main menu', 1, (255, 255, 255))
        screen.blit(text2, (self.x, self.y2))

        text3 = font.render('Quit the game?', 1, (255, 255, 255))
        screen.blit(text3, (self.x, self.y3))

class EndScene(SceneBase):
    def __init__(self, ending):
        SceneBase.__init__(self)
        self.x = 100
        self.y1 = 100
        self.y2 = 200
        self.y3 = 300
        self.ending = ending
        self.rect_x = self.x - 10
        self.rect_y = self.y2
        self.choose_option = 1
    
    def ProcessInput(self, events, pressed_keys, position_mouse):
        for event in events:
            if ((position_mouse[0] > self.x and position_mouse[0] < self.x + 400) and (position_mouse[1] > self.y2 and position_mouse[1] < self.y2 + 50)):
                self.rect_y = self.y2
            elif ((position_mouse[0] > self.x and position_mouse[0] < self.x + 400) and (position_mouse[1] > self.y3 and position_mouse[1] < self.y3 + 50)):
                self.rect_y = self.y3

            if self.rect_y == self.y2 and ((event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN):
                self.SwitchToScene(TitleScene())
            elif self.rect_y == self.y3 and ((event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN):
                self.SwitchToScene(None)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if self.choose_option > 1 and self.choose_option <= 2:
                    self.choose_option -= 1
                    self.ChooseOption()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if self.choose_option >= 1 and self.choose_option < 2:
                    self.choose_option += 1
                    self.ChooseOption()

    def ChooseOption(self):
        if self.choose_option == 1:
            self.rect_y = self.y2
        elif self.choose_option == 2:
            self.rect_y = self.y3

    def Update(self, seconds):
        pass
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (self.rect_x, self.rect_y, 400, 50), 10)

        font = pygame.font.SysFont('impact', 45)
        if self.ending == 0:
            text1 = font.render('You Lose !', 1, (65, 110, 220))
        elif self.ending == 1:
            text1 = font.render('You Win !!!', 1, (65, 110, 220))
        elif self.ending == 2:
            text1 = font.render('P2 wins !!!', 1, (65, 110, 220))
        elif self.ending == 3:
            text1 = font.render('P1 Wins !!!', 1, (65, 110, 220))
        screen.blit(text1, (self.x, self.y1))
    
        font = pygame.font.SysFont('impact', 40)
        text2 = font.render('Back to main menu', 1, (255, 255, 255))
        screen.blit(text2, (self.x, self.y2))

        text3 = font.render('Quit the game?', 1, (255, 255, 255))
        screen.blit(text3, (self.x, self.y3))

class Tank:
    def __init__(self, originX, originY, width, height, speed):
        self.originX = originX
        self.originY = originY
        self.width = width
        self.height = height
        self.dtype = 1
        self.direction = 1
        self.speed = speed
        self.shootloop = 0
        self.explosion_count = 0
        self.drown = False
        self.drowning_count = 0
        self.seconds = 0
        self.shift_pressed = 0
        self.bullets = []
        self.barrel = Barrel(self.originX + self.width / 2, self.originY + self.height / 2)
        self.lives = 3
        #direction 1 - up, 2 - right, 3 - down, 4 - left, 
    
    def ChangeDirection(self, direction):
        self.direction = direction
         
    def ChangeLocation(self, pressed_keys):
        if self.shift_pressed % 2 == False:
            if pressed_keys[pygame.K_UP]: 
                self.originY -= self.speed
                self.ChangeDirection(1)
            elif pressed_keys[pygame.K_RIGHT]: 
                self.originX += self.speed
                self.ChangeDirection(2)
            elif pressed_keys[pygame.K_DOWN]:
                self.originY += self.speed
                self.ChangeDirection(3)
            elif pressed_keys[pygame.K_LEFT]:
                self.originX -= self.speed
                self.ChangeDirection(4) 

        if self.shift_pressed % 2 == True:
            if pressed_keys[pygame.K_UP]: 
                self.ChangeDirection(1)
            elif pressed_keys[pygame.K_RIGHT]: 
                self.ChangeDirection(2)
            elif pressed_keys[pygame.K_DOWN]:
                self.ChangeDirection(3)
            elif pressed_keys[pygame.K_LEFT]:
                self.ChangeDirection(4) 

            if self.direction == 1:
                self.originY -= self.speed
            if self.direction == 2: 
                self.originX += self.speed
            if self.direction == 3:
                self.originY += self.speed
            if self.direction == 4:
                self.originX -= self.speed
        self.InfiniteScene()

    # It's if you want an infinite scene
    def InfiniteScene(self):
        if self.originY - self.height < 0:
            self.originY = self.originY % 600
        if self.originY + self.height> 600:
            self.originY = self.originY % 600
        if self.originX - self.width < 0:
            self.originX = self.originX % 1000
        if self.originX + self.width> 1000:
            self.originX = self.originX % 1000

    # If you need to get the parameters
    def GetRectangle(self):
        get_rect = (self.originX, self.originY, self.width, self.height)
        return get_rect

    def Render(self, screen):
        if self.direction == 1:
            screen.blit(walkUp, (self.originX, self.originY))
        elif self.direction == 2:
            screen.blit(walkRight, (self.originX, self.originY))
        elif self.direction == 3:
            screen.blit(walkDown, (self.originX, self.originY))
        elif self.direction == 4:
            screen.blit(walkLeft, (self.originX, self.originY))

    def Shoot(self, angle):
        if self.shootloop == 0:
            self.bullets.append(Bullet(self.originX, self.originY, self.dtype, 5, angle))

    def ShootLoop(self, seconds):
        if pygame.time.get_ticks() > self.seconds + 500:
            self.shootloop = 0

    def TerminateBullets(self):
        for bullet in self.bullets:
            # Terminate all bullets that out of walls
            if bullet.originX < 0:
                self.bullets.pop(self.bullets.index(bullet))
            if bullet.originX > 1000:
                self.bullets.pop(self.bullets.index(bullet))
            if bullet.originY < 0:
                self.bullets.pop(self.bullets.index(bullet))
            if bullet.originY > 600:
                self.bullets.pop(self.bullets.index(bullet))

class Turrets:
    def __init__(self):
        self.originX = random.randint(100, 900)
        self.originY = random.randint(100, 500)
        self.radius = 25
        self.angle = 0
        self.shootloop = 0
        self.reload = random.randint(2000, 3500)
        self.seconds = 0
        self.barrel = Barrel(self.originX, self.originY)
        self.bullets = []

    def Render(self, screen):
        font = pygame.font.SysFont('impact', 20)
        text = font.render('Turret', 1, (255, 255, 255))
        screen.blit(text, (self.originX - 15, self.originY - 55))
        screen.blit(walkRight, (self.originX - 25, self.originY - 25))

    def ChangeDirection(self, originX, originY):
        try:
            if self.originX > originX:
                self.angle = math.atan((self.originY - originY) / (originX - self.originX)) - math.pi
            else:
                self.angle = math.atan((self.originY - originY) / (originX - self.originX))
        
        except ZeroDivisionError:
            pass

    def Shoot(self, angle):
        if self.shootloop == 0:
            self.bullets.append(Bullet(self.originX - self.radius, self.originY - self.radius, 1, 5, 180 * angle / math.pi - 90))
    
    def ShootLoop(self, seconds):
        if pygame.time.get_ticks() > self.seconds + self.reload:
            self.shootloop = 0

    def TerminateBullets(self):
        for bullet in self.bullets:
            # Terminate all bullets that out of walls
            try:
                if bullet.originX < 0:
                    self.bullets.pop(self.bullets.index(bullet))
                if bullet.originX > 1000:
                    self.bullets.pop(self.bullets.index(bullet))
                if bullet.originY < 0:
                    self.bullets.pop(self.bullets.index(bullet))
                if bullet.originY > 600:
                    self.bullets.pop(self.bullets.index(bullet))

            except ValueError:
                pass

class Tank2(Tank):
    def __init__(self, originX, originY, width, height, speed):
        super().__init__(originX, originY, width, height, speed)

    def ChangeLocation(self, pressed_keys):
        if self.shift_pressed % 2 == False:
            if pressed_keys[pygame.K_w]: 
                self.originY -= self.speed
                self.ChangeDirection(1)
            elif pressed_keys[pygame.K_d]: 
                self.originX += self.speed
                self.ChangeDirection(2)
            elif pressed_keys[pygame.K_s]:
                self.originY += self.speed
                self.ChangeDirection(3)
            elif pressed_keys[pygame.K_a]:
                self.originX -= self.speed
                self.ChangeDirection(4) 

        if self.shift_pressed % 2 == True:
            if pressed_keys[pygame.K_w]: 
                self.ChangeDirection(1)
            elif pressed_keys[pygame.K_d]: 
                self.ChangeDirection(2)
            elif pressed_keys[pygame.K_s]:
                self.ChangeDirection(3)
            elif pressed_keys[pygame.K_a]:
                self.ChangeDirection(4) 

            if self.direction == 1:
                self.originY -= self.speed
            if self.direction == 2: 
                self.originX += self.speed
            if self.direction == 3:
                self.originY += self.speed
            if self.direction == 4:
                self.originX -= self.speed
        self.InfiniteScene()

class PowerUp:
    def __init__(self, originX, originY):
        self.originX = originX
        self.originY = originY
        self.width = 60
        self.height = 60
        self.use = False
    def Render(self, screen):
        if self.use == False:
            screen.blit(winPoint, (self.originX, self.originY))
    def Consume(self, originX, originY, width, height):
        if (originX > self.originX and originX < self.originX + self.width) or (originX + width > self.originX and originX + width < self.originX + self.width):
            if (originY > self.originY and originY < self.originY + self.height) or (originY + height > self.originY and originY + height < self.originY + self.height):
                self.use = True
                return True

class Water(PowerUp):
    def __init__(self, originX, originY):
        super().__init__(originX, originY)
        self.originX = originX
        self.originY = originY
        self.width = 64
        self.height = 64
    def Render(self, screen):
        screen.blit(water, (self.originX, self.originY))
    def Consume(self, originX, originY, width, height):
        if (originX > self.originX and originX < self.originX + self.width) or (originX + width > self.originX and originX + width < self.originX + self.width):
            if (originY > self.originY and originY < self.originY + self.height) or (originY + height > self.originY and originY + height < self.originY + self.height):
                return True
class Bullet:
    def __init__(self, originX, originY, dtype, radius, angle):
        self.originX = originX
        self.originY = originY
        self.dtype = dtype
        self.radius = radius * self.dtype
        self.direction = angle
        self.speedY = math.cos(math.radians(angle)) * 3
        self.speedX = math.sin(math.radians(angle)) * 3

    def Render(self, screen):
        self.originX -= self.speedX
        self.originY -= self.speedY
        pygame.draw.circle(screen, (255, 255, 255), (int(self.originX) + 30, int(self.originY + 30)), self.radius)

class Barrel:
    def __init__(self, originX, originY):
        self.originX = originX
        self.originY = originY
        self.dulo_spin = 0
        self.dulo = dulo4

    def Render(self, screen):
        screen.blit(self.dulo, (self.originX - int(self.dulo.get_width() / 2), self.originY - int(self.dulo.get_height() / 2)))
    
    def UpdateLocation(self, originX, originY, direction):
        self.originX = originX
        self.originY = originY

    def Rotate(self, rotation_side):
        if rotation_side == "Left":
            self.dulo_spin += 2 % 360
            self.dulo = pygame.transform.rotate(dulo4, self.dulo_spin)

        else:  
            self.dulo_spin -= 2 % 360
            self.dulo = pygame.transform.rotate(dulo4, self.dulo_spin)

    def turretRotate(self, angle):
        self.dulo = pygame.transform.rotate(dulo4, 180 * angle / math.pi - 90)


class GameSceneSingle(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.tank = Tank(100, 100, 65, 65, 2)
        self.turrets = []
        self.turrets.append(Turrets())
        self.turrets.append(Turrets())
        self.turrets.append(Turrets())
        self.score = 0

    def ProcessInput(self, events, pressed_keys, position_mouse):
        self.tank.ChangeLocation(pressed_keys)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(PauseScene(1))

            if event.type == pygame.KEYDOWN and event.key == pygame.K_j and self.tank.shootloop == 0:
                bulletSound.play()
                # When we shoot we mark the time when we shoot and after look, if the time after shooting more than 0.5 sec you may shoot again
                self.tank.seconds = pygame.time.get_ticks()
                # Shooting and giving the angle of our barrel to bullet
                self.tank.Shoot(self.tank.barrel.dulo_spin)
                # Starting Loop
                self.tank.shootloop = 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                self.tank.shift_pressed += 1

        if pressed_keys[pygame.K_k]:
            # Rotating the barrel
            self.tank.barrel.Rotate("Left")

        elif pressed_keys[pygame.K_l]:
            self.tank.barrel.Rotate("Right")

        if self.score >= 3:
            victorySound.play()
            self.SwitchToScene(EndScene(1))

    def Update(self, seconds):
        # Updating Location
        if self.tank.shootloop > 0:
            self.tank.ShootLoop(seconds)
        for turret in self.turrets:
            if turret.shootloop > 0:
                turret.ShootLoop(seconds)

            turret.barrel.UpdateLocation(turret.originX, turret.originY, turret.angle)
            turret.ChangeDirection(self.tank.originX, self.tank.originY)
            turret.barrel.turretRotate(turret.angle)

            if turret.shootloop == 0:
                turret.seconds = pygame.time.get_ticks()
                turret.Shoot(turret.angle)
                turret.shootloop = 1

            turret.TerminateBullets()

        self.tank.barrel.UpdateLocation(self.tank.originX + self.tank.width / 2 - 5, self.tank.originY + self.tank.height / 2, self.tank.direction)
        self.tank.TerminateBullets()

    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0,0,0))
        if self.tank.lives <= 0:
            explosionSound.play()

            if self.tank.explosion_count >= 56:
                self.SwitchToScene(EndScene(0))

            else:
                screen.blit(explosionAnim[self.tank.explosion_count//14], (self.tank.originX, self.tank.originY))
                self.tank.explosion_count += 1
                if self.tank.explosion_count % 14 == 0:
                    self.tank.originX -= 7
                    self.tank.originY -= 7

        else:
            font = pygame.font.SysFont('impact', 20)
            text = font.render('Player', 1, (220, 110, 0))
            screen.blit(text, (self.tank.originX + 5, self.tank.originY - 25))
            self.tank.Render(screen)
            self.tank.barrel.Render(screen)

        for bullet in self.tank.bullets:
            bullet.Render(screen)

        for turret in self.turrets:
            for bullet in turret.bullets:
                bullet.Render(screen)
                if (bullet.originX > self.tank.originX - 25 and bullet.originX < self.tank.originX - 25 + self.tank.width):
                    if (bullet.originY > self.tank.originY - 25 and bullet.originY < self.tank.originY - 25 + self.tank.height):
                        turret.bullets.pop(turret.bullets.index(bullet))
                        if self.tank.lives >= 1:
                            self.tank.lives -= 1

            for bullet in self.tank.bullets:
                if (bullet.originX > turret.originX - turret.radius * 2 and bullet.originX < turret.originX) or (bullet.originX + bullet.radius > turret.originX - turret.radius * 2 and bullet.originX + bullet.radius < turret.originX):
                    if (bullet.originY > turret.originY - turret.radius * 2 and bullet.originY < turret.originY) or (bullet.originY + bullet.radius > turret.originY - turret.radius * 2 and bullet.originY + bullet.radius < turret.originY):
                        self.tank.bullets.pop(self.tank.bullets.index(bullet))
                        self.turrets.pop(self.turrets.index(turret))
                        self.score += 1

            turret.Render(screen)
            turret.barrel.Render(screen)

        font = pygame.font.SysFont('impact', 20)
        text1 = font.render('Score: ' + str(self.score), 1, (255, 255, 255))
        screen.blit(text1, (120, 10))

        text2 = font.render('Lives: ' + str(self.tank.lives), 1, (255, 255, 255))
        screen.blit(text2, (720, 10))

class GameSceneMultiple(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.tank = Tank(120, 100, 65, 65, 2)
        self.tank2 = Tank2(720, 100, 65, 65, 2)
        self.powers = [PowerUp(450, 500)]
        self.lake = []
        self.lake.append(Water(400, 250))
        self.lake.append(Water(464, 250))
        self.lake.append(Water(400, 314))
        self.lake.append(Water(464, 314))

    def ProcessInput(self, events, pressed_keys, position_mouse):
        self.tank.ChangeLocation(pressed_keys)
        self.tank2.ChangeLocation(pressed_keys)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(PauseScene(2))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_j and self.tank.shootloop == 0:
                bulletSound.play()
                # When we shoot we mark the time when we shoot and after look, if the time after shooting more than 0.5 sec you may shoot again
                self.tank.seconds = pygame.time.get_ticks()
                # Shooting and giving the angle of our barrel to bullet
                self.tank.Shoot(self.tank.barrel.dulo_spin)
                # Starting Loop
                self.tank.shootloop = 1

            # TANK2
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.tank2.shootloop == 0:
                bulletSound.play()
                # When we shoot we mark the time when we shoot and after look, if the time after shooting more than 0.5 sec you may shoot again
                self.tank2.seconds = pygame.time.get_ticks()
                # Shooting and giving the angle of our barrel to bullet
                self.tank2.Shoot(self.tank2.barrel.dulo_spin)
                # Starting Loop
                self.tank2.shootloop = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                self.tank.shift_pressed += 1
                self.tank2.shift_pressed += 1

        if pressed_keys[pygame.K_k]:
            # Rotating the barrel
            self.tank.barrel.Rotate("Left")
        elif pressed_keys[pygame.K_l]:
            self.tank.barrel.Rotate("Right")

        # TANK2
        if pressed_keys[pygame.K_f]:
            # Rotating the barrel
            self.tank2.barrel.Rotate("Left")
        elif pressed_keys[pygame.K_g]:
            self.tank2.barrel.Rotate("Right")

    def Update(self, seconds):
        # Updating Location
        if self.tank.shootloop > 0:
            self.tank.ShootLoop(seconds)
        self.tank.barrel.UpdateLocation(self.tank.originX + self.tank.width / 2 - 5 , self.tank.originY + self.tank.height / 2 , self.tank.direction)
        self.tank.TerminateBullets()
        
        # TANK2
        if self.tank2.shootloop > 0:
            self.tank2.ShootLoop(seconds)
        self.tank2.barrel.UpdateLocation(self.tank2.originX + self.tank2.width / 2 - 5 , self.tank2.originY + self.tank2.height / 2, self.tank2.direction)
        self.tank2.TerminateBullets()
        for power in self.powers:
            if power.Consume(self.tank.originX, self.tank.originY, self.tank.width, self.tank.height) == True:
                self.powers.pop(self.powers.index(power))
                coinSound.play()
                self.tank.dtype = 2
            if power.Consume(self.tank2.originX, self.tank2.originY, self.tank2.width, self.tank2.height) == True:
                self.powers.pop(self.powers.index(power))
                coinSound.play()
                self.tank2.dtype = 2

    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0,0,0))
        for waters in self.lake:
            waters.Render(screen)
            if waters.Consume(self.tank.originX, self.tank.originY, self.tank.width, self.tank.height) == True:
                self.tank.drown = True
        if self.tank.lives <= 0:
            explosionSound.play()
            if self.tank.explosion_count >= 56:
                self.SwitchToScene(EndScene(2))
            else:
                screen.blit(explosionAnim[self.tank.explosion_count//14], (self.tank.originX, self.tank.originY))
                self.tank.explosion_count += 1
                if self.tank.explosion_count % 14 == 0:
                    self.tank.originX -= 7
                    self.tank.originY -= 7

        elif self.tank.drown == True:
            drowningSound.play()
            if self.tank2.drowning_count >= 60:
                self.SwitchToScene(EndScene(3))
            else:
                screen.blit(drowningAnim[self.tank2.drowning_count//15], (425, 275))
                self.tank2.drowning_count += 1 

        else:
            self.tank.Render(screen)
            self.tank.barrel.Render(screen)
            font = pygame.font.SysFont('impact', 20)
            text3 = font.render('P1', 1, (220, 110, 0))
            screen.blit(text3, (self.tank.originX + 15, self.tank.originY - 30))
        for bullet in self.tank.bullets:
            if (bullet.originX > self.tank2.originX - 25 and bullet.originX < self.tank2.originX - 25 + self.tank2.width):
                if (bullet.originY > self.tank2.originY - 25 and bullet.originY < self.tank2.originY - 25 + self.tank2.height):
                    self.tank.bullets.pop(self.tank.bullets.index(bullet))
                    if self.tank2.lives >= 1:
                        self.tank2.lives -= 1
                        if bullet.dtype == 2:
                            self.tank2.lives -= 1
                        if self.tank2.lives < 1:
                            self.tank2.lives = 0
            bullet.Render(screen)
        # TANK2
        for waters in self.lake:
            if waters.Consume(self.tank2.originX, self.tank2.originY, self.tank2.width, self.tank2.height) == True:
                self.tank2.drown = True
        if self.tank2.lives <= 0:
            explosionSound.play()
            if self.tank2.explosion_count >= 56:
                self.SwitchToScene(EndScene(3))
            else:
                screen.blit(explosionAnim[self.tank2.explosion_count//14], (self.tank2.originX, self.tank2.originY))
                self.tank2.explosion_count += 1
                if self.tank2.explosion_count % 14 == 0:
                    self.tank2.originX -= 7
                    self.tank2.originY -= 7

        elif self.tank2.drown == True:
            drowningSound.play()
            if self.tank2.drowning_count >= 60:
                self.SwitchToScene(EndScene(3))
            else:
                screen.blit(drowningAnim[self.tank2.drowning_count//15], (425, 275))
                self.tank2.drowning_count += 1 

        else:
            self.tank2.Render(screen)
            self.tank2.barrel.Render(screen)
            font = pygame.font.SysFont('impact', 20)
            text4 = font.render('P2', 1, (220, 110, 0))
            screen.blit(text4, (self.tank2.originX + 15, self.tank2.originY - 30))
        for bullet in self.tank2.bullets:
            if (bullet.originX > self.tank.originX - 25 and bullet.originX < self.tank.originX - 25 + self.tank.width):
                if (bullet.originY > self.tank.originY - 25 and bullet.originY < self.tank.originY - 25 + self.tank.height):
                    self.tank2.bullets.pop(self.tank2.bullets.index(bullet))
                    if self.tank.lives >= 1:
                        self.tank.lives -= 1
                        if bullet.dtype == 2:
                            self.tank.lives -= 1
                        if self.tank.lives < 1:
                            self.tank.lives = 0
            bullet.Render(screen)
        for power in self.powers:
            power.Render(screen)

        font = pygame.font.SysFont('impact', 20)
        text1 = font.render('Player1: ' + str(self.tank.lives), 1, (255, 255, 255))
        screen.blit(text1, (120, 10))

        text2 = font.render('Player2: ' + str(self.tank2.lives), 1, (255, 255, 255))
        screen.blit(text2, (720, 10))

run_game(1000, 600, 60, TitleScene())