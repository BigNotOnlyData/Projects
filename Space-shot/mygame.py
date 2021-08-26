# import pygame._view
import pygame
import sys
import random
import config as c
from game_objects import Player, Mob, Explosion, Pow, Button, Enemy


class MyGame:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
        pygame.display.set_caption("SpaceShot")
        # pygame.display.set_icon(pygame.image.load(c.img_icon))
        self.clock = pygame.time.Clock()
        self.load_images()
        self.load_music()
        self.background_init()
        self.game_over = True

    def load_images(self):
        self.player_img = pygame.image.load(c.img_player).convert()
        self.player_mini_img = pygame.transform.scale(self.player_img, (25, 19))
        self.player_mini_img.set_colorkey(c.BLACK)

        self.explosion_anim = {}
        self.explosion_anim['lg'] = []  # Большой
        self.explosion_anim['sm'] = []  # Маленький
        self.explosion_anim['player'] = []
        for file in c.img_expl_regular:
            img = pygame.image.load(file).convert()
            img.set_colorkey(c.BLACK)
            img_lg = pygame.transform.scale(img, (75, 75))
            self.explosion_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img, (32, 32))
            self.explosion_anim['sm'].append(img_sm)
        for file in c.img_expl_sonic:
            img = pygame.image.load(file).convert()
            img.set_colorkey(c.BLACK)
            self.explosion_anim['player'].append(img)

        self.powerup_images = {}
        self.powerup_images['shield'] = pygame.image.load(c.img_shield).convert()
        self.powerup_images['gun'] = pygame.image.load(c.img_gun).convert()

    def load_music(self):
        pygame.mixer.music.load(c.music)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)

        self.expl_sounds = []
        for sound in c.expl_sounds:
            self.expl_sounds.append(pygame.mixer.Sound(sound))

        self.shield_sound = pygame.mixer.Sound(c.shield_sound)
        self.power_sound = pygame.mixer.Sound(c.power_sound)
        self.hurt_sound = pygame.mixer.Sound(c.hurt_sound)

    def background_init(self):
        background_orig = pygame.image.load(c.img_background).convert()
        self.background1 = pygame.transform.rotate(background_orig, 90)
        self.background2 = self.background1.copy()
        self.bg_rect1 = self.background1.get_rect(centerx=c.WIDTH // 2, y=0)
        self.bg_rect2 = self.background2.get_rect(centerx=c.WIDTH // 2, y=self.bg_rect1.y - self.bg_rect1.height)

    def draw_background(self, rect1, rect2):
        if rect1.y > c.HEIGHT:
            rect1.y = rect2.y - rect1.height
        elif rect2.y > c.HEIGHT:
            rect2.y = rect1.y - rect2.height
        else:
            rect1.y += 1
            rect2.y += 1
        self.screen.blit(self.background1, rect1)
        self.screen.blit(self.background2, rect2)

    def start_game(self):
        self.score = 0
        self.number_meteotites_shot_down = 0
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = Player(self.player_img, self.all_sprites, self.bullets)
        self.all_sprites.add(self.player)
        for i in range(8):
            self.newmob()

    def newmob(self):
        img_meteor = random.choice(c.img_meteors)
        m = Mob(img_meteor)
        self.all_sprites.add(m)
        self.mobs.add(m)

    def collision_player_meteorite(self, player, mobs):
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            self.hurt_sound.play()
            player.shield -= hit.radius
            expl = Explosion(hit.rect.center, 'sm', self.explosion_anim)
            self.all_sprites.add(expl)
            self.newmob()

            if player.shield <= 0:
                self.death_explosion = Explosion(player.rect.center, 'player', self.explosion_anim)
                self.all_sprites.add(self.death_explosion)
                player.hide()
                # print("спрятали игрока")
                player.lives -= 1
                player.shield = 100

        # Если игрок умер, игра окончена
        if player.lives == 0 and not self.death_explosion.alive():
            self.game_over = True

    def collision_bullet_meteorite(self, bullets, mobs):
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        # На место одного убитого доб авляем одного нового моба
        for hit in hits:
            if not self.enemies:
                self.number_meteotites_shot_down += 1
            else:
                self.number_meteotites_shot_down = 0

            if self.number_meteotites_shot_down > 10:
                self.enemy = Enemy(self.all_sprites, self.enemy_bullets)
                self.all_sprites.add(self.enemy)
                self.enemies.add(self.enemy)

            self.score += 60 - hit.radius
            random.choice(self.expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg', self.explosion_anim)
            self.all_sprites.add(expl)
            if random.random() > 0.9:
                pow = Pow(hit.rect.center, self.powerup_images)
                self.all_sprites.add(pow)
                self.powerups.add(pow)
            self.newmob()

    def collision_player_powerup(self, player, powerups):
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += random.randrange(10, 30)
                self.shield_sound.play()
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'gun':
                player.powerup()
                self.power_sound.play()

    def collision_bullet_enemy(self, enemies, bullets):
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for hit in hits:
            hit.shield -= 30
            if hit.shield <= 0:
                hit.kill()

    def collision_enemybullet_player(self, player, enemy_bullets):
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for hit in hits:
            self.hurt_sound.play()
            player.shield -= 30
            expl = Explosion(hit.rect.center, 'sm', self.explosion_anim)
            self.all_sprites.add(expl)

            if player.shield <= 0:
                self.death_explosion = Explosion(player.rect.center, 'player', self.explosion_anim)
                self.all_sprites.add(self.death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100

        # Если игрок умер, игра окончена
        if player.lives == 0 and not self.death_explosion.alive():
            self.game_over = True

    def draw_text(self, surf, text, size, x, y, color):
        # Создаем экземляр класса Font
        font = pygame.font.Font(c.font_name, size)
        # Сформировать слой Surface с текстом. Сглаживание включено True
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def draw_shield_bar(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct * 100) / BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, c.GREEN, fill_rect)
        pygame.draw.rect(surf, c.WHITE, outline_rect, 2)

    def draw_shield_bar_enemy(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct * 100) / BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, c.RED, fill_rect)
        pygame.draw.rect(surf, c.WHITE, outline_rect, 2)

    def draw_lives(self, surf, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            surf.blit(img, img_rect)

    def show_pause(self):
        self.screen.blit(self.background1, (0, 0))
        self.draw_text(self.screen, "SHMUP!", 64, c.WIDTH / 2, c.HEIGHT / 4, c.WHITE)
        self.draw_text(self.screen, "Arrow keys move, Space to fire", 22, c.WIDTH / 2, c.HEIGHT / 2, c.WHITE)
        self.draw_text(self.screen, "Press a key to begin", 18, c.WIDTH / 2, c.HEIGHT * 3 / 4, c.WHITE)
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(c.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def blit_text(self, surface, text, pos, font, color=pygame.Color('red')):
        """ Функция взята с https://fooobar.com/questions/1668682/rendering-text-with-multiple-lines-in-pygame
        Смысл в том чтобы разделить длинный текст на строки и разместить его на заданной поверхности"""
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width + pos[0] >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    def rules(self):
        # Порядок отображения важен
        bg = self.background_menu.copy()
        surf = pygame.Surface((c.WIDTH // 1.5, c.HEIGHT // 2))
        surf.fill(c.WHITE)
        surf.set_alpha(150)
        rect_surf = surf.get_rect(centerx=c.WIDTH // 2, centery=c.HEIGHT // 2)
        btn_back = Button(self.img_btn.copy(), self.img_btn_active.copy(), c.WIDTH // 2, c.HEIGHT - 100, "BACK", c.RED, 0, 0)
        font = pygame.font.SysFont('arial', 28)
        text = "Летишь и взрываешь все, что попадается на пути.\nУправление кораблем осуществляется \
         через клавиши стрелок, cтрельба через клавишу пробел. Пауза - Esc"
        self.blit_text(surf, text, (20, 20), font)
        bg.blit(surf, rect_surf)
        self.screen.blit(bg, (0, 0))

        rul = True
        while rul:
            self.clock.tick(c.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        rul = False

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and btn_back.rect.collidepoint(event.pos):
                        rul = False

            btn_back.draw(self.screen)
            pygame.display.update()

    def main_menu(self):
        self.background_menu = pygame.image.load(c.img_background).convert()
        self.img_btn = pygame.image.load(c.img_btn).convert()
        self.img_btn.set_colorkey(c.BLACK)
        self.img_btn = pygame.transform.scale(self.img_btn, (230, 50))
        self.img_btn_active = pygame.image.load(c.img_active_btn).convert()
        self.img_btn_active.set_colorkey(c.BLACK)
        self.img_btn_active = pygame.transform.scale(self.img_btn_active, (230, 50))
        text_b = ['New game', 'Continue', 'Rules', 'Exit']
        color = [c.GREEN, c.BLACK, c.BLUE, c.RED]

        buttons = []
        number_active = 0
        n = 0
        for b in range(4):
            button = Button(self.img_btn.copy(), self.img_btn_active.copy(), c.WIDTH // 2, 130 + 100 * b, text_b[b], color[b], b,
                            number_active)
            buttons.append(button)

        menu = True
        while menu:
            self.clock.tick(c.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        n += 1
                        number_active = n % 4
                    if event.key == pygame.K_UP:
                        n -= 1
                        number_active = n % 4

                    if event.key == pygame.K_RETURN:
                        if number_active == 0:
                            self.run()
                        if number_active == 1 and not self.game_over:
                            menu = False
                        if number_active == 2:
                            self.rules()
                        if number_active == 3:
                            sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    for i in range(4):
                        # Находится ли позиция мыши в прямоугольньнике кнопки
                        if buttons[i].rect.collidepoint(event.pos):
                            number_active = i

                if event.type == pygame.MOUSEBUTTONUP:
                    for i in range(4):
                        if buttons[i].rect.collidepoint(event.pos) and event.button == 1:
                            if number_active == 0:
                                self.run()
                            if number_active == 1 and not self.game_over:
                                menu = False
                            if number_active == 2:
                                self.rules()
                            if number_active == 3:
                                sys.exit()

            self.screen.blit(self.background_menu, (0, 0))  # очистить фон
            for btn in buttons:
                btn.active = number_active
                btn.draw(self.screen)

            pygame.display.update()

    def run(self):
        self.game_over = False
        self.running = True
        self.start_game()
        while self.running:
            # Держим цикл на правильной скорости
            self.clock.tick(c.FPS)
            if self.game_over:
                self.main_menu()
                self.start_game()
                self.game_over = False

            # 1. Проверка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()


            # 2. Обновления
            self.all_sprites.update()
            self.collision_player_meteorite(self.player, self.mobs)
            self.collision_bullet_meteorite(self.bullets, self.mobs)
            self.collision_player_powerup(self.player, self.powerups)
            self.collision_bullet_enemy(self.enemies, self.bullets)
            self.collision_enemybullet_player(self.player, self.enemy_bullets)

            # 3. Рендеринг
            self.screen.fill(c.BLUE)
            self.draw_background(self.bg_rect1, self.bg_rect2)
            self.all_sprites.draw(self.screen)
            self.draw_text(self.screen, str(self.score), 18, c.WIDTH / 2, 10, c.WHITE)
            self.draw_shield_bar(self.screen, 5, 5, self.player.shield)
            self.draw_lives(self.screen, c.WIDTH - 100, 5, self.player.lives, self.player_mini_img)
            if self.enemies:
                self.draw_shield_bar_enemy(self.screen, 5, 20, self.enemies.sprites()[0].shield)
            pygame.display.update()

        # pygame.quit()


def main():
    app = MyGame()
    app.main_menu()


if __name__ == '__main__':
    main()
