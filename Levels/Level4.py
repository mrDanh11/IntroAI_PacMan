from Entities.Entity import Entity
from EntitiesManager import EntitiesManager as EM
from Config import Config, Object, Sounds, Board
from Levels.ExperimentBox import ExperimentBox
import pygame
import time
import tracemalloc #de lay bo nho
import math

# testcases: (ghost, pacman)
testcases = [
    ((16, 13), (24, 14)),  # Giữ nguyên test case đầu tiên (đang dùng mặc định)
<<<<<<< Updated upstream
    ((4, 2),    (26, 25)),  # Ghost ở góc trên trái, Pacman ở góc dưới phải
=======
    ((6, 6),    (25, 25)),  # Ghost ở góc trên trái, Pacman ở góc dưới phải
>>>>>>> Stashed changes
    ((29, 27),  (27, 3)),    # Ghost bên phải bản đồ, Pacman bên trái trên
    ((4, 13),  (24,13)),  # Cả 2 ở giữa bản đồ
    ((30, 26),   (3, 2))    # Ghost dưới cùng trái, Pacman trên cùng phải
]
testcaseID = 0

quit = False
start = False

class Level4:
    def __init__(self):
        pass

    def setup(self):
        # Setup positions
        Object.redGhostX, Object.redGhostY = testcases[testcaseID][0]
        Object.pacmanX, Object.pacmanY = testcases[testcaseID][1]
        Object.pinkGhostX, Object.pinkGhostY = -1, -1
        Object.blueGhostX, Object.blueGhostY = -1, -1
        Object.orangeGhostX, Object.orangeGhostY = -1, -1

        Board.maze = [row[:] for row in Board.initMaze]

        # Setup real coordinates
        (Object.realPacmanX, Object.realPacmanY) = Entity.getRealCoordinates((Object.pacmanX, Object.pacmanY), Object.PACMAN_SIZE)
        (Object.realRedGhostX, Object.realRedGhostY) = Entity.getRealCoordinates((Object.redGhostX, Object.redGhostY), Object.RED_GHOST_SIZE)

        # Reset Board.coordinates
        for i in range(len(Board.coordinates)):
            for j in range(len(Board.coordinates[0])):
                Board.coordinates[i][j] = Board.BLANK
        Board.coordinates[Object.redGhostX][Object.redGhostY] = Board.RED_GHOST
        Board.coordinates[Object.pacmanX][Object.pacmanY] = Board.PACMAN

    def get_volume(self, ghost_x, ghost_y, pac_x, pac_y, max_distance=15):
        distance = math.sqrt((ghost_x - pac_x) ** 2 + (ghost_y - pac_y) ** 2)
        volume = max(0.0, 1 - (distance / max_distance))
        return min(1.0, max(0.0, volume))

    def execute(self):
        global quit, start
        quit = False
        start = False

        self.setup()  # setup once before loop

        font = pygame.font.Font(None, 30)
        shortkey = font.render("ESC: Menu  Q: Quit", True, (255, 255, 255))

        Sounds().dramatic_theme_music()
        ghost_move_sound = pygame.mixer.Sound("Assets/sounds/ghost_move.mp3")

        clock = pygame.time.Clock()

        tracemalloc.start()
        start_time = time.time()
        path, numOfExpendedNodes = EM().redGhost.getTargetPathInformation(
            (Object.redGhostX, Object.redGhostY), (Object.pacmanX, Object.pacmanY)
        )
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        step = 0
        countFrames = 0

        while Config.running:
            Config.screen.fill('black')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ghost_move_sound.stop()
                    Sounds.dramatic_theme_music_sound.stop()
                    Config.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        ghost_move_sound.stop()
                        Sounds.click_sound.play()
                        Sounds.dramatic_theme_music_sound.stop()
                        quit = True
                        return
                    if event.key == pygame.K_q:
                        ghost_move_sound.stop()
                        Sounds.click_sound.play()
                        Sounds.dramatic_theme_music_sound.stop()
                        Config.running = False
                        return
                    if event.key == pygame.K_SPACE:
                        if not start:
                            ghost_move_sound.play(loops=-1)
                        start = True

            EM().maze.draw()

            if start and path:
                if countFrames % 15 == 0 and step < len(path):
                    targetX, targetY = path[step]
                    curX, curY = Object.redGhostX, Object.redGhostY

                    if (curX, curY) == (targetX, targetY):
                        step += 1
                        if step < len(path):
                            targetX, targetY = path[step]

                    if step < len(path):
                        newX, newY = curX, curY
                        if targetX != curX:
                            newX += (targetX - curX) // abs(targetX - curX)
                        if targetY != curY:
                            newY += (targetY - curY) // abs(targetY - curY)
                        Object.redGhostX = newX
                        Object.redGhostY = newY

                EM().redGhost.move()

            EM().pacman.draw()
            EM().redGhost.draw()

            if not start:
                overlay = pygame.Surface((Config.width, Config.height))
                overlay.set_alpha(180)
                overlay.fill((0, 0, 0))
                Config.screen.blit(overlay, (0, 0))

                color = (255, 255, 255 - countFrames % 30 * 8)
                labelFont = pygame.font.Font(None, 30)
                space_to_start = labelFont.render("PRESS SPACE TO START", True, color)
                Config.screen.blit(space_to_start, (Config.width / 2 - 130, Config.height / 2 - 50))

            Config.screen.blit(shortkey, (580, 800 - 30))
            pygame.display.flip()
            clock.tick(Config.fps)
            countFrames += 1

            if (Object.redGhostX, Object.redGhostY) == (Object.pacmanX, Object.pacmanY):
                ghost_move_sound.stop()
                Sounds.dramatic_theme_music_sound.stop()
                break

        Sounds.lose_sound.play()
        start = False

        algorithm = "A*"
        search_time = end_time - start_time
        memory_usage = peak / (2 ** 20)

        while Config.running:
            nextTestcase = ExperimentBox().showResultBoard(
                algorithm, search_time, memory_usage, numOfExpendedNodes
            )
            if nextTestcase == -1:
                quit = True
                break
            elif nextTestcase is not None:
                global testcaseID
                testcaseID = nextTestcase
                break
