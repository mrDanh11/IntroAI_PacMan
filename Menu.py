import pygame
from Levels import *
from Config import Config, Sounds

# backgroundPath = "Assets/R.jpg"
backgroundPath = "Assets/pacman_background.jpg"

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
LIGHT_GRAY = (200, 200, 200)
RED = (200, 0, 0)
LIGHT_RED = (255, 50, 50)
BLACK = (0, 0, 0)
LIGHT_GREEN = (144, 238, 144)

prevHoverOn = None
curHoverOn = None

tabs = ["Algorithms", "Modes"]
active_tab = "Algorithms"

buttons_by_tab = {
    "Algorithms": [
        ("Level 1: BFS", Level1()),
        ("Level 2: IDS", Level2()),
        ("Level 3: UCS", Level3()),
        ("Level 4: A*", Level4()),
    ],
    "Modes": [
        ("Level 5: Parallel Execution", Level5()),
        ("Level 6: Controll Pac-Man", Level6()),
    ]
}


class Menu:
    def drawBackground(self):
        background = pygame.image.load(backgroundPath)
        bg_width, bg_height = background.get_size()
        bg_x = (Config.width - bg_width) // 2
        bg_y = (Config.height - bg_height) // 2
        Config.screen.blit(background, (bg_x, bg_y))

    def drawTabs(self):
        tab_height = 50
        tab_margin = 20
        font = pygame.font.Font(None, 30)

        total_width = Config.width - 100
        tab_width = total_width // len(tabs)
        tab_y = 30

        for i, tab in enumerate(tabs):
            tab_x = 50 + i * (tab_width + tab_margin)
            color = LIGHT_GRAY if tab == active_tab else GRAY
            pygame.draw.rect(Config.screen, color, (tab_x, tab_y, tab_width, tab_height), border_radius=15)

            text_surface = font.render(tab, True, BLACK)
            text_x = tab_x + (tab_width - text_surface.get_width()) / 2
            text_y = tab_y + (tab_height - text_surface.get_height()) / 2
            Config.screen.blit(text_surface, (text_x, text_y))

    def drawLevelButtons(self):
        global curHoverOn, prevHoverOn
        mouse_x, mouse_y = pygame.mouse.get_pos()

        button_spacing = 70
        button_y_start = 130
        max_text_size = 36
        min_text_size = 24

        for i, (text, level) in enumerate(buttons_by_tab[active_tab]):
            # Tự động điều chỉnh chiều rộng button
            font = pygame.font.Font(None, max_text_size)
            text_surface = font.render(text, True, BLACK)
            dynamic_width = max(300, text_surface.get_width() + 40)
            x = (Config.width - dynamic_width) // 2
            y = button_y_start + i * button_spacing

            # Hover
            if x <= mouse_x <= x + dynamic_width and y <= mouse_y <= y + 50:
                curHoverOn = text
                pygame.draw.rect(Config.screen, LIGHT_GREEN, (x - 2, y - 2, dynamic_width + 4, 54), border_radius=15)
                font = pygame.font.Font(None, max_text_size + 4)
            else:
                pygame.draw.rect(Config.screen, WHITE, (x, y, dynamic_width, 50), border_radius=15)
                font = pygame.font.Font(None, max_text_size)

            text_surface = font.render(text, True, BLACK)
            text_x = x + (dynamic_width - text_surface.get_width()) / 2
            text_y = y + (50 - text_surface.get_height()) / 2
            Config.screen.blit(text_surface, (text_x, text_y))

    def drawExitButton(self):
        global curHoverOn
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_width = 200
        button_height = 45

        x = (Config.width - button_width) // 2
        y = Config.height - 80

        if x <= mouse_x <= x + button_width and y <= mouse_y <= y + button_height:
            curHoverOn = "Exit"
            pygame.draw.rect(Config.screen, LIGHT_RED, (x, y, button_width, button_height), border_radius=15)
        else:
            pygame.draw.rect(Config.screen, RED, (x, y, button_width, button_height), border_radius=15)

        font = pygame.font.Font(None, 36)
        text_surface = font.render("Exit", True, WHITE)
        text_x = x + (button_width - text_surface.get_width()) / 2
        text_y = y + (button_height - text_surface.get_height()) / 2
        Config.screen.blit(text_surface, (text_x, text_y))

    def execute(self):
        global curHoverOn, prevHoverOn, active_tab
        while Config.running:
            Config.screen.fill(WHITE)
            self.drawBackground()
            curHoverOn = None

            self.drawTabs()
            self.drawLevelButtons()
            self.drawExitButton()

            if curHoverOn != prevHoverOn:
                prevHoverOn = curHoverOn
                if curHoverOn is not None:
                    Sounds.hover_sound.play()

            pygame.display.flip()
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Config.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Tabs
                    tab_height = 50
                    tab_margin = 20
                    total_width = Config.width - 100
                    tab_width = total_width // len(tabs)
                    tab_y = 30
                    for i, tab in enumerate(tabs):
                        tab_x = 50 + i * (tab_width + tab_margin)
                        if tab_x <= mouse_x <= tab_x + tab_width and tab_y <= mouse_y <= tab_y + tab_height:
                            active_tab = tab
                            Sounds.click_sound.play()

                    # Buttons
                    button_spacing = 70
                    button_y_start = 130
                    for i, (text, level) in enumerate(buttons_by_tab[active_tab]):
                        font = pygame.font.Font(None, 36)
                        text_surface = font.render(text, True, BLACK)
                        dynamic_width = max(300, text_surface.get_width() + 40)
                        x = (Config.width - dynamic_width) // 2
                        y = button_y_start + i * button_spacing
                        if x <= mouse_x <= x + dynamic_width and y <= mouse_y <= y + 50:
                            Sounds.click_sound.play()
                            Sounds.beginning_game_sound.stop()
                            level.execute()

                    # Exit
                    exit_x = (Config.width - 200) // 2
                    exit_y = Config.height - 80
                    if exit_x <= mouse_x <= exit_x + 200 and exit_y <= mouse_y <= exit_y + 45:
                        Sounds.click_sound.play()
                        Config.running = False

        pygame.quit()
