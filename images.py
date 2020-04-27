import pygame
#.|all_images|
mainMenu = pygame.image.load("./all_images/BackMenu.png")
walkLeft = pygame.image.load("./all_images/Left.png")
walkRight = pygame.image.load("./all_images/Right.png")
walkUp = pygame.image.load("./all_images/Up.png")
walkDown = pygame.image.load("./all_images/Down.png")
ewalkLeft = pygame.image.load("./all_images/eLeft.png")
ewalkRight = pygame.image.load("./all_images/eRight.png")
ewalkUp = pygame.image.load("./all_images/eUp.png")
ewalkDown = pygame.image.load("./all_images/eDown.png")
backGround = pygame.image.load("./all_images/BackGround.png")
explosionAnim = [pygame.image.load("./all_images/Explosion1.png"),
pygame.image.load("./all_images/Explosion2.png"), pygame.image.load("./all_images/Explosion3.png"),
pygame.image.load("./all_images/Explosion4.png")]
water = pygame.image.load("./all_images/Water.png")
drowningAnim = [pygame.image.load("./all_images/Drowning1.png"), pygame.image.load("./all_images/Drowning2.png"),
pygame.image.load("./all_images/Drowning3.png"), pygame.image.load("./all_images/Water.png")]
edrowningAnim = [pygame.image.load("./all_images/eDrowning1.png"), pygame.image.load("./all_images/eDrowning2.png"),
pygame.image.load("./all_images/eDrowning3.png"), pygame.image.load("./all_images/Water.png")]
winPoint = pygame.image.load("./all_images/WinPoint.png")
powerUp = [pygame.image.load("./all_images/Explosion1.png"), pygame.image.load("./all_images/WinPoint.png"), pygame.image.load("./all_images/Wall.png")]
dulo = pygame.image.load("./all_images/dulo.png")
dulo2 = pygame.image.load("./all_images/dulo2.png")
dulo3 = pygame.image.load("./all_images/dulo3.png")
dulo4 = pygame.image.load("./all_images/dulo4.png")
dulo5 = pygame.image.load("./all_images/dulo4.png")
coin = pygame.image.load("./all_images/coin2.png")
dulo.set_colorkey((0,0,0))
dulo2.set_colorkey((0,0,0))
dulo4.blit(walkUp, (100, 100))
dulo.blit(walkUp, (100, 100))