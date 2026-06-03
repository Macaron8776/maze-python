import pygame       #ゲーム再作に必要なpygameをインポート
from pygame.locals import *     #キーボード処理に必要
import sys          #ゲーム終了処理に必要
import os

pygame.init()       # pygame初期化


#マップデータの作成
#SCR_RECT = Rect(0, 0, WIDTH, HEIGHT)
ROW = 18    #マップサイズ縦
COL = 27    #マップサイズ横
size = 32     #マスサイズ(ピクセル)
       # 0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6  (27マス)
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
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]	#17     (18マス)

def load_image(filename, colorkey=None):
    image = pygame.image.load(filename).convert()
    return image

def movable(x,y):
    """(x,y)は移動可能か？"""
    # マップ範囲内か？
    if x<0  or x>COL-1 or y<0 or y>ROW-1:
        return False
    # マップチップは移動可能か？
    if map[y][x] == 1:  # 壁は移動できない
        return False
    return True

#ゲームクリア時のフォントを作成  (フォントの種類、フォントサイズ)
sysfont  = pygame.font.SysFont(None, 80)
sysfont2 = pygame.font.SysFont(None, 65)
sysfont3 = pygame.font.SysFont(None, 50)
# テキストを描画したSurface(=画像に変化)を作成
font1 = sysfont.render("GAME  CLEAR!!", True, (255,138,197))              #第2引数＝アンチエイリアシング（Trueにすると文字なめらか）
font2 = sysfont3.render("Congratulations on your succes!!", True, (255,138,197))              #第3引数＝文字の色　、　第4引数＝背景色
font3 = sysfont3.render("Thank you for playing!!", True, (143,232,224))
font4 = sysfont3.render("Press  \"Enter\"  to exit Game", True, (255,255,255))

#ゲームクリア時のウィンドウクラス
class Window:
    """ウィンドウの基本クラス"""
    EDGE_WIDTH = 4  # 白枠の幅
    def __init__(self, rect):
        self.rect = rect  # 一番外側の白い矩形
        # 内側の黒い矩形                      # 　X に 4*2 = 8 ,　Y に 8　小さな四角形を描く。
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH*2, -self.EDGE_WIDTH*2)
        self.is_visible = False  # ウィンドウを表示中か？
    def draw(self, screen):
        """ウィンドウを描画"""
        if self.is_visible == False: return
        pygame.draw.rect(screen, (255,255,255), self.rect, 0)   #黒色指定
        pygame.draw.rect(screen, (0,0,0), self.inner_rect, 0)   #白色指定
        screen.blit(font1,(230,120))
        screen.blit(font2,(153,190))
        screen.blit(font3,(235,300))
        screen.blit(font4,(200,420))
    def show(self):
        """ウィンドウを表示"""
        self.is_visible = True

# ゲームクリア用ウィンドウ
wnd = Window(Rect(128,96,608,384))     #ゲームクリア時にウィンドウ作成


def main():
    
    #画面の生成
    DISP_WIDTH  = 864     #画面の横サイズ
    DISP_HEIGHT = 576 #画面の縦サイズ
    pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
    screen = pygame.display.get_surface()
    pygame.display.set_caption("GAME")

    x,y = 1,1

    #データ読み込み
    yukaImg = load_image("image6.png")         # 床
    kabeImg = load_image("kabe.png")           # 壁    
    player = load_image("dog.gif")
    goal = load_image("bone.gif")

    def draw_map(screen):
        """マップを描画する"""
        for r in range(ROW):            #(ROW = 縦18マスを表示)
            for c in range(COL):        #(COL = 横27マスを表示)
                if map[r][c] == 0:      #マップで0(床)を表示
                    screen.blit(yukaImg, (c*size,r*size))
                elif map[r][c] == 1:    #マップで1(壁)を表示
                    screen.blit(kabeImg, (c*size,r*size))

    #画面更新のための時計をセット
    clock = pygame.time.Clock()

    while (1):
        clock.tick(60)      #画像の移動処理
        #画像表示
        draw_map(screen)    #マップ描画
        screen.blit(player, (x*size,y*size))  # プレイヤー描画
        screen.blit(goal, (25*size,16*size))  # プレイヤー描画
        
        wnd.draw(screen)  # ゲーム終了時用のウィンドウの描画
        pygame.display.update()     # 画面更新

        # 一回押されたときの処理方法
        for event in pygame.event.get():
            # 画面の閉じるボタンを押したとき
            if event.type == QUIT:
                pygame.quit()       
                sys.exit()
            #ゴール時の当たり判定
            if x == 25 and y == 16:
            #if x == 1 and y == 2:
                wnd.show()  # ウィンドウの描画
                if event.type == KEYDOWN and event.key == K_RETURN:
                    pygame.quit()       
                    sys.exit()         
            else:
                if event.type == KEYDOWN and event.key == K_LEFT:
                    if movable(x-1,y):      #移動可能かの判定
                        x -= 1              
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    if movable(x+1,y):
                        x += 1
                if event.type == KEYDOWN and event.key == K_UP:
                    if movable(x,y-1):
                        y -= 1
                if event.type == KEYDOWN and event.key == K_DOWN:
                    if movable(x,y+1):
                        y += 1

if __name__ == "__main__":
    main()