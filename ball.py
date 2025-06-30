import pygame
import random
from define import *


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
