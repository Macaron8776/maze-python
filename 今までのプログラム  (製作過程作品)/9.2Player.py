import pygame       #ゲーム再作に必要なpygameをインポート
from pygame.locals import *     #キーボード処理に必要
import sys          #ゲーム終了処理に必要
import time
import random
import schedule
import datetime
import threading

"""     life1_gensyou = false  で　当たり判定回避   212行目参照 """

pygame.init()       # pygame初期化
score1 = 0
score2 = 0
x, y = 2, 1
x2, y2 = 1, 2
player_move = True          #プレイヤー1が動けるか
player2_move = True         #プレイヤー2が動けるか
life1 = 10
life2 = 10
life1_gensyou = True        #ライフ計算時に無効、キーボード判定後に有効（そのマスではダメージが動かない限り減らないようにするためのスイッチ）
life2_gensyou = True        #ライフ計算時に無効、キーボード判定後に有効（そのマスではダメージが動かない限り減らないようにするためのスイッチ）
finish_score1 = 0
finish_score2 = 0
p1_clear = False
p2_clear = False
p1_time = 0
p2_time = 0

#カウントダウンタイマーに必要な時間を取得（ゲーム開始時）
start_time = datetime.datetime.now()



EDGE_WIDTH = 4

#ゲームクリア時のフォントを作成  (フォントの種類、フォントサイズ)
sysfont  = pygame.font.SysFont(None, 80)
sysfont2 = pygame.font.SysFont(None, 65)
sysfont3 = pygame.font.SysFont(None, 50)
sysfont4 = pygame.font.SysFont(None, 40)
sysfont5 = pygame.font.SysFont("hg創英角ﾎﾟｯﾌﾟ体hgp創英角ﾎﾟｯﾌﾟ体hgs創英角ﾎﾟｯﾌﾟ体", 20)
# テキストを描画したSurface(=画像に変化)を作成
#　　〇〇〇　ゲームクリア時の文字作成　〇〇〇
font1 = sysfont.render("GAME  FINISH!!", True, (255,138,197))              #第2引数＝アンチエイリアシング（Trueにすると文字なめらか）、#第3引数＝文字の色、第4引数＝背景色
font4 = sysfont3.render("Press  \"Enter\"  to exit Game", True, (255,255,255))
#　　〇〇〇　ゲームオーバーの文字作成　〇〇〇
player_life_0 = sysfont2.render("F  A  I  L  D  ! !", True, (255,105,180))       #片方ゲームオーバー時
player_clear = sysfont2.render("C  L  E  A  R  ! !", True, (255,105,180))
#　　〇〇〇　スコア・時間表示の文字作成　〇〇〇
font_player1 = sysfont3.render("1P", True, (255,255,255))
font_player2 = sysfont3.render("2P", True, (255,255,255))
font_score = sysfont3.render("SCORE : ", True, (255,255,255))
font_life = sysfont3.render("LIFE : ", True, (255,255,255))
font_time = sysfont3.render("TIME : ", True, (255,255,255))
#　　〇〇〇　スコアの計算方法の詳細　〇〇〇
finish_score_syousai = sysfont5.render("★ 最終スコア ★", True, (255,255,255))
finish_score_syousai_2 = sysfont5.render("スコア ＋ ライフ × 100 ＋ 時間 × 20", True, (255,255,255))



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
    	[1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,1],    #16
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]	#17     (18マス)


#カウントダウンタイマーセット
def timer(screen):
    global player_move, player2_move, life1_gensyou, life2_gensyou, limit_time
    #制限時間セット
    seigen_zikan = 120

    #プレイ時現在の時刻取得
    now_time = datetime.datetime.now()
    #経過時間 = スタート時の時間 -　現在の時間
    keika_time = now_time - start_time
    #残り制限時間 = 制限時間 - 経過時間
    limit_time = seigen_zikan - keika_time.seconds
    
    if limit_time <= 0:
        limit_time = 0
        wnd.clear_show()
        #1Pについて（移動、ライフ減少）
        player_move = False             #プレイヤ1ーが動けるか    
        life1_gensyou = False
        #2Pについて（移動、ライフ減少）
        player2_move = False             #プレイヤ1ーが動けるか    
        life2_gensyou = False

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN or event.type == QUIT:
                pygame.quit()
                sys.exit()

    pygame.draw.rect(screen, (0, 0, 0), (1250, 465, 75, 30))   #黒色指定
    timer_img = sysfont3.render(str(limit_time), True, (255,255,255))
    screen.blit(timer_img,(1250, 465))
        

        
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
    global p1_time, p2_time

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
        #スコアの計算方法解説
        screen.blit(finish_score_syousai,(150, 190))
        screen.blit(finish_score_syousai_2,(250, 220))
        #1Pフィニッシュスコアを画面に表示
        finish_score1_img = sysfont3.render("1P :  " + str(score1) + " + " + str(life1) + "×100 + " + str(p1_time) + "×20  =  " + str(finish_score1), True, (143,232,224))
        screen.blit(finish_score1_img,(150, 265))
        #2Pフィニッシュスコアを画面に表示
        finish_score2_img = sysfont3.render("2P :  " + str(score2) + " + " + str(life2) + "×100 + " + str(p2_time) + "×20  =  " + str(finish_score2), True, (143,232,224))
        screen.blit(finish_score2_img,(150, 310))
        if finish_score1 > finish_score2 :
            win_img = sysfont.render("1P WIN !!!", True, (143,232,224))
        elif finish_score1 < finish_score2 :
            win_img = sysfont.render("2P WIN !!!", True, (143,232,224))
        else :
            win_img = sysfont.render("DRAW !!!", True, (143,232,224))
        screen.blit(win_img,(300,365))
        font4 = sysfont3.render("Press  \"Enter\"  to exit Game", True, (255,255,255))
        screen.blit(font4,(200,430))
    def clear_show(self):
        """ウィンドウを表示"""
        self.clearwindow = True

# ゲームクリア用ウィンドウ
wnd = C_Window(Rect(96,96,672,384))     #ゲームクリア時にウィンドウ作成


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
        self.enemy_hyouzi = True
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
        global life1, life2
        global life1_gensyou, life2_gensyou
        global p1_time, p2_time

        if self.enemy_hyouzi == True:           #敵表示のスイッチオンで敵の描画
            screen.blit(self.image, (self.ex*size, self.ey*size))  # 敵描画
            #1Pが敵にあたった（ゲームオーバー）時
            if self.ex == x and self.ey == y and life1_gensyou == True:
                #当たった後には、スコアを黒で塗りつぶす。
                                      #　黒色　(左上x座標　左上y座標　横幅、縦幅)　
                pygame.draw.rect(screen, (0, 0, 0), (1070, 120, 60, 30))   #黒色指定
                if self.level == -1:
                    life1 = life1 - 1
                if self.level == -2:
                    life1 = life1 - 2
                if self.level == -3:
                    life1 = life1 - 3
                if self.level == -4:
                    life1 = life1 - 4
                if self.level == -5:
                    life1 = life1 - 5
                if self.level == 1:
                    life1 = life1 + 1
                self.enemy_hyouzi = False    #敵表示のスイッチオフ（敵表示を消す）。


                ########################
                #　クリア判定時
                ########################
                if life1 <= 0:
                    p1_time = 0 
                    life1 = 0
                    screen.blit(player_life_0,(950, 170))   #プレイヤーのウィンドウに　faild　表示
                    player_move = False             #プレイヤ1ーが動けるか        
                    life1_gensyou = False

            #2Pが敵にあたった（ゲームオーバー）時
            if self.ex == x2 and self.ey == y2 and life2_gensyou == True:
                #当たった後には、スコアを黒で塗りつぶす。
                                      #　黒色　(左上x座標　左上y座標　横幅、縦幅)　
                pygame.draw.rect(screen, (0, 0, 0), (1070, 330, 60, 30))   #黒色指定

                if self.level == -1:
                    life2 = life2 - 1
                if self.level == -2:
                    life2 = life2 - 2
                if self.level == -3:
                    life2 = life2 - 3
                if self.level == -4:
                    life2 = life2 - 4
                if self.level == -5:
                    life2 = life2 - 5
                if self.level == 1:
                    life2 = life2 + 1
                self.enemy_hyouzi = False    #敵表示のスイッチオフ（敵表示を消す）。


                ########################
                #　クリア判定時
                ########################
                if life2 <= 0:
                    p2_time = 0
                    life2 = 0
                    screen.blit(player_life_0,(950,380))    #プレイヤーのウィンドウに　faild　表示
                    player2_move = False             #プレイヤー2が動けるか
                    life2_gensyou = False


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
        global score1, score2, finish_score1, finish_score2, p1_time, p2_time

        if self.status == True:
            screen.blit(self.image, (self.ix*size, self.iy*size))  # アイテム描画            
            #プレイヤー1と座標一致したとき
            if self.ix == x and self.iy == y :       #1P用スコア
                #当たった後には、スコアを黒で塗りつぶす。
                                      #　黒色　(左上x座標　左上y座標　横幅、縦幅)　
                pygame.draw.rect(screen, (0, 0, 0), (1070, 70, 100, 30))   #黒色指定
                
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
                
            
            #プレイヤー2と座標一致したとき
            if self.ix == x2 and self.iy == y2:     #2P用スコア
                                  #　黒色　(左上x座標　左上y座標　横幅、縦幅)　
                pygame.draw.rect(screen, (0, 0, 0), (1070, 280, 100, 30))   #黒色指定
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
            
            
            #####################
            #　総合スコア計算
            #####################
            finish_score1 = score1 + life1 * 100 + p1_time * 30
            finish_score2 = score2 + life2 * 100 + p2_time * 30


######################
#　スコア・ライフ表示
######################
def score_show(screen):
    global score1, score2, life1, life2

    #画面に表示
    score1_img = sysfont3.render(str(score1), True, (255,255,255))
    screen.blit(score1_img,(1080, 70))
    score2_img = sysfont3.render(str(score2), True, (255,255,255))
    screen.blit(score2_img,(1080, 280))
    #########################
    #ライフ表示用フォント作成
    #########################
    life1_img = sysfont3.render(str(life1), True, (255,255,255))
    screen.blit(life1_img,(1080, 120))
    life2_img = sysfont3.render(str(life2), True, (255,255,255))
    screen.blit(life2_img,(1080, 330))

def main():
    #画面の生成
    DISP_WIDTH  = 1350   #864(mapのみ)     #画面の横サイズ
    DISP_HEIGHT = 675    #576(mapのみ)     #画面の縦サイズ
    pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT)) #FULLSCREEN　でフルスクリーン表示
    screen = pygame.display.get_surface()
    pygame.display.set_caption("GAME")


    #########################
    #   データ読み込み
    #########################
    """ここで壁や床、プレイあーの情報と、迷路の外の画面で使う解説用画像の読み込み"""
    #背景（薄ピンク）表示
    pygame.draw.rect(screen, (208, 170, 255), (10, 580, 854, 90))   #黒色指定
    #　壁、プレイヤー系
    yukaImg = pygame.image.load("yuka.gif").convert()         # 床
    kabeImg = pygame.image.load("kabe.png").convert()           # 壁
    player = pygame.image.load("poodle.gif").convert()
    player2 = pygame.image.load("poodle2.gif").convert()
    goal = pygame.image.load("bone.gif").convert()
    # エネミー系画像読み込み　＆　表示
    #敵1
    catImg = pygame.image.load("cat.gif").convert()
    screen.blit(catImg, (20, 590))
    e1_life_font = sysfont4.render("... -1", True, (0, 0, 0))
    screen.blit(e1_life_font,(60, 590))
    #敵2
    tanukiImg = pygame.image.load("tanuki.gif").convert()
    screen.blit(tanukiImg, (20, 630))
    e2_life_font = sysfont4.render("... -2", True, (0, 0, 0))
    screen.blit(e2_life_font,(60, 630))
    #敵3
    kangarooImg = pygame.image.load("kangaroo.gif").convert()
    screen.blit(kangarooImg, (140, 590))
    e3_life_font = sysfont4.render("... -3", True, (0, 0, 0))
    screen.blit(e3_life_font,(180, 590))
    #敵4
    inoshishiImg = pygame.image.load("inoshishi.gif").convert()
    screen.blit(inoshishiImg, (140, 630))
    e4_life_font = sysfont4.render("... -4", True, (0, 0, 0))
    screen.blit(e4_life_font,(180, 630))
    #敵5
    eagleImg = pygame.image.load("eagle.gif").convert()
    screen.blit(eagleImg, (260, 590))
    e5_life_font = sysfont4.render("... -5", True, (0, 0, 0))
    screen.blit(e5_life_font,(300, 590))
    #敵6
    nyuusankinImg = pygame.image.load("nyuusankin.gif").convert()
    screen.blit(nyuusankinImg, (260, 630))
    e5_life_font = sysfont4.render("... +1", True, (0, 0, 0))
    screen.blit(e5_life_font,(300, 630))    

    #　アイテム系画像読み込み
    #アイテム１
    iceImg = pygame.image.load("ice.gif").convert()
    screen.blit(iceImg, (575, 590))
    item1_score_font = sysfont4.render("... +100", True, (0, 0, 0))
    screen.blit(item1_score_font,(605, 590))
    #アイテム２
    softImg = pygame.image.load("soft.gif").convert()
    screen.blit(softImg, (575, 630))
    item1_score_font = sysfont4.render("... +150", True, (0, 0, 0))
    screen.blit(item1_score_font,(605, 630))
    #アイテム３
    water_mImg = pygame.image.load("water-m.gif").convert()
    screen.blit(water_mImg, (725, 590))
    item1_score_font = sysfont4.render("... +200", True, (0, 0, 0))
    screen.blit(item1_score_font,(755, 590))
    #アイテム４
    pinImg = pygame.image.load("pin.gif").convert()
    screen.blit(pinImg, (725, 630))
    item1_score_font = sysfont4.render("... +300", True, (0, 0, 0))
    screen.blit(item1_score_font,(755, 630))


    #　　〇〇〇　スコア、タイムの文字表示　〇〇〇
    screen.blit(font_player1,(900, 20))
    screen.blit(font_score,(920, 70))
    screen.blit(font_life,(920, 120))

    screen.blit(font_player2,(900, 230))
    screen.blit(font_score,(920, 280))
    screen.blit(font_life,(920, 330))

    screen.blit(font_time,(1120, 465))

    #スコア計算方法についての表示
    screen.blit(finish_score_syousai,(890, 610))
    screen.blit(finish_score_syousai_2,(950, 640))

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
    enemy1 = enemy("cat.gif", 13, 16, -1)
    enemy2 = enemy("cat.gif", 9, 7, -1)
    enemy3 = enemy("cat.gif", 12, 2, -1)
    enemy4 = enemy("tanuki.gif", 4, 4, -2)
    enemy5 = enemy("tanuki.gif", 24, 4, -2)
    enemy6 = enemy("tanuki.gif", 23, 15, -2)
    enemy7 = enemy("kangaroo.gif", 21, 1, -3)
    enemy8 = enemy("kangaroo.gif", 17, 9, -3)
    enemy9 = enemy("inoshishi.gif", 19, 10, -4)
    enemy10 = enemy("inoshishi.gif", 2, 15, -4)
    enemy11 = enemy("cat.gif", 3, 8, -1)
    enemy12 = enemy("cat.gif", 9, 2, -1)
    enemy13 = enemy("kangaroo.gif", 12, 10, -3)
    enemy14 = enemy("inoshishi.gif", 23, 13, -4)
    enemy15 = enemy("eagle.gif", 24, 16, -5)
    enemy16 = enemy("cat.gif", 4, 12, -1)
    enemy17 = enemy("cat.gif", 8, 6, -1)
    enemy18 = enemy("cat.gif", 23, 7, -1)
    enemy19 = enemy("cat.gif", 21, 10, -1)
    enemy20 = enemy("cat.gif", 17, 13, -1)

    kaifuku1 = enemy("nyuusankin.gif", 6, 16, 1)
    kaifuku2 = enemy("nyuusankin.gif", 15, 2, 1)
    #敵の動きを読み込む
    schedule.every(0.5/60).minutes.do(enemy1.enemy_move)          #時間指定は分単位（＝ 0.5 秒）
    schedule.every(0.5/60).minutes.do(enemy2.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy3.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy4.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy5.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy6.enemy_move)
    schedule.every(1/60).minutes.do(enemy7.enemy_move)            #時間指定は分単位（＝ 1 秒）
    schedule.every(1/60).minutes.do(enemy8.enemy_move)
    schedule.every(1/60).minutes.do(enemy9.enemy_move)
    schedule.every(1/60).minutes.do(enemy10.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy11.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy12.enemy_move)
    schedule.every(1/60).minutes.do(enemy13.enemy_move)
    schedule.every(1/60).minutes.do(enemy14.enemy_move)
    schedule.every(0.2/60).minutes.do(enemy15.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy16.enemy_move) 
    schedule.every(0.5/60).minutes.do(enemy17.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy18.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy19.enemy_move)
    schedule.every(0.5/60).minutes.do(enemy20.enemy_move)

    #画面更新のための時計をセット
    clock = pygame.time.Clock()




    while (1):
        global x,y,x2,y2            #各プレイヤーの座標
        global player_move, player2_move
        global life1_gensyou, life2_gensyou
        global p1_time, p2_time, limit_time
        global p1_clear, p2_clear

        clock.tick(60)      #画像の移動処理

        draw_map(screen)                         #マップ描画
        screen.blit(player, (x*size,y*size))     # プレイヤー1描画
        screen.blit(player2, (x2*size,y2*size))  # プレイヤー2描画
        screen.blit(goal, (25*size,16*size))     # ゴール描画

        timer(screen)

        ##################################################
        #当たり判定後、スコア・ライフを塗りつぶし、計算
        #スプライト判定無効化＆表示
        ##################################################
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

        ###################################
        #スコア・ライフを文字列変換、表示
        ###################################
        score_show(screen)


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
        enemy11.atari(screen)
        enemy12.atari(screen)
        enemy13.atari(screen)
        enemy14.atari(screen)
        enemy15.atari(screen)
        enemy16.atari(screen)
        enemy17.atari(screen)
        enemy18.atari(screen)
        enemy19.atari(screen)
        enemy20.atari(screen)
        kaifuku1.atari(screen)
        kaifuku2.atari(screen)
        
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


            #########################
            #ゴール判定の条件設定
            #########################
            a =     x == 25 and y == 16         #　1Pゴール
            b =     x2 == 25 and y2 == 16
            #b =     x2 == 25 and y2 == 16       #　2Pゴール
            c =     life1 == 0                  #　1Pライフゼロ
            d =     life2 == 0                  #　2Pライフゼロ
            #########################
            #ゴール時の当たり判定
            #########################
            if a:
                if p1_clear == False:
                    p1_time = limit_time
                    p1_clear = True
                player_move = False
                life1_gensyou = False        #ライフ計算時に無効、キーボード判定後に有効（そのマスではダメージが動かない限り減らないようにするためのスイッチ）
                screen.blit(player_clear,(950, 170))
            if b:
                if p2_clear == False:
                    p2_time = limit_time
                    p2_clear = True
                player2_move = False
                life2_gensyou = False        #ライフ計算時に無効、キーボード判定後に有効（そのマスではダメージが動かない限り減らないようにするためのスイッチ）
                screen.blit(player_clear,(950, 380))
                #    同時ゴール　　　1Pゴール　　　　2Pゴール　　　　1,2Pライフ0
            if   a and b   or   a and d   or   b and c   or   c and d:     
                wnd.clear_show()  # ウィンドウの描画
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

if __name__ == "__main__":
    main()