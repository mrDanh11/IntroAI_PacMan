from Levels import *
from Config import Config, Sounds
import pygame

backgroundPath = "Assets/background_menu.jpg"

buttonWidth = 300
buttonHeight = 50

exitButtonWidth = 200
exitButtonHeight = 40

buttonX = (Config.width - buttonWidth) / 2

exitButtonX = (Config.width - exitButtonWidth) / 2
exitButtonY = 650

buttons = [
    (buttonX - 100, 300, buttonWidth - 100, buttonHeight, "BFS", Level1()),
    (buttonX - 100, 370, buttonWidth - 100, buttonHeight, "IDS", Level2()),
    (buttonX + 200, 300, buttonWidth - 100, buttonHeight, "UCS", Level3()),
    (buttonX + 200, 370, buttonWidth - 100, buttonHeight, "A*", Level4()),
    (buttonX, 480, buttonWidth, buttonHeight, "Parallel Execution", Level5()),
    (buttonX, 550, buttonWidth, buttonHeight, "Play", Level6()),
]

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
LIGHT_GRAY = (200, 200, 200)
RED = (200, 0, 0)
LIGHT_RED = (255, 50, 50)
BLACK = (0, 0, 0)
LIGHT_GREEN = (144, 238, 144)  # Màu xanh nhạt (Light Green)

prevHoverOn = None
curHoverOn = None

class Menu:
  def drawBackground(self):
    background = pygame.image.load(backgroundPath)

    bg_width, bg_height = background.get_size()

    # Tính tọa độ để căn giữa ảnh
    bg_x = (Config.width - bg_width) // 2
    bg_y = 0 #(Config.height - bg_height) // 2

    # Vẽ ảnh background lên màn hình
    Config.screen.blit(background, (bg_x, bg_y))

  def drawLevelButtons(self):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    global curHoverOn, prevHoverOn

    for x, y, width, height, text, level in buttons:
        color = LIGHT_GREEN
        default_color = WHITE

        text_size = 36

        # Kiểm tra chuột có hover vào nút Level không
        if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
          curHoverOn = text
          pygame.draw.rect(Config.screen, LIGHT_GREEN, (x - 2.5, y - 2.5, width + 5, height + 5), border_radius=15)
          text_size = 40
        else:
          pygame.draw.rect(Config.screen, default_color, (x, y, width, height), border_radius=15)

        font = pygame.font.Font(None, text_size)

        # Hiển thị text trên nút
        text_surface = font.render(text, True, BLACK)
        text_x = x + (width - text_surface.get_width()) / 2
        text_y = y + (height - text_surface.get_height()) / 2
        Config.screen.blit(text_surface, (text_x, text_y))

  def drawExitButton(self):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    global curHoverOn, prevHoverOn

    # Vẽ nút Exit
    if exitButtonX <= mouse_x <= exitButtonX + exitButtonWidth and 650 <= mouse_y <= 650 + exitButtonHeight:
      curHoverOn = "Exit"
      pygame.draw.rect(Config.screen, LIGHT_RED, (exitButtonX, exitButtonY, exitButtonWidth, exitButtonHeight), border_radius=15)
    else:
      pygame.draw.rect(Config.screen, RED, (exitButtonX, exitButtonY, exitButtonWidth, exitButtonHeight), border_radius=15)

    font = pygame.font.Font(None, 36)

    # Hiển thị văn bản trên nút Exit
    text = "Exit"
    text_surface = font.render(text, True, WHITE)
    text_x = exitButtonX + (exitButtonWidth - text_surface.get_width()) / 2
    text_y = exitButtonY + (exitButtonHeight - text_surface.get_height()) / 2
    Config.screen.blit(text_surface, (text_x, text_y))

  def execute(self):
    global curHoverOn, prevHoverOn

    while Config.running:
      Config.screen.fill(WHITE)
      self.drawBackground()

      curHoverOn = None

      self.drawLevelButtons()
      self.drawExitButton()

      if curHoverOn != prevHoverOn:
        prevHoverOn = curHoverOn
        if curHoverOn != None:
          Sounds.hover_sound.play()

      pygame.display.flip()
      
      mouse_x, mouse_y = pygame.mouse.get_pos()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Config.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Nếu click vào nút Levels
            for x, y, width, height, text, level in buttons:
              if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                Sounds.click_sound.play()
                Sounds.beginning_game_sound.stop()
                level.execute()
            # Nếu click Exit
            if exitButtonX <= mouse_x <= exitButtonX + exitButtonWidth and 650 <= mouse_y <= 650 + exitButtonHeight:
              Sounds.click_sound.play()
              Config.running = False
              

    pygame.quit()