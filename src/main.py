import pygame
import sys
from menu import load_menu_assets, draw_menu

#Initialize pygame
pygame.init()

#Window settings
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Cat Café")

#Surface at full resolution
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

#FPS and clock
FPS = 60
clock = pygame.time.Clock()

#HUD
hud_font = pygame.font.Font("assets/fonts/Golden Age.ttf", 80)

#Load menu assets
menu_frames, button_day, button_night = load_menu_assets()

#Menu animation
menu_frame_index = 0
menu_anim_timer = 0
MENU_ANIM_SPEED = 1

#Game state
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_END = "end"
game_state = STATE_MENU

#Load background layers
bg_wall = pygame.image.load("assets/bg_wall.png")
bg_wall = pygame.transform.scale(bg_wall, (GAME_WIDTH, GAME_HEIGHT))

floor_img = pygame.image.load("assets/floor.png")
floor_img = pygame.transform.scale(floor_img, (GAME_WIDTH, GAME_HEIGHT))

countertop_img = pygame.image.load("assets/countertop.png")
countertop_img = pygame.transform.scale(countertop_img, (GAME_WIDTH, GAME_HEIGHT))

lamps_img = pygame.image.load("assets/lamps.png")
lamps_img = pygame.transform.scale(lamps_img, (GAME_WIDTH, GAME_HEIGHT))

#Load player
player_img = pygame.image.load("assets/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (310, 320))

#Player position
PLAYER_X = 630
PLAYER_Y = 340

#In-game clock
in_game_hour = 9
in_game_minute = 0
time_elapsed = 0

shift = "day"
money = 0
customers_served = 0

#Main game loop
running = True
while running:
    delta_time = clock.tick(FPS) / 1000.0

    #Mouse hovering
    raw_mouse = pygame.mouse.get_pos()
    win_w, win_h = screen.get_size()
    mouse_pos = (
    int(raw_mouse[0] * GAME_WIDTH / win_w),
    int(raw_mouse[1] * GAME_HEIGHT / win_h)
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == STATE_MENU:
                button_day_rect = button_day.get_rect(center=(960, 620))
                button_night_rect = button_night.get_rect(center=(960, 760))

                if button_day_rect.collidepoint(mouse_pos):
                    shift = "day"
                    in_game_hour = 9
                    in_game_minute = 0
                    game_state = STATE_PLAYING

                elif button_night_rect.collidepoint(mouse_pos):
                    shift = "night"
                    in_game_hour = 0
                    in_game_minute = 0
                    game_state = STATE_PLAYING

    #===================== MENU =====================
    if game_state == STATE_MENU:
        menu_anim_timer += delta_time
        if menu_anim_timer >= MENU_ANIM_SPEED:
            menu_anim_timer = 0
            menu_frame_index = (menu_frame_index + 1) % len(menu_frames)

        draw_menu(game_surface, menu_frames, button_day, button_night, menu_frame_index, mouse_pos, hud_font)

    #===================== PLAYING =====================
    elif game_state == STATE_PLAYING:
        game_surface.blit(bg_wall, (0, 0))
        game_surface.blit(floor_img, (0, 0))
        game_surface.blit(player_img, (PLAYER_X, PLAYER_Y))
        game_surface.blit(countertop_img, (0, 0))
        game_surface.blit(lamps_img, (0, 0))

        #Display clock
        time_text = f"{in_game_hour:02d}:{in_game_minute:02d}"
        clock_shadow = hud_font.render(time_text, True, (0, 0, 0))
        game_surface.blit(clock_shadow, (895, 30))
        clock_surface = hud_font.render(time_text, True, (255, 255, 255))
        game_surface.blit(clock_surface, (890, 25))

        #Display money
        money_text = f"${money:.2f}"
        money_shadow = hud_font.render(money_text, True, (0, 0, 0))
        game_surface.blit(money_shadow, (490, 30))
        money_surface = hud_font.render(money_text, True, (189, 247, 173))
        game_surface.blit(money_surface, (485, 25))

        #Display customers served
        customers_served_text = f"{customers_served}"
        customers_served_shadow = hud_font.render(customers_served_text, True, (0, 0, 0))
        game_surface.blit(customers_served_shadow, (1365, 30))
        customers_surface = hud_font.render(customers_served_text, True, (240, 247, 173))
        game_surface.blit(customers_surface, (1360, 25))

        #Advance in-game time
        time_elapsed += delta_time
        if shift == "day":
            interval = 18.75
            end_hour = 17
        else:
            interval = 12.5
            end_hour = 6

        if time_elapsed >= interval:
            time_elapsed = 0
            in_game_minute += 15
            if in_game_minute >= 60:
                in_game_minute = 0
                in_game_hour += 1
            if in_game_hour >= end_hour:
                game_state = STATE_END

    #===================== END =====================
    elif game_state == STATE_END:
        game_surface.fill((40, 35, 50))
        end_text = hud_font.render("Shift Over!", True, (255, 210, 80))
        game_surface.blit(end_text, end_text.get_rect(center=(GAME_WIDTH // 2, 400)))
        money_end = hud_font.render(f"Money earned: ${money:.2f}", True, (255, 255, 255))
        game_surface.blit(money_end, money_end.get_rect(center=(GAME_WIDTH // 2, 550)))
        customers_end = hud_font.render(f"Customers served: {customers_served}", True, (255, 255, 255))
        game_surface.blit(customers_end, customers_end.get_rect(center=(GAME_WIDTH // 2, 680)))

    #Scale to fill entire window
    win_w, win_h = screen.get_size()
    scaled_surface = pygame.transform.scale(game_surface, (win_w, win_h))
    screen.blit(scaled_surface, (0, 0))

    #Update display
    pygame.display.update()

pygame.quit()
sys.exit()