import pygame
import random

# 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# 플레이어 변수 설정
player_size = 50
player_x = screen_width // 2 - player_size // 2
player_y = screen_height - player_size - 10
player_speed = 5

# 목표물 변수 설정
target_size = 50
target_x = random.randint(0, screen_width - target_size)
target_y = random.randint(0, screen_height // 2)
target_speed = 5

# 점수 변수 설정
score = 0

# 폰트 설정
font = pygame.font.SysFont(None, 55)

# 게임 루프
running = True
while running:
    pygame.time.delay(30)  # 게임 속도 조절

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < screen_height - player_size:
        player_y += player_speed

    # 목표물 이동
    target_y += target_speed
    if target_y > screen_height:
        target_x = random.randint(0, screen_width - target_size)
        target_y = 0

    # 충돌 감지
    if (player_x < target_x + target_size and
        player_x + player_size > target_x and
        player_y < target_y + target_size and
        player_y + player_size > target_y):
        score += 1
        target_x = random.randint(0, screen_width - target_size)
        target_y = 0

    # 화면 그리기
    screen.fill(black)
    pygame.draw.rect(screen, white, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(screen, red, (target_x, target_y, target_size, target_size))

    # 점수 표시
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, [10, 10])

    # 화면 업데이트
    pygame.display.update()

# 게임 종료
pygame.quit()
