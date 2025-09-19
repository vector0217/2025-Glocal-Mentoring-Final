'''
    pygame을 활용한 캐릭터 움직이기 게임 만들기
'''
import pygame

# 초기화
pygame.init()

# 화면 설정
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simple Game")

# 색상 및 변수 설정
white = (255, 255, 255)
red = (255, 0, 0)
x = 400
y = 300
move_x = 0
move_y = 0
width = 50
height = 50

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_x = -5
            if event.key == pygame.K_RIGHT:
                move_x = 5
            if event.key == pygame.K_UP:
                move_y = -5
            if event.key == pygame.K_DOWN:
                move_y = 5
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                move_x = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                move_y = 0

    # 위치 업데이트
    x += move_x
    y += move_y

    # 화면 경계 체크
    if x < 0:
        x = 0
    elif x > 800 - width:
        x = 800 - width

    if y < 0:
        y = 0
    elif y > 600 - height:
        y = 600 - height

    # 화면에 그리기
    screen.fill(white)
    pygame.draw.rect(screen, red, [x, y, width, height])
    pygame.display.update()

pygame.quit()
