import pygame
import config as c
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, image, all_sprites_group, bullets_group):
        super().__init__()
        self.shoot_sound = pygame.mixer.Sound(c.shoot_sound)
        self.player_img = image
        self.image = pygame.transform.scale(self.player_img, (50, 38))
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, c.RED, self.rect.center, self.radius)
        self.rect.centerx = c.WIDTH / 2
        self.rect.bottom = c.HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100  # полоска здоровья
        self.shoot_delay = 650  # задержка выстрелов
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.all_sprites = all_sprites_group
        self.bullets = bullets_group

    def update(self):
        POWERUP_TIME = 6000
        # тайм-аут для бонусов
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if not self.hidden:
            # Устанавливаем скорость = 0
            self.speedx = 0
            self.speedy = 0
            # снимаем "маску" зажатых клавиш
            keystate = pygame.key.get_pressed()

            if keystate[pygame.K_LEFT]:
                self.speedx = -8
            if keystate[pygame.K_RIGHT]:
                self.speedx = 8
            if keystate[pygame.K_UP]:
                self.speedy = -8
            if keystate[pygame.K_DOWN]:
                self.speedy = 8
            if keystate[pygame.K_SPACE]:
                self.shoot()

            # Изменяем координаты нашего объекта
            self.rect.x += self.speedx
            self.rect.y += self.speedy

            # Проверка достижеия границы экрана
            if self.rect.right > c.WIDTH:
                self.rect.right = c.WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > c.HEIGHT:
                self.rect.bottom = c.HEIGHT

        elif self.hidden and (pygame.time.get_ticks() - self.hide_timer) > 1500:
            self.hidden = False
            self.rect.centerx = c.WIDTH / 2
            self.rect.bottom = c.HEIGHT - 10
        else:
            # print("скрыт")
            pass

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
                self.shoot_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                self.all_sprites.add(bullet1, bullet2)
                self.bullets.add(bullet1, bullet2)
                self.shoot_sound.play()
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                self.all_sprites.add(bullet1, bullet2, bullet3)
                self.bullets.add(bullet1, bullet2, bullet3)
                self.shoot_sound.play()


    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (c.WIDTH / 2, c.HEIGHT + 200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()


class Mob(pygame.sprite.Sprite):
    def __init__(self, img_path):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(img_path).convert()
        # self.image_orig = pygame.transform.scale(meteor_img, (50, 38))
        self.image_orig.set_colorkey(c.BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.9 / 2)
        # pygame.draw.circle(self.image_orig, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(c.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        # сколько миллисекунд прошло с тех пор, как часы были запущены
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        # проверяется текущее время
        now = pygame.time.get_ticks()
        # вычитается время последнего обновления
        if now - self.last_update > 50:
            self.last_update = now
            # вращение спрайтов
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > c.HEIGHT + 10 or self.rect.left > c.WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(c.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 8)

        self.rotate()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(c.img_bullet).convert()
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        # self.radius = int(self.rect.width / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, images):
        super().__init__()
        self.size = size
        self.images = images
        self.image = self.images[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Pow(pygame.sprite.Sprite):
    def __init__(self, center, images):
        pygame.sprite.Sprite.__init__(self)
        self.powerup_images = images
        self.type = random.choice(['shield', 'gun'])
        self.image = self.powerup_images[self.type]
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > c.HEIGHT:
            self.kill()


class Button:
    def __init__(self, image, active_image, x, y, text, color, id, active):
        self.image = image
        self.active_image = active_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.text = text
        self.font_color = color
        self.font = pygame.font.Font(c.font_name, 25)
        self.text_surf = self.font.render(self.text, True, self.font_color)
        self.text_surf_rect = self.text_surf.get_rect(centerx=self.image.get_width() // 2,\
                                                      centery=self.image.get_height() // 2)
        self.id = id
        self.active = active

    def draw(self, screen):
        if self.active == self.id:
            screen.blit(self.active_image, self.rect)
            self.active_image.blit(self.text_surf, self.text_surf_rect)
        else:
            screen.blit(self.image, self.rect)
            self.image.blit(self.text_surf, self.text_surf_rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, all_sprites_group, bullets_group):
        super().__init__()
        self.image = pygame.image.load(c.img_enemy).convert()
        self.image = pygame.transform.scale(self.image, (60, 40))
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = c.WIDTH // 2
        self.rect.centery = -50
        self.speedx = 3
        self.speedy = 1
        self.shield = 100
        self.last_shot = pygame.time.get_ticks()
        self.all_spites = all_sprites_group
        self.enemy_bullets = bullets_group

    def update(self):
        if self.rect.top < 50:
            self.dx = 0
            self.rect.x += self.dx
            self.rect.y += self.speedy
        else:
            self.speedy = 0
            if self.rect.left < 0:
                self.rect.left = 0
                self.speedx = -self.speedx
            if self.rect.right > c.WIDTH:
                self.rect.right = c.WIDTH
                self.speedx = -self.speedx

            self.rect.x += self.speedx
            self.rect.y += self.speedy
        self.shot()

    def shot(self):
        TIME_DELAY = 2000
        now = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.last_shot > TIME_DELAY:
            self.last_shot = now
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            self.all_spites.add(bullet)
            self.enemy_bullets.add(bullet)


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(c.img_enemy_bullet).convert()
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > c.HEIGHT:
            self.kill()


# class Background(pygame.sprite.Sprite):
#     def __init__(self, y_start, name, color):
#         super().__init__()
#         self.image_orig = pygame.image.load(path.join(c.img_dir, c.img_background_name)).convert()
#         self.image_rot = pygame.transform.rotate(self.image_orig, 90)
#         self.image = pygame.transform.scale(self.image_rot, (c.WIDTH, c.HEIGHT + 30))
#         self.image.set_colorkey(c.BLACK)
#         # self.image = pygame.Surface()
#         self.rect = self.image.get_rect()
#         self.rect.y = y_start
#         self.name = name
#         print(self.name)
#         print(self.rect)
#         print(self.image.get_height())
#
#     def update(self):
#         if self.rect.y > c.HEIGHT:
#             self.rect.bottom = 0
#         else:
#             self.rect.y += 15