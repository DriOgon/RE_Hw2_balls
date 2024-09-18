import pygame
import random
# from config import level

GAME ='game'
WIN = 'win'
LOSE = 'lose'

# 分数初始化
score = 0

# 定义屏幕
WIDTH, HEIGHT = 600, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 游戏资源
background = pygame.image.load('images/back.png')
mask = pygame.image.load('images/mask.png')
end_screen = pygame.image.load('images/end.png')
win_screen = pygame.image.load('images/win.png')

# 牌组初始化
T_WIDTH, T_HEIGHT = 60, 66
DOCK_RECT = pygame.Rect(90, 564, T_WIDTH * 7, T_HEIGHT)

tiles = []# 所有的牌
docks = []# 下方的牌堆
# 初始化排行榜列表
rankings = []
def get_rankings():
    return rankings
# 更新排行榜函数
def update_rankings(score):
    global rankings
    rankings.append(score)
    rankings = sorted(rankings, reverse=True)[:10]  # 只保留前10名

# 随机生成牌 存到tiles中
# 第一关：只有一个平层，没有覆盖
def initialize_tiles_level1():
    global tiles
    tiles = []
    ts = list(range(1, 13)) * 3  # 根据需要减少牌的数量
    random.shuffle(ts)
    n = 0
    rows = 6  # 控制行数
    cols = 6  # 控制列数

    # 在平面上布局牌，没有层次
    for i in range(rows):
        for j in range(cols):
            if n >= len(ts):
                break
            t = ts[n]
            n += 1
            tile_img = pygame.image.load(f'images/tile{t}.png')
            tile = {
                'image': tile_img,
                'rect': tile_img.get_rect(),  # 牌的位置用于碰撞检测
                'tag': t,  # 牌的标签1-12
                'layer': 0,  # 没有层次
                'status': 1  # 所有牌可点击
            }
            tile['rect'].topleft = (100 + j * tile_img.get_width(),
                                    100 + i * tile_img.get_height() * 0.9)
            tiles.append(tile)

# 第二关：金字塔
def initialize_tiles_level2():
    global tiles
    tiles = []
    ts = list(range(1, 13)) * 12
    random.shuffle(ts)
    n = 0
    for k in range(7): # 7层
        for i in range(7 - k): # 行
            for j in range(7 - k): # 列
                t = ts[n]
                n += 1
                tile_img = pygame.image.load(f'images/tile{t}.png')
                tile = {
                    'image': tile_img,
                    'rect': tile_img.get_rect(), # 牌的位置用于碰撞检测
                    'tag': t,   # 牌的标签1-12
                    'layer': k, # 牌的层数
                    'status': 1 if k == 6 else 0  # 只有最上层的牌可点击
                }
                tile['rect'].topleft = (120 + (k * 0.5 + j) * tile_img.get_width(),
                                        100 + (k * 0.5 + i) * tile_img.get_height() * 0.9)
                tiles.append(tile)
    # 将多余的4张牌放到下面
    for i in range(4):
        t = ts[n]
        n += 1
        tile_img = pygame.image.load(f'images/tile{t}.png')
        tile = {
            'image': tile_img,
            'rect': tile_img.get_rect(topleft=(210 + i * tile_img.get_width(), 516)),
            'tag': t,
            'layer': 0,
            'status': 1
        }
        tiles.append(tile)

# 第三关：更复杂的布局和更多层次
def initialize_tiles_level3():
    global tiles
    tiles = []
    
    # 计算总共需要的牌数
    total_tiles_needed = sum((9 - k) ** 2 for k in range(9)) + 6  # 每层和底部的独立牌
    ts = list(range(1, 13)) * ((total_tiles_needed // 12) + 1)  # 根据需要重复生成牌
    random.shuffle(ts)
    n = 0
    layer_offsets = [0, 0.5, 1.0]  # 控制每层牌的偏移，制造更复杂的布局

    y_offset = -30  # 向上移动 50 像素
    x_offset = -80  # 向左移动 30 像素

    # 9层的复杂布局，每层牌数量不同
    for k in range(9):  # 9层
        offset = layer_offsets[k % len(layer_offsets)]  # 使用偏移
        rows = 9 - k  # 行数随层数减少
        cols = 9 - k  # 列数随层数减少
        for i in range(rows):  # 行
            for j in range(cols):  # 列
                if n >= total_tiles_needed:
                    break
                t = ts[n]
                n += 1
                tile_img = pygame.image.load(f'images/tile{t}.png')
                tile = {
                    'image': tile_img,
                    'rect': tile_img.get_rect(),  # 牌的位置用于碰撞检测
                    'tag': t,  # 牌的标签1-12
                    'layer': k,  # 牌的层数
                    'status': 1 if k == 8 else 0  # 只有最上层的牌可点击
                }
                # 左移和上移 tile 的 X 和 Y 坐标
                tile['rect'].topleft = (120 + (offset + j) * tile_img.get_width() + x_offset,
                                        50 + (offset + i) * tile_img.get_height() * 0.9 + y_offset)
                tiles.append(tile)

    # 在底部随机放一些独立的牌
    for i in range(6):
        t = ts[n]
        n += 1
        tile_img = pygame.image.load(f'images/tile{t}.png')
        tile = {
            'image': tile_img,
            'rect': tile_img.get_rect(topleft=(random.randint(100, 500) + x_offset, random.randint(500, 600) + y_offset)),
            'tag': t,
            'layer': 0,
            'status': 1
        }
        tiles.append(tile)

# 游戏逻辑
# 三个相同的牌消掉
# 如何点亮被消牌的下一层
def game_logic(event,level):
    global docks,score
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        for tile in reversed(tiles):
            if tile['status'] == 1 and tile['rect'].collidepoint(pos): # 点击了可点击的牌tile
                tile['status'] = 2
                tiles.remove(tile)
                diff = [t for t in docks if t['tag'] != tile['tag']] # 牌堆与tile不同的牌
                if len(docks) - len(diff) < 2: # 相减的结果就是tile（相同）牌的数量
                    docks.append(tile)
                else:
                    docks = diff # 消掉三个相同牌
                    # 分数逻辑
                    if level == 1:
                        score += 1
                    elif level == 2:
                        score += 2
                    elif level == 3:
                        score += 3
                    
                # 点亮下面的牌
                for down in tiles:
                    if down['layer'] == tile['layer'] - 1 and down['rect'].colliderect(tile['rect']):
                        for up in tiles:
                            if up['layer'] == down['layer'] + 1 and up['rect'].colliderect(down['rect']):
                                break
                        else:
                            down['status'] = 1
                break
    if len(docks) >= 7:
        docks.clear()
        diff.clear()
        update_rankings(score) # 将分数加入排行榜
        score = 0 # 分数清零
        return LOSE
    if len(tiles) == 0:
        return WIN
    
    return GAME

# 绘制游戏
def draw_game(level):
    screen.blit(background, (0, 0))
    for tile in tiles:
        screen.blit(tile['image'], tile['rect'].topleft)
        if tile['status'] == 0:
            screen.blit(mask, tile['rect'].topleft)
    for i, tile in enumerate(docks):
        tile['rect'].topleft = (DOCK_RECT.x + i * T_WIDTH, DOCK_RECT.y)
        screen.blit(tile['image'], tile['rect'].topleft)
    
    # 绘制关卡数
    font = pygame.font.SysFont('华文中宋', 30)
    level_text = font.render(f"关卡: {level}", True, (0, 0, 0))
    screen.blit(level_text, (10, 10))
    # 绘制分数
    font = pygame.font.SysFont('华文中宋', 30)
    score_text = font.render(f"分数: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 50))