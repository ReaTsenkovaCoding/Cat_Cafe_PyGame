import pygame
def load_menu_assets():
    #Load welcome background spritesheet
    sheet = pygame.image.load("assets/welcome_screen/welcome_bg.png").convert_alpha()
    sheet = pygame.transform.scale(sheet, (1920, 1080 * 2))

    #Slice 2 frames
    frame1 = sheet.subsurface(pygame.Rect(0,0,1920,1080))
    frame2 = sheet.subsurface(pygame.Rect(0,1080,1920,1080))
    frames = [frame1, frame2]

    #Load buttons, sizes
    button_day = pygame.image.load("assets/welcome_screen/button_day.png").convert_alpha()
    button_day = pygame.transform.scale(button_day, (430, 140))

    button_night = pygame.image.load("assets/welcome_screen/button_night.png").convert_alpha()
    button_night = pygame.transform.scale(button_night, (430, 140))

    return frames, button_day, button_night

def draw_menu(game_surface, frames, button_day, button_night, frame_index, mouse_pos, hud_font):
    #Draw current animation frame
    game_surface.blit(frames[frame_index], (0,0))
    button_font = pygame.font.Font("assets/fonts/Golden Age.ttf", 40)

    #Button positions
    button_day_rect = button_day.get_rect(center = (980, 680))
    button_night_rect = button_night.get_rect(center = (980, 860))

    #Hover effect
    for button, button_rect in [(button_day, button_day_rect), (button_night, button_night_rect)]:
        game_surface.blit(button, button_rect)
        if button_rect.collidepoint(mouse_pos):
            overlay = pygame.Surface((button_rect.width
                                     , button_rect.height), pygame.SRCALPHA)
            overlay.fill((0,0,0,60))
            game_surface.blit(overlay,button_rect)

    #Button texts
    day_text = button_font.render("Day Shift", True, (60, 40, 20))
    game_surface.blit(day_text, day_text.get_rect(center = (1000, 675)))

    night_text = button_font.render("Night Shift", True, (255, 255, 255))
    game_surface.blit(night_text, night_text.get_rect(center = (1000, 855)))