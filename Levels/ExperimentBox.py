from Config import Config, Sounds
import pygame

# Box hiển thị sau khi kết thúc game để người chơi chọn testcase
BoxWidth = 500
BoxHeight = 300

boxX = (Config.width - BoxWidth) / 2
boxY = 80

ButtonWidth = 60
ButtonHeight = 40
ButtonSpacing = 20
ButtonY = boxY + BoxHeight - 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 102, 204)
LIGHT_GRAY = (245, 245, 245)
HOVER_COLOR = (200, 255, 200)
BOX_BORDER = (50, 50, 50)

font = pygame.font.Font(None, 28)
big_font = pygame.font.Font(None, 34)
bold_font = pygame.font.Font(None, 30)

prevHoverOn = None
curHoverOn = None

class ExperimentBox:
    def showResultBoard(self, algorithm, search_time, memory_usage , num_expanded_nodes):
        global prevHoverOn, curHoverOn
        curHoverOn = None

        # --- Draw main popup box ---
        pygame.draw.rect(Config.screen, LIGHT_GRAY, (boxX, boxY, BoxWidth, BoxHeight), border_radius=18)
        pygame.draw.rect(Config.screen, BOX_BORDER, (boxX, boxY, BoxWidth, BoxHeight), 3, border_radius=18)

        # --- Header ---
        header_text = big_font.render("🎯 Algorithm Results", True, DARK_BLUE)
        Config.screen.blit(header_text, (boxX + BoxWidth / 2 - header_text.get_width() / 2, boxY + 15))

        # --- Stats section ---
        stats = [
            ("Algorithm", algorithm),
            ("Time", f"{search_time * 1000:.2f} ms"),
            ("Memory", f"{memory_usage * 1024:.2f} KB"),
            ("Expanded Nodes", str(num_expanded_nodes))
        ]

        for i, (label, value) in enumerate(stats):
            card_x = boxX + 30 + (i % 2) * (BoxWidth / 2 - 40)
            card_y = boxY + 60 + (i // 2) * 60
            card_width = BoxWidth / 2 - 60
            card_height = 50

            pygame.draw.rect(Config.screen, WHITE, (card_x, card_y, card_width, card_height), border_radius=10)
            pygame.draw.rect(Config.screen, BOX_BORDER, (card_x, card_y, card_width, card_height), 2, border_radius=10)

            label_text = font.render(label + ":", True, BLACK)
            value_text = bold_font.render(value, True, DARK_BLUE)

            Config.screen.blit(label_text, (card_x + 10, card_y + 6))
            Config.screen.blit(value_text, (card_x + 10, card_y + 25))

        # --- Footer title ---
        pick_testcase_text = font.render("Pick a Testcase:", True, BLACK)
        Config.screen.blit(pick_testcase_text, (boxX + 30, ButtonY - 30))

        # --- Buttons ---
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i in range(5):
            button_x = boxX + 30 + i * (ButtonWidth + ButtonSpacing)
            is_hovered = button_x <= mouse_x <= button_x + ButtonWidth and ButtonY <= mouse_y <= ButtonY + ButtonHeight
            color = HOVER_COLOR if is_hovered else WHITE

            if is_hovered:
                curHoverOn = i

            pygame.draw.rect(Config.screen, BOX_BORDER, (button_x - 2, ButtonY - 2, ButtonWidth + 4, ButtonHeight + 4), border_radius=12)
            pygame.draw.rect(Config.screen, color, (button_x, ButtonY, ButtonWidth, ButtonHeight), border_radius=12)

            number = bold_font.render(f"{i + 1}", True, BLACK)
            number_rect = number.get_rect(center=(button_x + ButtonWidth / 2, ButtonY + ButtonHeight / 2))
            Config.screen.blit(number, number_rect)

        # --- Hover Sound ---
        if curHoverOn != prevHoverOn:
            prevHoverOn = curHoverOn
            if curHoverOn is not None:
                Sounds.hover_sound.play()

        pygame.display.flip()

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Config.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    Config.running = False
                    return -1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in range(5):
                    button_x = boxX + 30 + i * (ButtonWidth + ButtonSpacing)
                    if button_x <= mouse_x <= button_x + ButtonWidth and ButtonY <= mouse_y <= ButtonY + ButtonHeight:
                        Sounds.click_sound.play()
                        return i

        return None
