import pygame       #ゲーム再作に必要なpygameをインポート
from pygame.locals import *     #キーボード処理に必要
import sys          #ゲーム終了処理に必要
import time
import random
import schedule


pygame.init()       # pygame初期化
score1 = 0
score2 = 0
x, y = 2, 1
x2, y2 = 1, 2
player_move = True          #プレイヤー1が動けるか
player2_move = True         #プレイヤー2が動けるか
e_switch = True     #敵の描画
life1 = 10
life2 = 10
life1_gensyou = True        #ライフ計算時に無効、キーボード判定後に有効（そのマスではダメージが動かない限り減らないようにするためのスイッチ）
life2_gensyou = True        #ライフ計算時に無効、キーボード判定後に有効（そのマスではダメージが動かない限り減らないようにするためのスイッチ）

EDGE_WIDTH = 4

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
main_over = sysfont.render("GAME  OVER!!", True, (255,138,197))         #2人ともゲームオーバー時
player_over = sysfont2.render("GAME OVER!!", True, (255,255,255))       #片方ゲームオーバー時
faild = sysfont.render("Faild...", True, (255,138,197))
#　　〇〇〇　スコア・時間表示の文字作成　〇〇〇
font_score1 = sysfont3.render("1P SCORE : ", True, (255,255,255))
font_score2 = sysfont3.render("2P SCORE : ", True, (255,255,255))
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


######################
#　ウィンドウクラス
######################
class C_Window:
    """ウィンドウの基本クラス"""
    global EDGE_WIDTH  # 白枠の幅
    def __init__(self, rect):
        self.rect = rect  # 一番外側の白い矩形
        # 内側の黒い矩形                      # 　X に 4*2 = 8 ,　Y に 8　小さな四角形を描く。
        self.inner_rect = self.rect.inflate(-EDGE_WIDTH*2, -EDGE_WIDTH*2)
        self.clearwindow = False    #　クリアウィンドウを表示中か？
    def clear(self, screen):
        """ウィンドウを描画"""
        if self.clearwindow == False: return
        pygame.draw.rect(screen, (255,255,255), self.rect, 0)   #黒色指定
        pygame.draw.rect(screen, (0,0,0), self.inner_rect, 0)   #白色指定
        screen.blit(font1,(230,120))
        screen.blit(font2,(153,190))
        screen.blit(font3,(235,300))
        screen.blit(font4,(200,420))
    def over(self,screen):
        pygame.draw.rect(screen, (255,255,255), self.rect, 0)   #黒色指定
        pygame.draw.rect(screen, (0,0,0), self.inner_rect, 0)   #白色指定
        screen.blit(main_over,(230,120))
        screen.blit(faild,(330,210))
        screen.blit(font3,(235,300))
        screen.blit(font4,(200,420))
    def clear_show(self):
        """ウィンドウを表示"""
        self.clearwindow = True

# ゲームクリア用ウィンドウ
wnd = C_Window(Rect(128,96,608,384))     #ゲームクリア時にウィンドウ作成


######################
#　エネミークラス
######################
class enemy(pygame.sprite.Sprite):
    def __init__(self, filename, ex, ey, level):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.ex = ex            # x座標代入
        self.ey = ey            # y座標代入
        self.level = level      # 敵のスコア減少率
    def enemy_move(self):
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


    ########################
    #　ゲームオーバー時の画面
    ########################
    def atari(self, screen):
        global player_move          #プレイヤー1が動けるか
        global player2_move         #プレイヤー2が動けるか
        global e_switch
        global life1, life2
        global life1_gensyou, life2_gensyou

        if e_switch == True:           #敵の描画
            screen.blit(self.image, (self.ex*size, self.ey*size))  # 敵描画
        #1Pが敵にあたった（ゲームオーバー）時
        if self.ex == x and self.ey == y and life1_gensyou == True:
            if self.level == 1:
                life1 = life1 - 1
            if self.level == 2:
                life1 = life1 - 2
            if self.level == 3:
                life1 = life1 - 3
            if self.level == 4:
                life1 = life1 - 4
            life1_gensyou = False        #ライフ計算時に無効、キーボード判定後に有効（そのマスではダメージが動かない限り減らないようにするためのスイッチ）
            print(life1)
            
            if life1 <= 0:
                screen.blit(player_over,(950,100))
                player_move = False             #プレイヤ1ーが動けるか        
        #2Pが敵にあたった（ゲームオーバー）時
        if self.ex == x2 and self.ey == y2 and life2_gensyou == True:
            if self.level == 1:
                life2 = life2 - 1
            if self.level == 2:
                life2 = life2 - 2
            if self.level == 3:
                life2 = life2 - 3
            if self.level == 4:
                life2 = life2 - 4
            life2_gensyou = False        #ライフ計算時に無効、キーボード判定後に有効（そのマスではダメージが動かない限り減らないようにするためのスイッチ）
            print(life2)
            
            if life2 <= 0:
                screen.blit(player_over,(950,250))
                player2_move = False             #プレイヤー2が動けるか
        #1Pと2Pがどちらもそうなったとき敵を画面から消して、ゲームオーバー画面を表示する。
        if player_move == False and player2_move == False:
            e_switch = False        #敵キャラクター削除
            wnd.over(screen)  # ゲーム終了時用のウィンドウの描画

            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    pygame.quit()       
                    sys.exit()


######################
#　アイテムクラス
######################
class item(pygame.sprite.Sprite):
                    #ファイル名　  座標　　画像オン　アイスの種類
    def __init__(self, filename, ix, iy, status, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.ix = ix            # x座標代入
        self.iy = iy            # y座標代入
        self.status = status    # 画像オン(True)代入
        self.type = type        # アイスの種類代入


    #####################
    #　スコア計算
    #####################
    def point(self, screen):
        global score1
        global score2

        if self.status == True:
            screen.blit(self.image, (self.ix*size, self.iy*size))  # アイテム描画            
            #プレイヤー1と座標一致したとき
            if self.ix == x and self.iy == y:       #1P用スコア
                if self.type == 1:
                    score1 = score1 + 100
                if self.type == 2:
                    score1 = score1 + 150
                if self.type == 3:
                    score1 = score1 + 200
                if self.type == 4:
                    score1 = score1 + 300
                #アイテム画像を非表示にする
                self.status = False
                #スコア表示用フォント作成
                score1_img = sysfont.render(str(score1), True, (255,255,255))
                screen.blit(score1_img,(900, 100))
                print(score1)
            #プレイヤー2と座標一致したとき
            if self.ix == x2 and self.iy == y2:     #2P用スコア
                if self.type == 1:
                    score2 = score2 + 100
                if self.type == 2:
                    score2 = score2 + 150
                if self.type == 3:
                    score2 = score2 + 200
                if self.type == 4:
                    score2 = score2 + 300
                #アイテム画像を非表示にする
                self.status = False
                print(score2)


    ######################
    #　スコア表示
    ######################
    def score_show(screen):
        #画面に表示
            score1_img = sysfont.render(str(score1), True, (255,255,255))
            screen.blit(score1_img,(900, 100))
            score2_img = sysfont.render(str(score2), True, (255,255,255))
            screen.blit(score2_img,(900, 250))



def main():
    #画面の生成
    DISP_WIDTH  = 1300   #864(mapのみ)     #画面の横サイズ
    DISP_HEIGHT = 576    #画面の縦サイズ
    pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
    screen = pygame.display.get_surface()
    pygame.display.set_caption("GAME")

    #データ読み込み
    yukaImg = pygame.image.load("image6.png").convert()         # 床
    kabeImg = pygame.image.load("kabe.png").convert()           # 壁
    player = pygame.image.load("poodle.gif").convert()
    player2 = pygame.image.load("poodle2.gif").convert()
    goal = pygame.image.load("bone.gif").convert()


    #　　〇〇〇　スコア、タイム表示　〇〇〇
    screen.blit(font_score1,(900, 50))
    screen.blit(font_score2,(900, 200))
    screen.blit(font_time,(900, 350))

    

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
        global x,y,x2,y2            #各プレイヤーの座標
        global player_move          #プレイヤー1が動けるか
        global player2_move          #プレイヤー2が動けるか
        global e_switch         #敵の描画
        global life1_gensyou
        global life2_gensyou

        clock.tick(60)      #画像の移動処理
        #画像表示
        draw_map(screen)    #マップ描画
        screen.blit(player, (x*size,y*size))  # プレイヤー1描画
        screen.blit(player2, (x2*size,y2*size))  # プレイヤー2描画
        screen.blit(goal, (25*size,16*size))  # ゴール描画

        #item.score_show(screen)

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
        enemy1.atari(screen)
        enemy2.atari(screen)
        enemy3.atari(screen)
        enemy4.atari(screen)
        enemy5.atari(screen)
        enemy6.atari(screen)
        enemy7.atari(screen)
        enemy8.atari(screen)
        enemy9.atari(screen)
        enemy10.atari(screen)
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
            if x == 25 and y == 16 or x2 == 25 and y2 == 16:
            #if x == 1 and y == 2:
                wnd.clear_show()  # ウィンドウの描画
                e_switch = False     #敵の描画
                if event.type == KEYDOWN and event.key == K_RETURN:
                    pygame.quit()
                    sys.exit()         
            else:
                #プレイヤー1についての移動処理
                if player_move == True:     #プレイヤ1ーが動けるか  
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
                    life1_gensyou = True        #ライフ計算時に無効、キーボード判定後に有効（そのマスではダメージが動かない限り減らないようにするためのスイッチ）
                
                #プレイヤー2についての移動処理
                if player2_move == True:     #プレイヤ1ーが動けるか  
                    if event.type == KEYDOWN and event.key == K_z:
                        if movable(x2-1,y2):      #移動可能かの判定
                            x2 -= 1              
                    if event.type == KEYDOWN and event.key == K_c:
                        if movable(x2+1,y2):
                            x2 += 1
                    if event.type == KEYDOWN and event.key == K_s:
                        if movable(x2,y2-1):
                            y2 -= 1
                    if event.type == KEYDOWN and event.key == K_x:
                        if movable(x2,y2+1):
                            y2 += 1
                    life2_gensyou = True        #ライフ計算時に無効、キーボード判定後に有効（そのマスではダメージが動かない限り減らないようにするためのスイッチ）

if __name__ == "__main__":
    main()