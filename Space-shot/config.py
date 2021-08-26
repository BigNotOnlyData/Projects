from os import path
import sys


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return path.join(sys._MEIPASS, relative)
    return path.join(relative)

# Экран
WIDTH = 480
HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Пути расположения папок
img_dir = resource_path(path.join(path.dirname(__file__), 'img'))
meteors_dir = resource_path(path.join(img_dir, 'Meteors'))
explosions_dir = resource_path(path.join(img_dir, 'Explosions'))
fonts_dir = resource_path(path.join(path.dirname(__file__), 'fonts'))
snd_dir = resource_path(path.join(path.dirname(__file__), 'snd'))

# Картинки
img_player = resource_path(path.join(img_dir, "playerShip1_blue.png"))
img_background = resource_path(path.join(img_dir, "starfield.png"))
img_bullet = resource_path(path.join(img_dir, "laserGreen11.png"))
img_shield = resource_path(path.join(img_dir, "shield_gold.png"))
img_gun = resource_path(path.join(img_dir, "bolt_gold.png"))
img_btn = resource_path(path.join(img_dir, "buttonBlue.png"))
img_active_btn = resource_path(path.join(img_dir, 'buttonYellow.png'))
img_enemy = resource_path(path.join(img_dir, "enemyBlack1.png"))
img_enemy_bullet = resource_path(path.join(img_dir, "laserRed03.png"))
img_icon = resource_path(path.join(img_dir, 'rick.ico'))

img_meteors = [resource_path(path.join(meteors_dir, filename)) for filename in \
               ['meteorBrown_big1.png', 'meteorBrown_big2.png',
                'meteorBrown_big3.png', 'meteorBrown_big4.png',
                'meteorBrown_med1.png', 'meteorBrown_med3.png',
                'meteorBrown_small1.png', 'meteorBrown_small2.png',
                'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png']]

img_expl_regular = [resource_path(path.join(explosions_dir, filename)) for filename in \
                    [f'regularExplosion0{i}.png' for i in range(9)]]

img_expl_sonic = [resource_path(path.join(explosions_dir, filename)) for filename in \
                  [f'sonicExplosion0{i}.png' for i in range(9)]]

# Шрифты
font_name = resource_path(path.join(fonts_dir, 'kenvector_future_thin.ttf'))

# Звуки/музыка
expl_sounds = [resource_path(path.join(snd_dir, snd)) for snd in ['expl3.wav', 'expl6.wav']]
shoot_sound = resource_path(path.join(snd_dir, 'pew.wav'))
shield_sound = resource_path(path.join(snd_dir, 'Shieldup15.wav'))
power_sound = resource_path(path.join(snd_dir, 'Powerup.wav'))
hurt_sound = resource_path(path.join(snd_dir, 'Hurt.wav'))
music = resource_path(path.join(snd_dir, 'music_fon.wav'))
