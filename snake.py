import pygame
import random
import time as Time

def direction_check(dir,dir_changes,snake_head_dir):
    dir_changes = list(dir_changes)
    if len(dir_changes) == 0:
        if (snake_head_dir == "n" or snake_head_dir == "s") and (not (dir == "n" or dir == "s")):
            dir_changes.append(dir)
        if (snake_head_dir == "e" or snake_head_dir == "w") and (not (dir == "e" or dir == "w")):
            dir_changes.append(dir)
    elif (dir_changes[-1] == "n" or dir_changes[-1] == "s") and (not (dir == "n" or dir == "s")):
        dir_changes.append(dir)
    elif (dir_changes[-1] == "e" or dir_changes[-1] == "w") and (not (dir == "e" or dir == "w")):
        dir_changes.append(dir)
    return dir_changes

def update_pos(pos, dir, speed_const, dt):
    pixel_move = speed_const * dt
    if dir == "s":
        pos.y -= pixel_move
    elif dir == "n":
        pos.y += pixel_move
    elif dir == "e":
        pos.x -= pixel_move
    elif dir == "w":
        pos.x += pixel_move
    return pos
    
def get_events(pygame, event, direction_changes, snake_head_dir):
    if event.type == pygame.KEYDOWN:
        if pygame.key.name(event.key) == "w":
            direction_changes = list(direction_check("n",direction_changes,snake_head_dir))
        elif pygame.key.name(event.key) == "s":
            direction_changes = list(direction_check("s",direction_changes,snake_head_dir))
        elif pygame.key.name(event.key) == "a":
            direction_changes = list(direction_check("w",direction_changes,snake_head_dir))
        elif pygame.key.name(event.key) == "d":
            direction_changes = list(direction_check("e",direction_changes,snake_head_dir))
    return direction_changes

def round_loop(pos_list,nearest_N):
    for i, pos in enumerate(pos_list):
        pos_list[i].x = (round(pos.x/nearest_N,) * nearest_N) % 580
        pos_list[i].y = (round(pos.y/nearest_N,) * nearest_N) % 580
    return pos_list

def generate_apple(all_pos, body_pos, apple_pos, head_pos, tail_pos):
    empty_pos = all_pos.copy()
    empty_pos = list(empty_pos - set(map(tuple, body_pos + apple_pos)))
    empty_pos = [pygame.Vector2(x) for x in empty_pos]
   
    l = len(empty_pos)
    if l == 0:
        return None
    elif l == 1:
        return empty_pos[0]
    else:
        n = random.randrange(0,l-1,1)
        return empty_pos[n]

def main(pygame,screen):
    # Load Images
    background = pygame.image.load("background.png")
    snake_head_north = pygame.image.load("snake_head.png")
    snake_head_east = pygame.transform.rotate(snake_head_north,270)
    snake_head_south = pygame.transform.rotate(snake_head_north,180)
    snake_head_west = pygame.transform.rotate(snake_head_north, 90)
    snake_tail_north = pygame.image.load("snake_tail.png")
    snake_tail_east = pygame.transform.rotate(snake_tail_north,270)
    snake_tail_south = pygame.transform.rotate(snake_tail_north,180)
    snake_tail_west = pygame.transform.rotate(snake_tail_north, 90)
    snake_body = pygame.image.load("snake_body.png")
    apple = pygame.image.load("apple.png")

    clock = pygame.time.Clock()
    running = True
    
    previous_time = pygame.time.get_ticks()
    direction_changes = []
    snake_head_dir = "n"
    snake_head = snake_head_north
    ms_per_unit = 100
    apple_num = 10
    tail_pos = None
    body_pos = []
    apple_pos = []
    bg_offset = pygame.Vector2(0,0)
    length = 1
    dt = 0
    speed_const = 20000/ms_per_unit
    dead = False
    all_pos = set()
    for x in range(0,580,20):
        for y in range(0,580,20):
            all_pos.add((x,y))
    
    font = pygame.font.Font(None, 36)
    bigfont = pygame.font.Font(None, 80)
    
    while running:
        width, height = pygame.display.get_surface().get_size()
        top_left_bg = pygame.Vector2((width/2)-310,(height/2)-310)
        top_left_play = pygame.Vector2((width/2)-290,(height/2)-290)
        
        head_pos = pygame.Vector2(280,280)
        
        bg_offset = update_pos(bg_offset, snake_head_dir, speed_const, dt)
        bg_offset.x = round(bg_offset.x,3)%40
        bg_offset.y = round(bg_offset.y,3)%40
        
        for i, pos in enumerate(body_pos):
            body_pos[i] = update_pos(pos, snake_head_dir, speed_const, dt)
        for i, pos in enumerate(apple_pos):
            apple_pos[i] = update_pos(pos, snake_head_dir, speed_const, dt)
        round_loop(body_pos,0.001)
        round_loop(apple_pos,0.001)
    
        try:
            tail_pos = update_pos(tail_pos, snake_head_dir, speed_const, dt)
            tail_pos.x = round(tail_pos.x,3)
            tail_pos.y = round(tail_pos.y,3)
            tail_pos = update_pos(tail_pos, snake_tail_dir, speed_const, dt)
        except:
            pass
        
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            direction_changes = get_events(pygame, event, direction_changes, snake_head_dir)
                
        
        time = pygame.time.get_ticks()
        if time - previous_time >= ms_per_unit:
            bg_offset.x = round(bg_offset.x/20) * 20
            bg_offset.y = round(bg_offset.y/20) * 20
            body_pos = round_loop(body_pos,20)
            apple_pos = round_loop(apple_pos,20)

            for pos in body_pos:
                if head_pos == pos:
                    dead = True
            
            temp_pos = head_pos.copy()
            body_pos.append(temp_pos)
            
                
            if len(apple_pos) < apple_num:
                new_apple = generate_apple(all_pos,body_pos,apple_pos,head_pos,tail_pos)
                if new_apple:
                    apple_pos.append(new_apple)
                            
            for pos in apple_pos:
                if head_pos == pos:
                    apple_pos.remove(pos)
                    length += 1
                    
            if len(body_pos) > length:
                tail_pos = body_pos[0]
                if (tail_pos.y - 20) % 580 == body_pos[1].y:
                    snake_tail_dir = "s"
                    snake_tail = snake_tail_south
                if (tail_pos.y + 20) % 580 == body_pos[1].y:
                    snake_tail_dir = "n"
                    snake_tail = snake_tail_north
                if (tail_pos.x - 20) % 580 == body_pos[1].x:
                     snake_tail_dir = "e"
                     snake_tail = snake_tail_east
                if (tail_pos.x + 20) % 580 == body_pos[1].x:
                     snake_tail_dir = "w"
                     snake_tail = snake_tail_west
    
                body_pos = body_pos[1:]
            else:
                tail_pos = None
    
                
            if len(direction_changes) > 0:
                snake_head_dir = direction_changes[0]
                if snake_head_dir == "n":
                    snake_head = snake_head_north
                if snake_head_dir == "s":
                    snake_head = snake_head_south
                if snake_head_dir == "w":
                    snake_head = snake_head_west
                if snake_head_dir == "e":
                    snake_head = snake_head_east
                direction_changes = direction_changes[1:] 
            
            previous_time = time
            
        screen.fill((0,0,0))
        shifter = pygame.Vector2(-20,-20)
        screen.blit(background,bg_offset+top_left_bg+shifter)
    
        for p in body_pos:
            if 560 < p.x <= 580:
                screen.blit(snake_body, p+pygame.Vector2(-580,0)+top_left_play)
            if 560 < p.y <= 580:
                screen.blit(snake_body, p+pygame.Vector2(0,-580)+top_left_play)
            screen.blit(snake_body,p+top_left_play)
    
        for p in apple_pos:
            if 560 < p.x <= 580:
                screen.blit(apple, p+pygame.Vector2(-580,0)+top_left_play)
            if 560 < p.y <= 580:
                screen.blit(apple, p+pygame.Vector2(0,-580)+top_left_play)
            screen.blit(apple,p+top_left_play)
        try:
            screen.blit(snake_tail,tail_pos+top_left_play)
        except:
            pass
        screen.blit(snake_head,head_pos+top_left_play)
    
        pygame.draw.rect(screen, (0, 0, 0), (top_left_bg.x-20, top_left_bg.y-20, 40, 660))    
        pygame.draw.rect(screen, (0, 0, 0), (top_left_bg.x+600, top_left_bg.y-20, 40, 660))    
        pygame.draw.rect(screen, (0, 0, 0), (top_left_bg.x-20, top_left_bg.y-20, 660, 40))    
        pygame.draw.rect(screen, (0, 0, 0), (top_left_bg.x-20, top_left_bg.y+600, 660, 40))    
    
        if dead == True:
            death_text = bigfont.render(f"You Died! Score: {length}", True, (0,0,0))
            center = death_text.get_rect()
            center.center = (width//2,height//2)
            screen.blit(death_text, center)
            instructions = font.render('Press "r" to retry', True, (0,0,0))
            center = instructions.get_rect()
            center.center = (width//2,(height//2)-50)
            screen.blit(instructions, center)
            pygame.display.flip()
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if pygame.key.name(event.key) == "r":
                            main(pygame,screen)
                            running = False
        else:
            score_text = font.render(f"Score: {length}", True, (255,255,255))
            screen.blit(score_text, (0,0))
            
        dt = clock.tick(60) / 1000  
        pygame.display.flip()
        
    pygame.quit

pygame.init()
screen = pygame.display.set_mode((720,720))
main(pygame,screen)
