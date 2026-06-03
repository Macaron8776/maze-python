import pygame       #ゲーム再作に必要なpygameをインポート
from pygame.locals import *     #キーボード処理に必要
import sys          #ゲーム終了処理に必要
import os
import time
import random
import schedule


pygame.init()       # pygame初期化
score = 0
life = 10
x,y = 1,1
pl_move = True      #プレイヤーが動けるか
e_switch = True     #敵の描画

EDGE_WIDTH = 4
life_gensyou = True    #プレイヤーがキーを押した後にオン。　True で　ライフ減少するようになる。　敵にあたるとFalse

#ゲームクリア時のフォントを作成  (フォントの種類、フォントサイズ)
sysfont  = pygame.font.SysFont(None, 80)
sysfont2 = pygame.font.SysFont(None, 65)
sysfont3 = pygame.font.SysFont(None, 50)
# テキストを描画したSurface(=画像に変化)を作成
#　　〇〇〇　ゲームクリア時の文字作成　〇〇〇
font1 = sysfont.render("GAME  CLEAR!!", True, (255,138,197))              #第2引数＝アンチエイリアシング（Trueにすると文字なめらか）
font2 = sysfont3.render("Congratulations on your succes!!", True, (255,138,197))              #第3引数＝文字の色　、　第4引数＝背景色
font3 = sysfont3.render("Thank you for playing!!", True, (143,232,224))
font4 = sysfont3.render("Press  \"Enter\"  to exit Game", True, (255,255,255))
#　　〇〇〇　ゲームオーバーの文字作成　〇〇〇
over = sysfont.render("GAME  OVER!!", True, (255,138,197))
faild = sysfont.render("Faild...", True, (255,138,197))
#　　〇〇〇　スコア・時間表示の文字作成　〇〇〇
font_score = sysfont3.render("SCORE : ", True, (255,255,255))
font_time = sysfont3.render("TIME : ", True, (255,255,255))




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
	    [1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1],	#7
	    [1,0,0,0,1,0,1,0,1,0,1,1,0,1,1,0,0,0,1,1,0,0,1,0,1,1,1],	#8
	    [1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,1],	#9
    	[1,0,1,1,0,1,0,1,1,0,0,1,0,1,0,1,0,1,0,0,1,0,0,0,1,0,1],	#10
    	[1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1],	#11
    	[1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,1,0,1],	#12
    	[1,0,1,1,1,0,0,1,0,1,0,0,0,0,0,1,1,0,1,1,0,1,1,0,1,0,1],	#13
    	[1,0,1,0,0,0,1,0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,1,1,0,0,1],	#14
    	[1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1],	#15
    	[1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1],    #16
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]	#17     (18マス)

        
def movable(x,y):
    """(x,y)は移動可能か？"""
    # マップ範囲内か？
    if x<0  or x>COL-1 or y<0 or y>ROW-1:
        return False
    # マップチップは移動可能か？
    if map[y][x] == 1:  # 壁は移動できない
        return False
    return True

class enemy(pygame.sprite.Sprite):
    def __init__(self, filename, ex, ey, level):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.ex = ex            # x座標代入
        self.ey = ey            # y座標代入
        self.level = level      # 敵のスコア減少率
    def enemy_move(self):
            #e_time = int(time.time())
            #if e_time & 1 == 0:
            suuti = random.randint(1, 4)
            if suuti == 1:
                if movable(self.ex+1,self.ey):      #移動可能かの判定
                    self.ex += 1
            if suuti == 2:
                if movable(self.ex-1,self.ey):
                    self.ex -= 1
            if suuti == 3:
                if movable(self.ex,self.ey+1):      #移動可能かの判定
                    self.ey += 1
            if suuti == 4:
                if movable(self.ex,self.ey-1):
                    self.ey -= 1


    def life(self, screen):
        global life
        global pl_move          #プレイヤーが動けるか
        global life_gensyou     #プレイヤーがキーを押した後にオン。　True で　ライフ減少するようになる。　敵にあたるとFalse
        global e_switch

        if e_switch == True:           #敵の描画
            screen.blit(self.image, (self.ex*size, self.ey*size))  # 敵描画
        if self.ex == x and self.ey == y and life_gensyou == True:
            life_gensyou = False
            if self.level == 1:
                life -= 1
            if self.level == 2:
                life -= 2
            if self.level == 3:
                life -= 3
            if self.level == 4:
                life -= 4
            
            print(life_gensyou)
            #スコアを表示
            print(life)

        if life <= 0:
            rect = Rect(128,96,608,384)  # 一番外側の白い矩形
            # 内側の黒い矩形                      # 　X に 4*2 = 8 ,　Y に 8　小さな四角形を描く。
            inner_rect = rect.inflate(-EDGE_WIDTH*2, -EDGE_WIDTH*2)
            pygame.draw.rect(screen, (255,255,255), rect, 0)   #黒色指定
            pygame.draw.rect(screen, (0,0,0), inner_rect, 0)   #白色指定
            screen.blit(over,(230,120))
            screen.blit(faild,(330,210))
            screen.blit(font3,(235,300))
            screen.blit(font4,(200,420))
            e_switch = False       #敵の描画
            pl_move = False             #プレイヤーが動けるか

            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    pygame.quit()       
                    sys.exit()


class item(pygame.sprite.Sprite):
                    #ファイル名　  座標　　画像オン　アイスの種類
    def __init__(self, filename, ix, iy, status, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.ix = ix            # x座標代入
        self.iy = iy            # y座標代入
        self.status = status    # 画像オン(True)代入
        self.type = type        # アイスの種類代入
    def point(self, screen):
        global score
        if self.status == True:
            screen.blit(self.image, (self.ix*size, self.iy*size))  # プレイヤー描画
            #座標一致したとき
            if self.ix == x and self.iy == y:
                #アイスだった時
                if self.type == 1:
                    score = score + 100
                if self.type == 2:
                    score = score + 150
                if self.type == 3:
                    score = score + 200
                if self.type == 4:
                    score = score + 300
                
                #画像を非表示にする
                self.status = False
                #スコアを表示
                print(score)



class C_Window:
    """ウィンドウの基本クラス"""
    global EDGE_WIDTH  # 白枠の幅
    def __init__(self, rect):
        self.rect = rect  # 一番外側の白い矩形
        # 内側の黒い矩形                      # 　X に 4*2 = 8 ,　Y に 8　小さな四角形を描く。
        self.inner_rect = self.rect.inflate(-EDGE_WIDTH*2, -EDGE_WIDTH*2)
        self.is_visible = False  # ウィンドウを表示中か？
    def clear(self, screen):
        """ウィンドウを描画"""
        if self.is_visible == False: return
        pygame.draw.rect(screen, (255,255,255), self.rect, 0)   #黒色指定
        pygame.draw.rect(screen, (0,0,0), self.inner_rect, 0)   #白色指定
        screen.blit(font1,(230,120))
        screen.blit(font2,(153,190))
        screen.blit(font3,(235,300))
        screen.blit(font4,(200,420))
    def cl_show(self):
        """ウィンドウを表示"""
        self.is_visible = True


# ゲームクリア用ウィンドウ
wnd = C_Window(Rect(128,96,608,384))     #ゲームクリア時にウィンドウ作成


def main():
    #画面の生成
    DISP_WIDTH  = 1300   #864     #画面の横サイズ
    DISP_HEIGHT = 576 #画面の縦サイズ
    pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
    screen = pygame.display.get_surface()
    pygame.display.set_caption("GAME")

    #データ読み込み
    yukaImg = pygame.image.load("image6.png").convert()         # 床
    kabeImg = pygame.image.load("kabe.png").convert()           # 壁
    player = pygame.image.load("poodle2.gif").convert()
    goal = pygame.image.load("bone.gif").convert()

    screen.blit(font_score,(900, 100))
    screen.blit(font_time,(900, 300))


    def draw_map(screen):
        """マップを描画する"""
        for r in range(ROW):            #(ROW = 縦18マスを表示)
            for c in range(COL):        #(COL = 横27マスを表示)
                if map[r][c] == 0:      #マップで0(床)を表示
                    screen.blit(yukaImg, (c*size,r*size))
                elif map[r][c] == 1:    #マップで1(壁)を表示
                    screen.blit(kabeImg, (c*size,r*size))

    #アイテム作成&判定(status)有効化
    item1 = item("pin.gif", 1, 16, True, 4)
    item2 = item("soft.gif", 2, 8, True, 2)
    item3 = item("ice.gif", 4, 3, True, 1)
    item4 = item("water-m.gif", 4, 11, True, 3)
    item5 = item("ice.gif", 7, 8, True, 1)
    item6 = item("soft.gif", 8, 12, True, 2)
    item7 = item("water-m.gif", 9, 1, True, 3)
    item8 = item("ice.gif", 11, 1, True, 1)
    item9 = item("pin.gif", 11, 9, True, 4)
    item10 = item("soft.gif", 11, 15, True, 2)
    item11 = item("water-m.gif", 12, 11, True, 3)
    item12 = item("pin.gif", 14, 16, True, 4)
    item13 = item("ice.gif", 16, 3, True, 1)
    item14 = item("water-m.gif", 16, 12, True, 3)
    item15 = item("soft.gif", 17, 16, True, 2)
    item16 = item("ice.gif", 18, 3, True, 1)
    item17 = item("soft.gif", 20, 4, True, 2)
    item18 = item("ice.gif", 20, 8, True, 1)
    item19 = item("water-m.gif", 21, 16, True, 3)
    item20 = item("soft.gif", 23, 13, True, 2)
    item21 = item("water-m.gif", 24, 11, True, 3)
    item22 = item("pin.gif", 25, 1, True, 4)


    #敵生成
    enemy1 = enemy("cat.gif", 13, 16, 1)
    enemy2 = enemy("cat.gif", 9, 7, 1)
    enemy3 = enemy("cat.gif", 12, 2, 1)
    enemy4 = enemy("tanuki.gif", 4, 4, 2)
    enemy5 = enemy("tanuki.gif", 24, 4, 2)
    enemy6 = enemy("tanuki.gif", 23, 15, 2)
    enemy7 = enemy("kangaroo.gif", 21, 1, 3)
    enemy8 = enemy("kangaroo.gif", 17, 9, 3)
    enemy9 = enemy("inoshishi.gif", 19, 10, 4)
    enemy10 = enemy("inoshishi.gif", 2, 15, 4)
    #敵の動きを読み込む
    schedule.every(0.5/60).minutes.do(enemy1.enemy_move)          #時間指定は分単位（＝ 0.5 秒）
    schedule.every(0.5/60).minutes.do(enemy2.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy3.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy4.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy5.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy6.enemy_move)
    schedule.every(1/60).minutes.do(enemy7.enemy_move)            ##時間指定は分単位（＝ 1 秒）
    schedule.every(1/60).minutes.do(enemy8.enemy_move)
    schedule.every(1/60).minutes.do(enemy9.enemy_move)
    schedule.every(1/60).minutes.do(enemy10.enemy_move)


    #画面更新のための時計をセット
    clock = pygame.time.Clock()

    while (1):
        global x,y              #グローバル変数とみなす様にするため記入
        global pl_move          #プレイヤーが動けるか
        global life_gensyou     #プレイヤーがキーを押した後にオン。　True で　ライフ減少するようになる。　敵にあたるとFalse
        global e_switch         #敵の描画

        clock.tick(60)      #画像の移動処理
        #画像表示
        draw_map(screen)    #マップ描画
        screen.blit(player, (x*size,y*size))  # プレイヤー描画
        screen.blit(goal, (25*size,16*size))  # プレイヤー描画


        #スプライト判定無効化＆表示
        item1.point(screen)
        item2.point(screen)
        item3.point(screen)
        item4.point(screen)
        item5.point(screen)
        item6.point(screen)
        item7.point(screen)
        item8.point(screen)
        item9.point(screen)
        item10.point(screen)
        item11.point(screen)
        item12.point(screen)
        item13.point(screen)
        item14.point(screen)
        item15.point(screen)
        item16.point(screen)
        item17.point(screen)
        item18.point(screen)
        item19.point(screen)
        item20.point(screen)
        item21.point(screen)
        item22.point(screen)


        #敵表示
        enemy1.life(screen)
        enemy2.life(screen)
        enemy3.life(screen)
        enemy4.life(screen)
        enemy5.life(screen)
        enemy6.life(screen)
        enemy7.life(screen)
        enemy8.life(screen)
        enemy9.life(screen)
        enemy10.life(screen)
        #敵の動きを実際に実行させる。
        schedule.run_pending()


        wnd.clear(screen)  # ゲーム終了時用のウィンドウの描画
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
                wnd.cl_show()  # ウィンドウの描画
                e_switch = False     #敵の描画
                if event.type == KEYDOWN and event.key == K_RETURN:
                    pygame.quit()
                    sys.exit()         
            else:
                if pl_move == True:     #プレイヤーが動けるか  
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
                    life_gensyou = True

if __name__ == "__main__":
    main()