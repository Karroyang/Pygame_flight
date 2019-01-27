import random
import pygame
# 定义屏幕常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 定义帧数
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 创建发射子弹的定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):

    def __init__(self, image_name, speed=1):
        # 调用父类的初始化
        super().__init__()

        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class BackGround(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt = False):

        # 1.调用父类的方法实现精灵的创建（image/rect/speed）
        super().__init__('./images/background.png')
        # 2.判断是否需要移出屏幕
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        # 1.调用父类的方法
        super().update()

        # 2.判断是否移出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):

        # 1.调用父类的方法实现精灵的创建（image/rect/speed）
        super().__init__('./images/enemy1.png')

        # 2.指定敌机的初始随机速度(1,3)
        self.speed = random.randint(1, 3)

        # 3.指定敌机的初始随机位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):

        # 1.调用父类的方法实现向下飞行
        super().update()

        # 2.判断是否移出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            # kill方法可以将精灵从精灵组中移出，精灵被销毁
            self.kill()

    def __del__(self):
        # print('删除 %s'%self.rect)
        pass


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):

        # 1.调用父类的方法实现精灵的创建（image/speed）
        super().__init__('./images/me1.png', 0)

        # 2.设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 3.创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        # 英雄水平方向移动
        self.rect.x += self.speed

        # 控制英雄不能飞出屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        # print('发射...')

        for i in (0,1,2):
            # 1.创建子弹精灵
            bullet = Bullet()
            # 2.设置初始位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            # 3.添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):

        # 调用父类方法创建精灵（image/speed)
        super().__init__('./images/bullet1.png', -2)

    def update(self):

        # 垂直向上移动
        super().update()

        # 判断是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        # print('子弹销毁')
        pass