import pygame       #ゲーム再作に必要なpygameをインポート
from pygame.locals import *     #キーボード処理に必要
import sys          #ゲーム終了処理に必要
import os


#class map:
#マップデータの作成
#SCR_RECT = Rect(0, 0, WIDTH, HEIGHT)
ROW = 18    #マップサイズ縦
COL = 27    #マップサイズ横
GS = 32     #マスサイズ(ピクセル)
DOWN,LEFT,RIGHT,UP = 0,1,2,3

def main():
    pygame.init()       # pygame初期化
    #画面の生成
    DISP_WIDTH  = 864 #画面の縦サイズ
    DISP_HEIGHT = 576 #画面の横サイズ
    pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
    screen = pygame.display.get_surface()
    pygame.display.set_caption("GAME")

    #マップデータ読み込み
    Map.images[0] = load_image("image6.png")         # 床
    Map.images[1] = load_image("kabe.png")           # 壁    
    Map.images[2] = load_image("bone.gif")

    #スプライト作成
    map = Map()
    player = Player("dog",(1,1),DOWN)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        map.draw(screen)
        player.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()
            # プレイヤーの移動処理
            if event.type == KEYDOWN and event.key == K_DOWN:
                player.move(DOWN, map)
            if event.type == KEYDOWN and event.key == K_LEFT:
                player.move(LEFT, map)
            if event.type == KEYDOWN and event.key == K_RIGHT:
                player.move(RIGHT, map)
            if event.type == KEYDOWN and event.key == K_UP:
                player.move(UP, map)
 
def load_image(filename, colorkey=None):
    #filename = os.path.join("data", filename)
    image = pygame.image.load(filename)
    
    image = image.convert()
    #if colorkey is not None:
        #if colorkey is -1:
        #    colorkey = image.get_at((0,0))
        #image.set_colorkey(colorkey, RLEACCEL)
    return image
 
def split_image(image):
    """128x128のキャラクターイメージを32x32の16枚のイメージに分割
    分割したイメージを格納したリストを返す"""
    imageList = []
    for i in range(0, 128, GS):
        for j in range(0, 128, GS):
            surface = pygame.Surface((GS,GS))
            surface.blit(image, (0,0), (j,i,GS,GS))
            surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
            surface.convert()
            imageList.append(surface)
    return imageList
 
class Map:
    row,col = 18,27  # マップの行数、列数
    images = [None] * 256  # マップチップ（番号->イメージ）
    # 固定マップ
    map =  [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],    #0
        [1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],	#1
		[1,0,1,1,0,1,0,0,0,0,0,1,0,1,1,0,0,0,1,0,0,0,1,1,1,0,1],	#2
		[1,0,1,1,0,1,0,1,0,1,0,1,0,0,1,1,0,1,0,1,0,1,0,1,0,0,1],	#3
		[1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,1,1],	#4
		[1,0,1,1,1,0,1,1,0,1,1,0,0,0,1,1,1,0,0,1,0,1,1,0,0,0,1],	#5
		[1,0,1,0,0,0,1,0,0,1,1,1,1,1,0,0,0,0,1,0,0,0,1,1,1,0,1],	#6
		[1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1],	#7
		[1,0,0,0,1,0,1,0,1,0,1,1,0,1,1,0,0,0,1,1,0,0,1,0,1,1,1],	#8
		[1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,1],	#9
		[1,0,1,1,0,1,0,1,1,0,0,1,0,1,0,1,0,1,0,0,1,0,0,0,1,0,1],	#10
		[1,0,1,1,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,0,1],	#11
		[1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,1,0,1],	#12
		[1,0,1,1,1,0,0,1,0,1,0,0,0,0,0,1,1,0,1,1,0,1,1,0,1,0,1],	#13
		[1,0,1,0,0,0,1,0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,1,1,0,0,1],	#14
		[1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1],	#15
		[1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,2,1],    #16
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]	#17#class map:
    def draw(self, screen):
        """マップを描画する"""
        for r in range(self.row):
            for c in range(self.col):
                screen.blit(self.images[self.map[r][c]], (c*GS,r*GS))
    def is_movable(self, x, y):
        """(x,y)は移動可能か？"""
        # マップ範囲内か？
        if x < 0 or x > self.col-1 or y < 0 or y > self.row-1:
            return False
        # マップチップは移動可能か？
        if self.map[y][x] == 1:  # 壁は移動できない
            return False
        return True
 
class Player:
    animcycle = 24  # アニメーション速度
    frame = 0
    def __init__(self, name, pos, dir):
        self.name = name  # プレイヤー名（ファイル名と同じ）
        self.images = split_image(load_image("%s.gif" % name))
        self.image = self.images[0]  # 描画中のイメージ
        self.x, self.y = pos[0], pos[1]  # 座標（単位：マス）
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
        self.direction = dir

    def move(self, dir, map):
        """プレイヤーを移動"""
        if dir == DOWN:
            self.direction = DOWN
            if map.is_movable(self.x, self.y+1):
                self.y += 1
                self.rect.top += GS
        elif dir == LEFT:
            self.direction = LEFT
            if map.is_movable(self.x-1, self.y):
                self.x -= 1
                self.rect.left -= GS
        elif dir == RIGHT:
            self.direction = RIGHT
            if map.is_movable(self.x+1, self.y):
                self.x += 1
                self.rect.left += GS
        elif dir == UP:
            self.direction = UP
            if map.is_movable(self.x, self.y-1):
                self.y -= 1
                self.rect.top -= GS
    def draw(self, screen):
        screen.blit(self.image, self.rect)


if __name__ == "__main__":
    main()
    