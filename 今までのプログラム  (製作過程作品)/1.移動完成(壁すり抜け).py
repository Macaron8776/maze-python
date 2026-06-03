import pygame       #ゲーム再作に必要なpygameをインポート
from pygame.locals import *     #キーボード処理に必要
import sys          #ゲーム終了処理に必要


class MySprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        width   = self.image.get_width()
        height  = self.image.get_height()
        self.rect = Rect(x, y, width, height)   #キャラののもととなるx,y座標を形式的に指定
        self.vx = vx
        self.vy = vy

    #移動処理関数 update()
    def update(self):  
        # 押されているキーをチェック
        pressed_keys = pygame.key.get_pressed()
        # 押されているキーに応じて画像を移動
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.vx, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.vx, 0)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.vy)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.vy)
        #画面からはみ出ないように
        #self.rect = self.rect.clamp_ip()

    def draw(self,screen):
        #画像表示
        screen.blit(self.image,self.rect)    #プレイヤー画像の表示        #(表示するファイル、座標)


def main():
    pygame.init()       # pygame初期化
    #画面の生成
    DISP_WIDTH  = 864     #画面の縦サイズ
    DISP_HEIGHT = 576 #画面の横サイズ
    pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
    screen = pygame.display.get_surface()
    pygame.display.set_caption("GAME")

    #class map:
    #マップデータの作成
    #SCR_RECT = Rect(0, 0, WIDTH, HEIGHT)
    ROW = 18    #マップサイズ縦
    COL = 27    #マップサイズ横
    GS = 32     #マスサイズ(ピクセル)
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
			[1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1],    #16
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]	#17
    #マップデータ読み込み
    yukaImg = pygame.image.load("image6.png").convert_alpha()         # 床
    kabeImg = pygame.image.load("kabe.png").convert_alpha()           # 壁    
    def draw_map(screen):
        """マップを描画する"""
        for r in range(ROW):            #(ROW = 縦18マスを表示)
            for c in range(COL):        #(COL = 横27マスを表示)
                if map[r][c] == 0:      #マップで0(床)を表示
                    screen.blit(yukaImg, (c*GS,r*GS))
                elif map[r][c] == 1:    #マップで1(壁)を表示
                    screen.blit(kabeImg, (c*GS,r*GS))


    #スプライト作成
    player = MySprite("dog.gif",32,32,2,2)      #(x座標、y座標、vxスピード、vyスピード)の指定
    goal = MySprite("bone.gif",32*25,32*16,2,2)

    #画面更新のための時計をセット
    clock = pygame.time.Clock()

    while (1):
        clock.tick(60)      #画像の移動処理
        #マップ表示
        draw_map(screen)    #マップ描画        
        #スプライト更新(キーボード操作)
        player.update()     #update()関数でキャラ移動をしている
        #スプライト描画
        player.draw(screen)     #プレイヤー
        goal.draw(screen)       #ゴール

        pygame.display.update()     # 画面更新

        # 一回押されたときの処理方法
        for event in pygame.event.get():
            # 画面の閉じるボタンを押したとき
            if event.type == QUIT:
                pygame.quit()
                sys.exit()        

if __name__ == "__main__":
    main()