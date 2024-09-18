#1.主菜单（开始游戏，退出游戏，神秘商店，排行榜）
#2.设置关卡，第一关，第二关，第三关....
#3.增加倒计时
#4.增加游戏中的道具(撤销，提示，重排)
#5.点击方块时的音效 和 鼠标移动到方块上的特效、音效
import pygame
from game import initialize_tiles_level1,initialize_tiles_level2, initialize_tiles_level3,game_logic, draw_game, get_rankings,tiles, docks

# 初始化 Pygame
pygame.init()

# 定义屏幕宽高
WIDTH, HEIGHT = 600, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('球了个球')

# 游戏状态
MENU = 'menu'
RANK = 'rank'
SHOP = 'shop'
GAME = 'game'
LOSE = 'lose'
WIN = 'win'
level = 1
game_state = MENU
# 音乐处理
try:
    music = pygame.mixer.Sound('music/bgm.mp3')
    music.play(-1)
except pygame.error as e:
    print(f"音乐加载失败: {e}")

# 初始化音效
hover_sound = pygame.mixer.Sound('music/hover.wav')
hover_played = False  # 悬停音效标志

# 处理悬停特效和音效的函数
def handle_hover_effect():
    global hover_played
    mouse_pos = pygame.mouse.get_pos()

    for tile in tiles:
        if tile.collidepoint(mouse_pos):
            # 绘制绿色边框特效
            pygame.draw.rect(screen, (0, 255, 0), tile, 5)
            if not hover_played:
                hover_sound.play()
                hover_played = True
        else:
            pygame.draw.rect(screen, (255, 255, 255), tile, 0)
            hover_played = False  # 重置音效播放标志

# 主菜单绘制
def draw_menu():
    screen.fill((255, 255, 255))
    # 背景图片
    image = pygame.image.load('images/menu.jpg')
    screen.blit(image, (0, 0, WIDTH, HEIGHT))
    # 标题和字体
    font = pygame.font.SysFont('华文中宋', 60)
    title = font.render("球了个球", True, (115, 115, 200))
    screen.blit(title, (180, 10))
    font = pygame.font.SysFont('华文中宋', 40)
    # 排行榜按钮
    rank_button = pygame.Rect(200, 300, 200, 80)
    pygame.draw.rect(screen, (115, 115, 200), rank_button)
    rank_text = font.render("排行榜", True, (255, 255, 255))
    screen.blit(rank_text, (rank_button.x + 40, rank_button.y + 10))
    # 商店按钮
    shop_button = pygame.Rect(200, 400, 200, 80)
    pygame.draw.rect(screen, (115, 115, 200), shop_button)
    shop_text = font.render("神秘商店", True, (255, 255, 255))
    screen.blit(shop_text, (shop_button.x + 20, shop_button.y + 10))
    # 开始游戏按钮
    start_button = pygame.Rect(200, 500, 200, 80)
    pygame.draw.rect(screen, (115, 115, 200), start_button)
    start_text = font.render("开始游戏", True, (255, 255, 255))
    screen.blit(start_text, (start_button.x + 20, start_button.y + 10))
    # 退出游戏按钮
    quit_button = pygame.Rect(200, 600, 200, 80)
    pygame.draw.rect(screen, (115, 115, 200), quit_button)
    quit_text = font.render("退出游戏", True, (255, 255, 255))
    screen.blit(quit_text, (quit_button.x + 20, quit_button.y + 10))
    return rank_button, shop_button, start_button, quit_button

# 失败界面绘制
def draw_lose():
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont('华文中宋', 40)
    end_text = font.render("游戏结束", True, (255, 0, 0))
    screen.blit(end_text, (200, 150))

    # 再来一次按钮
    retry_button = pygame.Rect(200, 300, 200, 80)
    pygame.draw.rect(screen, (0, 0, 0), retry_button)
    retry_text = font.render("再来一次", True, (255, 255, 255))
    screen.blit(retry_text, (retry_button.x + 20, retry_button.y + 10))

    # 返回主菜单按钮
    menu_button = pygame.Rect(200, 400, 200, 80)
    pygame.draw.rect(screen, (0, 0, 0), menu_button)
    menu_text = font.render("返回主菜单", True, (255, 255, 255))
    screen.blit(menu_text, (menu_button.x + 1, menu_button.y + 10))
    return retry_button, menu_button

# 胜利界面绘制
def draw_win():

    screen.fill((255, 255, 255))
    font = pygame.font.SysFont('华文中宋', 40)
    win_text = font.render("胜利！", True, (0, 255, 0))
    screen.blit(win_text, (200, 150))

    # 提示点击鼠标左键进入下一关
    next_level_text = font.render("点击鼠标左键进入下一关", True, (0, 0, 0))
    screen.blit(next_level_text, (100, 300))

# 排行榜界面绘制
def draw_rankings():
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont('华文中宋', 40)
    title = font.render("排行榜", True, (0, 0, 0))
    screen.blit(title, (200, 100))
    
    # 显示前10名的分数
    rankings_list = get_rankings()
    for idx, score in enumerate(rankings_list):
        score_text = font.render(f"{idx + 1}. {score}分", True, (0, 0, 0))
        screen.blit(score_text, (200, 150 + idx * 40))

    # 返回主菜单按钮
    menu_button = pygame.Rect(200, 600, 200, 80)
    pygame.draw.rect(screen, (0, 0, 0), menu_button)
    menu_text = font.render("返回主菜单", True, (255, 255, 255))
    screen.blit(menu_text, (menu_button.x + 1, menu_button.y + 10))
    
    return menu_button


# 初始化主菜单按钮和结束界面按钮
rank_button, shop_button, start_button, quit_button = draw_menu()
retry_button, menu_button = None, None


# 主循环
running = True
while running:
    # 绘制不同状态的界面
    if game_state == MENU:
        draw_menu()  # 仅绘制一次主菜单
    elif game_state == RANK:
        menu_button = draw_rankings()
    elif game_state == SHOP:
        pass
    elif game_state == GAME:
        draw_game(level)
        handle_hover_effect()  # 添加鼠标悬停特效和音效
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        # 设置 game_state 状态，以及鼠标点击事件
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # 主菜单下的点击事件
            if game_state == MENU:
                if rank_button.collidepoint(pos):
                    game_state = RANK
                elif shop_button.collidepoint(pos):
                    game_state = SHOP
                elif start_button.collidepoint(pos):
                    game_state = GAME
                    initialize_tiles_level1()  # 初始化游戏
                elif quit_button.collidepoint(pos):
                    running = False

            # 排行榜下的点击事件
            elif game_state == RANK:
                if menu_button.collidepoint(pos):
                    game_state = MENU
                    
            # 游戏中的点击事件
            elif game_state == GAME:
                game_state = game_logic(event,level)
                # 检查游戏结束
                if game_state == LOSE:
                    retry_button, menu_button = draw_lose()
                    level = 1  # 重新开始游戏
                if game_state == WIN:
                    draw_win()

            # 失败界面下的点击事件
            elif game_state == LOSE:
                if retry_button.collidepoint(pos):
                    game_state = GAME
                    if level ==1:  # 再来一次，重新初始化游戏
                        initialize_tiles_level1()
                    elif level == 2:
                        initialize_tiles_level2()
                    elif level == 3:
                        initialize_tiles_level3()
                elif menu_button.collidepoint(pos):
                    game_state = MENU

            # 胜利界面下的点击事件
            elif game_state == WIN:
                game_state = GAME
                level += 1  # 进入下一关
                if level ==2:  # 初始化下一关卡的游戏
                    initialize_tiles_level2()
                elif level == 3:
                    initialize_tiles_level3()   
            


    pygame.display.flip()

pygame.quit()
