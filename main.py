import pygame
import random
from define import *
from player import Player
from ball import Ball 
import sys, os
def resource_path(relative_path):
    """Lấy đường dẫn đúng khi chạy file .exe hoặc script .py"""
    try:
        base_path = sys._MEIPASS  # PyInstaller sẽ tạo thư mục tạm ở đây
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Cat'ch Game")
WINDOW_GAME = pygame.display.set_mode((CHIEUDAI, CHIEUCAO))
programIcon = pygame.image.load(resource_path('anh/hinh.jpg'))
pygame.display.set_icon(programIcon)
font = pygame.font.Font(resource_path('word/PressStart2P.ttf'), 24)

class Ball:
    def __init__(self, x, y, direction=1, color=COLOR_RED, sound_hit = None):
       
        self.x = x
        self.y = y
        self.radius = 10
        self.color = color
        self.speed= 5 
        self.vx = self.speed * direction
        self.vy = random.randint(-3, 3)
        self.alive = True
        self.sound_hit = sound_hit
        ball_scale_factor = 2.5  # hoặc 2.0 nếu muốn gấp đôi

# Tính lại kích thước
        new_width = int(self.radius * 2 * ball_scale_factor)
        new_height = int(self.radius * 2 * ball_scale_factor)

        self.image = pygame.image.load(resource_path("anh/mouse.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (new_width, new_height))


    def move(self):
        if not self.alive:
            return

        self.x += self.vx
        self.y += self.vy

        # Bật lại nếu chạm mép trên/dưới
        if self.y - self.radius <= 0 or self.y + self.radius >= CHIEUCAO:
            self.vy *= -1

    def show(self, surface):
        if self.alive:
            surface.blit(self.image, (int(self.x - self.radius), int(self.y - self.radius)))


    def check_collision(self, player):
        if (self.x - self.radius <= player.x + PLAYER_RONG and
            self.x + self.radius >= player.x and
            self.y + self.radius >= player.y and
            self.y - self.radius <= player.y + PLAYER_CAO):
        
        # Đổi hướng bóng
            self.vx *= -1

        # Ngẫu nhiên hóa một chút tốc độ dọc
            self.vy += random.uniform(-2, 2)

        # Giới hạn tốc độ tối đa để game không bị lỗi
            max_speed = 15
            self.vx = max(-max_speed, min(self.vx, max_speed))
            self.vy = max(-max_speed, min(self.vy, max_speed))

        # Tăng tốc nhẹ (tùy thích)
            self.vx *= 1.1
            self.vy *= 1.05
            # Đẩy bóng ra ngoài để tránh kẹt
            if self.vx > 0:
                self.x = player.x + PLAYER_RONG + self.radius + 1
            else:
                self.x = player.x - self.radius - 1
            if self.sound_hit:
                self.sound_hit.play()
        
    def is_out(self):
        return self.x < 0 or self.x > CHIEUDAI

#them anh nen vao
anhvao = pygame.image.load(resource_path("anh/anhvao.png")).convert()

# Tính tỉ lệ scale sao cho khung hình game (CHIEUDAI x CHIEUCAO) chứa được ảnh nền mà không méo
anhvao_width, anhvao_height = anhvao.get_size()

scale_x = CHIEUDAI / anhvao_width
scale_y = CHIEUCAO / anhvao_height

# Chọn tỉ lệ nhỏ hơn để ảnh nằm trọn màn hình (fit)
scale = max(scale_x, scale_y)

new_width = int(anhvao_width * scale)
new_height = int(anhvao_height * scale)

anhvao = pygame.transform.smoothscale(anhvao, (new_width, new_height))

# Tính vị trí vẽ ảnh để căn giữa ảnh nền
anhvao_x = (CHIEUDAI - new_width) // 2
anhvao_y = (CHIEUCAO - new_height) // 2

#THEM ANH NEN CUA TEN VA CUOI GAME
anhnhieu = pygame.image.load(resource_path("anh/anhnhieu.png")).convert()

# Tính tỉ lệ scale sao cho khung hình game (CHIEUDAI x CHIEUCAO) chứa được ảnh nền mà không méo
anhnhieu_width, anhnhieu_height = anhnhieu.get_size()

scale1_x = CHIEUDAI / anhnhieu_width
scale1_y = CHIEUCAO / anhnhieu_height

# Chọn tỉ lệ nhỏ hơn để ảnh nằm trọn màn hình (fit)
scale1 = max(scale1_x, scale1_y)

new1_width = int(anhnhieu_width * scale1)
new1_height = int(anhnhieu_height * scale1)

anhnhieu = pygame.transform.smoothscale(anhnhieu, (new1_width, new1_height))

# Tính vị trí vẽ ảnh để căn giữa ảnh nền
anhnhieu_x = (CHIEUDAI - new1_width) // 2
anhnhieu_y = (CHIEUCAO - new1_height) // 2

#them anh diem
scoreboard_left_img = pygame.image.load(resource_path("anh/score1.png")).convert_alpha()
# Lấy kích thước gốc
orig_w, orig_h = scoreboard_left_img.get_size()
target_width = 80
scale_ratio = target_width / orig_w
target_height = int(orig_h * scale_ratio)
scoreboard_left_img = pygame.transform.smoothscale(scoreboard_left_img, (target_width, target_height))

scoreboard_right_img = pygame.image.load(resource_path("anh/score2.png")).convert_alpha()
orig_w, orig_h = scoreboard_right_img.get_size()
target_width = 80
scale_ratio = target_width / orig_w
target_height = int(orig_h * scale_ratio)
scoreboard_right_img = pygame.transform.smoothscale(scoreboard_right_img, (target_width, target_height))

#them anh nhan vat
playerleft_img = pygame.image.load(resource_path("anh/player1.png")).convert_alpha()
playerleft_img = pygame.transform.scale(playerleft_img, (PLAYER_RONG, PLAYER_CAO))

playerright_img = pygame.image.load(resource_path("anh/player2.png")).convert_alpha()
playerright_img = pygame.transform.scale(playerright_img, (PLAYER_RONG, PLAYER_CAO))

#khoi tao player
playerleft = Player(COLOR_WHITE, 0, CHIEUCAO/2 - PLAYER_CAO/2, playerleft_img)
playerright = Player(COLOR_YELLOW, CHIEUDAI - PLAYER_RONG, CHIEUCAO/2 - PLAYER_CAO/2, playerright_img)

# START MENU 
def show_start_menu():
    showing = True
    while showing:
        WINDOW_GAME.blit(anhvao, (anhvao_x, anhvao_y))
        title_text = font.render("CAT'CH MOUSE", True, COLOR_BLACK)
        instruction_text = font.render("Press SPACE to Start", True, COLOR_BLACK)
        WINDOW_GAME.blit(title_text, (CHIEUDAI//2 - title_text.get_width()//2, 150))
        WINDOW_GAME.blit(instruction_text, (CHIEUDAI//2 - instruction_text.get_width()//2, 250))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                showing = False

def get_player_name(player_number):
    name = ""
    entering = True
    clock = pygame.time.Clock()  # Giới hạn tốc độ vòng lặp
    while entering:
        clock.tick(30)  # tránh vòng lặp chạy quá nhanh
        WINDOW_GAME.blit(anhnhieu, (anhnhieu_x, anhnhieu_y))
        prompt_text = font.render(f"Player {player_number}, enter your name:", True, COLOR_YELLOW)
        name_text = font.render(name + "_", True, COLOR_YELLOW)  # thêm dấu nháy
        WINDOW_GAME.blit(prompt_text, (CHIEUDAI//2 - prompt_text.get_width()//2, CHIEUCAO//3))
        WINDOW_GAME.blit(name_text, (CHIEUDAI//2 - name_text.get_width()//2, CHIEUCAO//2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() != "":
                        entering = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12 and event.unicode.isprintable():
                    name += event.unicode
    return name

#  AUDIO 

pygame.mixer.music.load(resource_path("sound/nen.mp3"))
sound_hit = pygame.mixer.Sound(resource_path('sound/hit.mp3'))
sound_win = pygame.mixer.Sound(resource_path('sound/win1.mp3'))
sound_diem = pygame.mixer.Sound(resource_path('sound/diem.mp3'))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#  GAME INIT 

ball = Ball(CHIEUDAI/2, CHIEUCAO/2, direction=1, sound_hit=sound_hit)
score_left, score_right = 0, 0
window_color = COLOR_BLACK
clock = pygame.time.Clock()



#  MAIN GAME LOOP 
show_start_menu()
name_left = get_player_name(1)
name_right = get_player_name(2)
run = True
#them nen
bg_image = pygame.image.load(resource_path("anh/background.png")).convert()
bg_image = pygame.transform.scale(bg_image, (CHIEUDAI, CHIEUCAO))


while run:
    clock.tick(60)
    WINDOW_GAME.blit(bg_image, (0, 0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.USEREVENT:
            start_x = CHIEUDAI / 2
            start_y = random.randint(50, CHIEUCAO - 50)  # random vị trí y (tránh sát mép)
            vx = random.choice([-1, 1]) * random.uniform(4, 6)  # random tốc độ ngang + hướng
            vy = random.uniform(-4, 4)  # random tốc độ dọc
            ball = Ball(start_x, start_y, direction=1, sound_hit=sound_hit)
            ball.vx = vx
            ball.vy = vy
            pygame.time.set_timer(pygame.USEREVENT, 0)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: playerleft.move_up()
    if keys[pygame.K_s]: playerleft.move_down()
    if keys[pygame.K_UP]: playerright.move_up()
    if keys[pygame.K_DOWN]: playerright.move_down()

    
    playerleft.show(WINDOW_GAME)
    playerright.show(WINDOW_GAME)
    
    
    # Vẽ bảng điểm cho player trái
    left_scoreboard_x = CHIEUDAI // 4 - scoreboard_left_img.get_width() // 2
    WINDOW_GAME.blit(scoreboard_left_img, (left_scoreboard_x, 10))

    # Vẽ bảng điểm cho player phải
    right_scoreboard_x = CHIEUDAI * 3 // 4 - scoreboard_right_img.get_width() // 2
    WINDOW_GAME.blit(scoreboard_right_img, (right_scoreboard_x, 10))

    # Vẽ điểm cho player trái
    left_score = font.render(f"{score_left}", True, COLOR_BLACK)
    WINDOW_GAME.blit(left_score, (
        left_scoreboard_x + scoreboard_left_img.get_width() // 2 - left_score.get_width() // 2, 
        68
        
    ))

    # Vẽ điểm cho player phải
    right_score = font.render(f"{score_right}", True, COLOR_BLACK)
    WINDOW_GAME.blit(right_score, (
        right_scoreboard_x + scoreboard_right_img.get_width() // 2 - right_score.get_width() // 2, 
        68
    ))

    if ball.alive:
        ball.move()
        ball.check_collision(playerleft)
        ball.check_collision(playerright)
        ball.show(WINDOW_GAME)
    if ball.is_out() and ball.alive:
        ball.alive = False
        if ball.x < 0:
            score_right += 1
        elif ball.x > CHIEUDAI:
            score_left += 1
        pygame.mixer.Sound.play(sound_diem)
        pygame.time.set_timer(pygame.USEREVENT, 1000)


    pygame.display.update()

    if score_left >= 5 or score_right >= 5:
        run = False

#GAME OVER SCREEN 
winner = name_left if score_left >= 5 else name_right
WINDOW_GAME.blit(anhnhieu, (anhnhieu_x, anhnhieu_y))
winner_text = font.render(f"{winner} wins!", True, COLOR_YELLOW)
instruction_text = font.render("Press R to Replay or ESC to Quit", True, COLOR_YELLOW)
WINDOW_GAME.blit(winner_text, (CHIEUDAI//2 - winner_text.get_width()//2, CHIEUCAO//3))
WINDOW_GAME.blit(instruction_text, (CHIEUDAI//2 - instruction_text.get_width()//2, CHIEUCAO//2))
pygame.display.update()
pygame.mixer.music.stop()
pygame.mixer.Sound.play(sound_win)

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                score_left = score_right = 0
                playerleft.y, playerright.y = CHIEUCAO/2 - PLAYER_CAO/2, CHIEUCAO/2 - PLAYER_CAO/2
                ball = Ball(CHIEUDAI/2, CHIEUCAO/2, direction=1, sound_hit=sound_hit)
                pygame.mixer.music.play(-1)
                show_start_menu()
                name_left = get_player_name(1)
                name_right = get_player_name(2)
                run = True
                waiting = False
            elif event.key == pygame.K_ESCAPE:
                waiting = False

pygame.quit()
