import pygame
import random
import sys
import requests
import io

# 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Game")

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# 플레이어 변수 설정
player_size = 50
player_x = screen_width // 2 - player_size // 2
player_y = screen_height - player_size - 10
player_speed = 7

# 목표물 변수 설정
target_size = 50
target_x = random.randint(0, screen_width - target_size)
target_y = -target_size
target_speed = 7

# 목숨 및 점수 변수 설정
lives = 3
score = 0
high_score = 0

# 폰트 설정
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)

# 하트 이미지 로드
# 인터넷에서 하트 이미지 다운로드
heart_url = "https://upload.wikimedia.org/wikipedia/commons/8/8e/Heart-image.png"

response = requests.get(heart_url)
if response.status_code == 200:
    image_bytes = io.BytesIO(response.content)
    heart_image = pygame.image.load(image_bytes)
    heart_image = pygame.transform.scale(heart_image, (30, 30))
else:
    print("❌ 하트 이미지를 불러오지 못했습니다.")
    pygame.quit()
    sys.exit()

# 게임 상태
game_active = False

# 게임 시작 버튼 그리기
def draw_start_button():
    start_button_rect = pygame.Rect(300, 250, 200, 100)
    pygame.draw.rect(screen, red, start_button_rect)
    text = font.render("START", True, white)
    screen.blit(text, (start_button_rect.x + 40, start_button_rect.y + 20))
    return start_button_rect

# 게임 루프
while True:
    if not game_active:
        screen.fill(black)
        start_button_rect = draw_start_button()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    game_active = True
                    lives = 3
                    score = 0
                    player_x = screen_width // 2 - player_size // 2
                    target_x = random.randint(0, screen_width - target_size)
                    target_y = -target_size

    else:
        pygame.time.delay(30)  # 게임 속도 조절

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
            player_x += player_speed

        # 목표물 이동 (상하 이동)
        target_y += target_speed

        # 충돌 감지 및 목표물 놓침 처리
        if (player_x < target_x + target_size and
            player_x + player_size > target_x and
            player_y < target_y + target_size and
            player_y + player_size > target_y):
            score += 1
            target_x = random.randint(0, screen_width - target_size)
            target_y = -target_size
            target_speed += 1  # 목표물 속도 증가
        elif target_y > screen_height:
            lives -= 1
            if lives == 0:
                high_score = max(high_score, score)
                game_active = False
            target_x = random.randint(0, screen_width - target_size)
            target_y = -target_size

        # 화면 그리기
        screen.fill(black)
        pygame.draw.rect(screen, white, (player_x, player_y, player_size, player_size))
        pygame.draw.rect(screen, red, (target_x, target_y, target_size, target_size))

        # 점수 표시
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, [10, 10])

        # 목숨 표시
        for i in range(lives):
            screen.blit(heart_image, (screen_width - 100 + i * 35, 10))

        # 최고 점수 표시
        high_score_text = small_font.render(f"High Score: {high_score}", True, white)
        screen.blit(high_score_text, [10, 60])

        # 화면 업데이트
        pygame.display.update()
