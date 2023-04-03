import pygame
import random

pygame.init()

# 기본 설정
size = [614, 426]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Solar System Dash")

# 이미지 로드
gamestart = pygame.image.load("data\gamestart.jpeg")
gameover = pygame.image.load("data\gameover.jpeg")
gameclear = pygame.image.load("data\gameclear.jpeg")
stage1 = pygame.image.load("data\stage1.png").convert_alpha()
stage2 = pygame.image.load("data\stage2.png").convert_alpha()
stage3 = pygame.image.load("data\stage3.png").convert_alpha()
stage4 = pygame.image.load("data\stage4.png").convert_alpha()
stage5 = pygame.image.load("data\stage5.png").convert_alpha()
stage6 = pygame.image.load("data\stage6.png").convert_alpha()
stage7 = pygame.image.load("data\stage7.png").convert_alpha()
stage8 = pygame.image.load("data\stage8.png").convert_alpha()
stage9 = pygame.image.load("data\stage9.png").convert_alpha()
stage1b = pygame.image.load("data\stage1b.jpg")
stage2b = pygame.image.load("data\stage2b.jpg")
stage3b = pygame.image.load("data\stage3b.jpg")
stage4b = pygame.image.load("data\stage4b.jpg")
stage5b = pygame.image.load("data\stage5b.jpg")
stage6b = pygame.image.load("data\stage6b.jpg")
stage7b = pygame.image.load("data\stage7b.jpg")
stage8b = pygame.image.load("data\stage8b.jpg")
stage9b = pygame.image.load("data\stage9b.jpg")

s_list = [0, stage1, stage2, stage3, stage4, stage5, stage6, stage7, stage8, stage9]
sb_list = [0, stage1b, stage2b, stage3b, stage4b, stage5b, stage6b, stage7b, stage8b, stage9b]

class Obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
    def put_img(self, address):
        if address[-3:] == 'png':
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
            self.img_x, self.img_y = self.img.get_size()
    def change_size(self, img_x, img_y):
        self.img = pygame.transform.scale(self.img, (img_x, img_y))
        self.img_x, self.img_y = self.img.get_size()
    def show(self):
        screen.blit(self.img, (self.x, self.y))

class Items:
    def __init__(self, img_adr, img_x, img_y, move):
        self.item_list = []
        self.item2_list = []
        self.img_adr = img_adr
        self.img_x = img_x
        self.img_y = img_y
        self.move = move
    def add_object(self, spaceship):
        o = Obj()
        o.put_img(self.img_adr)
        o.change_size(self.img_x, self.img_y)
        o.x = size[0]
        o.y = random.randrange(0, size[1] - o.img_y)
        o.move = self.move
        self.item_list.append(o)
    def move_all(self):
        d_list = []
        for i in range(len(self.item_list)):
            o = self.item_list[i]
            o.x -= self.move
            if o.x <= 0:
                d_list.append(i)
        d_list.reverse()
        for d in d_list:
            del self.item_list[d]
    def crash(self, spaceship):
        for i in range(len(self.item_list)):
            o = self.item_list[i]
            if crash(o, spaceship) == True:
                del self.item_list[i]
                return True
        return False
    def show(self):
        for i in self.item_list:
            i.show()

class Missiles(Items):
    def __init__(self, img_adr, img_x, img_y, move):
        super().__init__(img_adr, img_x, img_y, move)
    def add_object(self, spaceship):
        o = Obj()
        o.put_img(self.img_adr)
        o.change_size(self.img_x, self.img_y)
        o.x = spaceship.img_x + o.img_x + 10
        o.y = round(spaceship.y + spaceship.img_y/2 - o.img_y/2)
        o.move = self.move
        self.item_list.append(o)
    def move_all(self):
        d_list = []
        for i in range(len(self.item_list)):
            o = self.item_list[i]
            o.x += self.move
            if o.x >= size[0]:
                d_list.append(i)
        d_list.reverse()
        for d in d_list:
            del self.item_list[d]
    def crash(self, obstacles2):
        for i in range(len(self.item_list)):
            for j in range(len(obstacles2.item_list)):
                o = self.item_list[i]
                o2 = obstacles2.item_list[j]
                if crash(o, o2) == True:
                    del self.item_list[i]
                    del obstacles2.item_list[j]
                    return True
        return False

def crash(a, b):
    if (a.x - b.img_x <= b.x) and (b.x <= a.x + a.img_x):
        if (a.y - b.img_y <= b.y) and (b.y <= a.y + a.img_y):
            return True
        else:
            return False
    else:
        return False

def initialize_spaceship():
    spaceship = Obj()
    spaceship.put_img("data\spaceship.png")
    spaceship.change_size(60,30)
    spaceship.x = size[0] - 9.5*spaceship.img_x
    spaceship.y = round(size[1]/2 - spaceship.img_y/2)
    spaceship.move = 4
    return spaceship

def top_score(score):
    f = open("data/topscore.txt", 'r')
    topscore = int(f.read().strip())
    f.close()
    if score >= topscore:
        topscore = score
        f = open("data/topscore.txt", 'w')
        f.write(str(topscore))
        f.close()
    return topscore

def playing():
    clock = pygame.time.Clock()
    run = True
    game_status = 'ready'
    game_stage = 0
    
    down_go = False
    up_go = False
    space_go = False
    boostmode = False
    unbeatable = False
    count = 0
    countb = 0
    countc = 0
    life = 0
    score = 0
    m = 0
    stage_time = [0, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
    stageo_move = [0, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
    stagehb_move = [0, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7]
    stagea_move = [0, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5]

    while run:
        clock.tick(60)
        count += 1

        if game_status == 'ready':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_status = 'playing'
            screen.blit(gamestart, (0, 0))
            pygame.display.update()
        elif game_status == 'playing':
            if game_stage == 0:
                spaceship = initialize_spaceship()
                count60 = count
                game_stage += 1
                score = 0
                #오브젝트 초기화
                obstacles = Items("data\obstacle.png", 48, 50, 2)
                obstacles2 = Items("data\obstacle2.png", 35, 30, 2)
                hearts = Items("data\heart.png", 20, 20, 3)
                boosters = Items(r"data\booster.png", 20, 25, 3)
                asteroids = Items("data\asteroid.png", 45, 40, 2.5)
                missiles = Missiles("data\missile.png", 25, 7, 5)
                font = pygame.font.SysFont("ariblk", 25, False, False)
                font2 = pygame.font.SysFont("arialbd", 35, False, False)
                h_font = pygame.font.SysFont("segoeuisymbol", 20)
                p_font = pygame.font.SysFont("notosanscjkkrblack", 25)
            elif game_stage >= 1:
                #키보드 입력 처리
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            down_go = True
                        elif event.key == pygame.K_UP:
                            up_go = True
                        elif event.key == pygame.K_SPACE:
                            space_go = True
                            m = 0
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            down_go = False
                        elif event.key == pygame.K_UP:
                            up_go = False
                        elif event.key == pygame.K_SPACE:
                            space_go = False
                if down_go == True:
                    spaceship.y += spaceship.move
                    if spaceship.y >= size[1] - spaceship.img_y:
                        spaceship.y = size[1] - spaceship.img_y
                elif up_go == True:
                    spaceship.y -= spaceship.move
                    if spaceship.y <= 0:
                        spaceship.y = 0
                        
                if space_go == True and m % 6 == 0:
                    missiles.add_object(spaceship)
                    missiles.x = spaceship.img_x - missiles.img_x - 10
                    missiles.y = round(spaceship.img_y + spaceship.img_y/2 - missiles.img_y/2)
                missiles.move_all()
                m += 1

                #오브젝트 충돌 처리
                if boosters.crash(spaceship) == True:
                    countb = count
                    boostmode = True
                    obstacles.move = 9
                    obstacles2.move = 9
                    hearts.move = 9
                    boosters.move = 9
                    asteroids.move = 9
                if boostmode == True:
                        score += 5
                if obstacles.crash(spaceship) == True or obstacles2.crash(spaceship) == True or asteroids.crash(spaceship) == True:
                    if boostmode == True or unbeatable == True:
                        pass
                    elif life > 0:
                        unbeatable = True
                        countc = count
                        life -= 1
                    else:
                        game_status = 'gameover'
                if unbeatable == True and count - countc >= 60:
                    unbeatable = False
                if hearts.crash(spaceship) == True and boostmode == False:
                    life += 1
                if count - countb >= 180:
                    boostmode = False
                    obstacles.move = stageo_move[game_stage]
                    obstacles2.move = stageo_move[game_stage]
                    hearts.move = stagehb_move[game_stage]
                    boosters.move = stagehb_move[game_stage]
                    asteroids.move = stagea_move[game_stage]
                if missiles.crash(obstacles2) == True:
                    score += 1000
                
                #오브젝트 생성 및 이동
                if random.random() > 0.985 and count - count60 >= 60 and count - count60 < stage_time[game_stage] - 300:
                    obstacles.add_object(spaceship)
                    obstacles2.add_object(spaceship)
                obstacles.move_all()
                obstacles2.move_all()
                if random.random() > 0.995 and count - count60 >= 60 and count - count60 < stage_time[game_stage] - 300:
                    if game_stage == 4 or game_stage == 5:
                        asteroids.add_object(spaceship)
                asteroids.move_all()
                if random.random() > 0.997 and count - count60 >= 60 and count - count60 < stage_time[game_stage] - 300:
                    hearts.add_object(spaceship)
                    boosters.add_object(spaceship)
                hearts.move_all()
                boosters.move_all()
                    
                #스테이지 전환
                if count - count60 > stage_time[game_stage]:
                    if game_stage == 9:
                        game_status = 'gameclear'
                    else:
                        game_stage += 1
                        spaceship.y = round(size[1]/2 - spaceship.img_y/2)
                        obstacles.move = stageo_move[game_stage]
                        obstacles2.move = stageo_move[game_stage]
                        hearts.move = stagehb_move[game_stage]
                        boosters.move = stagehb_move[game_stage]
                        asteroids.move = stagea_move[game_stage]
                        count60 = count
                        life = 0
                        boostmode = False
                
                #화면 표시
                screen.blit(sb_list[game_stage], (0, 0))
                if count - count60 < 60:
                    screen.blit(s_list[game_stage], (0, 0))
                if unbeatable == True and count % 10 <= 4:
                    pass
                else:
                    spaceship.show()
                obstacles.show()
                obstacles2.show()
                hearts.show()
                missiles.show()
                boosters.show()
                asteroids.show()
                heart_string = u"\u2665" * (life+1)
                heart_width, _ = h_font.size(heart_string)
                text_heart = h_font.render(heart_string, True, (255,255,255))
                screen.blit(text_heart, (10, 0))
                text_s = font.render("SCORE: {}".format(score), True, (255,255,255))
                screen.blit(text_s, (20 + heart_width, 7))
                
                pygame.display.update()
        elif game_status == 'gameover':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_status = 'playing'
                    game_stage = 0
                    down_go = False
                    up_go = False
                    space_go = False
            screen.blit(gameover, (0, 0))
            text_ts = font2.render("TOP SCORE: {}".format(top_score(score)), True, (255,255,255))
            text_s = font2.render("SCORE: {}".format(score), True, (255,255,255))
            screen.blit(text_ts, (10, 5))
            screen.blit(text_s, (10, 35))
            pygame.display.update()
        elif game_status == 'gameclear':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_status = 'ready'
                    game_stage = 0
                    down_go = False
                    up_go = False
                    space_go = False
                    count = 0
                    life = 0
            screen.blit(gameclear, (0, 0))
            text_ts = font2.render("TOP SCORE: {}".format(top_score(score)), True, (255,255,255))
            text_s = font2.render("SCORE: {}".format(score), True, (255,255,255))
            screen.blit(text_ts, (10, 5))
            screen.blit(text_s, (10, 35))
            pygame.display.update()
            

playing()

pygame.quit()
