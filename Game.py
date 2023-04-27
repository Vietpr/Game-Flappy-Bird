
import pygame, sys, random

def creat_floor():    
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))

def creat_tubes():
    random_tubes = random.choice(tubes_height)
    down_tubes = tubes_surface.get_rect(midtop =(500,random_tubes))
    up_tubes = tubes_surface.get_rect(midtop =(500,random_tubes - 650))
    return down_tubes, up_tubes

def move_tubes(tubes):
    for tube in tubes:
        tube.centerx -= 5
    return tubes 

def draw_tube(tubes):
    for tube in tubes:
        if tube.bottom >= 600:
            screen.blit(tubes_surface,tube)
        else:
            flip_tubes = pygame.transform.flip(tubes_surface,False,True)
            screen.blit(flip_tubes,tube)

def check_collide(tubes):
    for tube in tubes:
        if bird_rect.colliderect(tube):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            return False
    return True

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*1,1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,630))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
# Tạo Khung (create framing)
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen= pygame.display.set_mode((432,768)) 

# Xét FPS 
hour = pygame.time.Clock()
# tạo font chữ (font creation)
game_font = pygame.font.Font("Flappy Bird/04B_19.TTF", 35)

# tạo biến (create variable)
gravity = 0.25 
bird_movement = 0 
game_active = True

# tạo điểm (make points)
score = 0
high_score = 0

# Chèn background (background inserts)
background = pygame.image.load("Flappy Bird/image/2c86e1bfc5fb35f33195c6cfcfdff551 (1).jpg").convert()
#background = pygame.transform.scale2x(background)   # zoom background

# chèn sàn (floor inserts)
floor = pygame.image.load("Flappy Bird/image/floor.png").convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# tạo chim (create bird)
bird_down = pygame.transform.scale2x(pygame.image.load("Flappy Bird/image/yellowbird-downflap.png")).convert_alpha()
bird_mid = pygame.transform.scale2x(pygame.image.load("Flappy Bird/image/yellowbird-midflap.png")).convert_alpha()
bird_up = pygame.transform.scale2x(pygame.image.load("Flappy Bird/image/yellowbird-upflap.png")).convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
#bird = pygame.image.load("Flappy Bird/image/yellowbird-midflap.png").convert_alpha()
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100, 384))  #get_rect: creat a rectangle around the bird

# Tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

# Tạo ống (create tubes)
tubes_surface = pygame.image.load("Flappy Bird/image/pipe-green.png").convert()
tubes_surface = pygame.transform.scale2x(tubes_surface)
tubes_list = []

# tạo thời gian ống xuất hiện
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 2200) #sau 1,2s tạo ra 1 ống mới
tubes_height = [300,420,550]

# tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load("Flappy Bird/image/message.png")).convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(216,384))

# chèn âm thanh
flap_sound = pygame.mixer.Sound('Flappy Bird/Music/5_Flappy_Bird_sound_sfx_wing.wav')
hit_sound = pygame.mixer.Sound('Flappy Bird/Music/5_Flappy_Bird_sound_sfx_hit.wav')
score_sound = pygame.mixer.Sound('Flappy Bird/Music/5_Flappy_Bird_sound_sfx_point.wav')
score_sound_countdown = 100
# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # create keypress on keyboard
            if event.key == pygame.K_SPACE and game_active:  # use the space control the bird up or down
                bird_movement = 0
                bird_movement = -11
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                tubes_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            tubes_list.extend(creat_tubes())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
            
            
    screen.blit(background,(0,0))
    # bird 
    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collide(tubes_list)
        # pipe
        tubes_list = move_tubes(tubes_list)
        draw_tube(tubes_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score,high_score)
        score_display("game_over")

    # floor( sàn)
    floor_x_pos -=1   # move the floor
    creat_floor()
    if floor_x_pos <= -432:
        floor_X_pos = 0
    pygame.display.update()
    hour.tick(120)
    

