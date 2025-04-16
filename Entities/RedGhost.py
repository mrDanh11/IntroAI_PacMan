# A*
from .Entity import Entity
from .GhostInterface import GhostInterface
from Config import Config, Material, Board, Object, Mode
import heapq
from collections import deque

class RedGhost(GhostInterface):
    def draw(self):
        realX = Object.realRedGhostX
        realY = Object.realRedGhostY
        if Mode.RedGhost == Mode.CHASING:
            Config.screen.blit(Material.RedGhostImage, (realY, realX))
        elif Mode.RedGhost == Mode.POWER_UP:
            if Mode.powerupTime <= 60 * 2:
                if Mode.powerupTime // 15 % 2 == 0: 
                    Config.screen.blit(Material.PowerupImage, (realY, realX))
                else:
                    Config.screen.blit(Material.RedGhostImage, (realY, realX))
            else:
                Config.screen.blit(Material.PowerupImage, (realY, realX))
        else: #dead
            Config.screen.blit(Material.DeadGhostImage, (realY, realX))
        
    def move(self):
        x, y = Object.redGhostX, Object.redGhostY
        targetX, targetY = Entity.getRealCoordinates((x, y), Object.RED_GHOST_SIZE)  # Tọa độ mục tiêu
        realX, realY = Object.realRedGhostX, Object.realRedGhostY  # Tọa độ thực tế

        dx, dy = (targetX - realX), (targetY - realY)
        sX = Config.p_height / 15
        sY = Config.p_width / 15

        # Kiểm tra nếu ma đỏ quá gần các ma khác
        other_ghosts = [
            (Object.pinkGhostX, Object.pinkGhostY),
            (Object.blueGhostX, Object.blueGhostY),
            (Object.orangeGhostX, Object.orangeGhostY)
        ]
        
        # Kiểm tra va chạm với các ma khác
        avoid_collision = False
        for gx, gy in other_ghosts:
            dist = abs(realX - gx) + abs(realY - gy)
            if dist <= 2:
                avoid_collision = True
                break

        if avoid_collision:
            # Nếu cần tránh, di chuyển theo hướng khác nhưng vẫn tiến về mục tiêu
            dx, dy = self.avoid_ghost_collision(realX, realY, targetX, targetY)
        else:
            # Nếu không gặp ma khác, tiếp tục di chuyển về mục tiêu
            dx, dy = (targetX - realX), (targetY - realY)
        
        # Cập nhật vị trí của ma đỏ
        if abs(dx) >= sX:
            realX = realX + dx / abs(dx) * sX
        else:
            realX = targetX

        if abs(dy) >= sY:
            realY = realY + dy / abs(dy) * sY
        else:
            realY = targetY

        Object.realRedGhostX = realX
        Object.realRedGhostY = realY
    
    #Kiểm tra vị trí có bị chặn không
    def is_position_clear(self, x, y):
        maze_value = Board.maze[x][y]
        return (maze_value < 3 or maze_value == 9) and Board.coordinates[x][y] in (Board.BLANK, Board.PACMAN)
    
    #Kiểm tra vị trí hợp lệ
    #Nếu vị trí nằm trong ma trận và không bị chặn thì trả về True
    #Ngược lại trả về False
    def isValidPos(self, x, y):
        return 0 <= x < Board.ROWS and 0 <= y < Board.COLS and self.is_position_clear(x, y) 
    
    def heuristic(self, ghostX, ghostY):
    # Tính toán Manhattan Distance đến Pacman
        h = abs(ghostX - Object.pacmanX) + abs(ghostY - Object.pacmanY)

        penalty = 0

        # Phạt nếu gần ghost khác (tránh va chạm)
        # - Phạt nặng nếu ghost cùng ô
        # - Phạt nhẹ nếu ghost cách gần (<= 2 ô)
        other_ghosts = [
            (Object.pinkGhostX, Object.pinkGhostY),
            (Object.blueGhostX, Object.blueGhostY),
            (Object.orangeGhostX, Object.orangeGhostY)
        ]
        
        for gx, gy in other_ghosts:
            dist = abs(ghostX - gx) + abs(ghostY - gy)
            if dist == 0:
                penalty += 100  # Cùng ô thì phạt nặng
            elif dist <= 2:
                penalty += 3  # Phạt nhẹ nếu gần

        # Phạt nếu node gần ngõ cụt (chỉ có 1 đường ra)
        # - Nếu số lượng láng giềng hợp lệ <= 1, tức là ở ngõ cụt
        valid_neighbors = sum(
            1 for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] 
            if self.isValidPos(ghostX + dx, ghostY + dy)
        )
        
        if valid_neighbors <= 1:
            penalty += 2  # Phạt vì gần dead-end

        # Trả về giá trị heuristic cộng với các phạt
        return h + penalty

    
    def getTargetPos(self, ghost, pacman): # A*
        (posX, posY) = ghost
        f = 0
        h = f + self.heuristic(posX, posY)
        
        heap = [(f, h, posX, posY, [])] # f(x), heuristic curX, curY, path
        heapq.heapify(heap)
        
        visited = set([(posX, posY)])
        
        DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)] # lên, xuống, phải, trái

        PATH_LIMIT = 100

        while heap:
            (f, h, x, y, path) = heapq.heappop(heap)
            
            if Board.coordinates[x][y] == Board.PACMAN or len(path) == PATH_LIMIT:
                return path[0]

            for dx, dy in DIRECTIONS:
                nx = x + dx
                ny = y + dy
                if not self.isValidPos(nx, ny):
                    continue
                while (nx, ny) not in Board.nodes and (nx, ny) != (Object.pacmanX, Object.pacmanY):
                    nx += dx
                    ny += dy
                    if not self.isValidPos(nx, ny):
                        break

                if (nx, ny) not in visited and self.isValidPos(nx, ny)\
                    and (nx, ny) != (Object.pinkGhostX, Object.pinkGhostY) \
                    and (nx, ny) != (Object.orangeGhostX, Object.orangeGhostY) \
                    and (nx, ny) != (Object.blueGhostX, Object.blueGhostY):  #check collision::
                    nh = self.heuristic(nx, ny)
                    nf = f - h + nh + abs(nx - x) + abs(ny - y)
                    heapq.heappush(heap, (nf, nh, nx, ny, path + [(nx, ny)]))
                    visited.add((nx, ny))
        
        return None
    
    def getTargetPathInformation(self, ghost, pacman):
        (posX, posY) = ghost
        f = 0
        h = f + self.heuristic(posX, posY)
        
        heap = [(f, h, posX, posY, [])] # f(x), heuristic curX, curY, path
        heapq.heapify(heap)
        
        visited = set([])
        
        DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)] # lên, xuống, phải, trái

        PATH_LIMIT = 100

        while heap:
            (f, h, x, y, path) = heapq.heappop(heap)
            visited.add((x, y))

            if Board.coordinates[x][y] == Board.PACMAN or len(path) == PATH_LIMIT:
                return path, len(visited)

            for dx, dy in DIRECTIONS:
                nx = x + dx
                ny = y + dy
                if not self.isValidPos(nx, ny):
                    continue
                while (nx, ny) not in Board.nodes and (nx, ny) != (Object.pacmanX, Object.pacmanY):
                    nx += dx
                    ny += dy
                    if not self.isValidPos(nx, ny):
                        break

                if (nx, ny) not in visited and self.isValidPos(nx, ny)\
                    and (nx, ny) != (Object.pinkGhostX, Object.pinkGhostY) \
                    and (nx, ny) != (Object.orangeGhostX, Object.orangeGhostY) \
                    and (nx, ny) != (Object.blueGhostX, Object.blueGhostY):  #check collision::
                    nh = self.heuristic(nx, ny)
                    nf = f - h + nh + abs(nx - x) + abs(ny - y)
                    heapq.heappush(heap, (nf, nh, nx, ny, path + [(nx, ny)]))
        
        return None, len(visited)

    def updatePos(self):
        oldX, oldY = Object.redGhostX, Object.redGhostY
        targetPos = self.getTargetPos((oldX, oldY), (Object.pacmanX, Object.pacmanY))
        if targetPos:
            targetX, targetY = targetPos

            newX, newY = oldX, oldY
            if targetX != oldX:
                newX += (targetX - oldX) // abs(targetX - oldX) 
            if targetY != oldY:
                newY += (targetY - oldY) // abs(targetY - oldY)

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.RED_GHOST

            Object.redGhostX = newX
            Object.redGhostY = newY
   
    def isValidPosPowerUp(self, x, y):
        if 0 <= x < Board.ROWS and 0 <= y < Board.COLS:
            if (Board.maze[x][y] < 3 or Board.maze[x][y] == 9) and Board.coordinates[x][y] == Board.BLANK \
                and (x, y) != (Object.pinkGhostX, Object.pinkGhostY) \
                and (x, y) != (Object.blueGhostX, Object.blueGhostY) \
                and (x, y) != (Object.orangeGhostX, Object.orangeGhostY) \
                and (x, y) != (Object.pacmanX, Object.pacmanY):
                return True
        return False
    
    def getTargetPosPowerUp(self, ghost, target): # A*
        (posX, posY) = ghost
        f = 0
        h = f + self.heuristic(posX, posY)
        
        heap = [(f, h, posX, posY, [])] # f(x), heuristic curX, curY, path
        heapq.heapify(heap)
        
        visited = set([(posX, posY)])
        
        DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)] # lên, xuống, phải, trái

        PATH_LIMIT = 100

        while heap:
            (f, h, x, y, path) = heapq.heappop(heap)
            
            if (x, y) == target or len(path) == PATH_LIMIT:
                return path[0] if len(path) > 0 else None

            for dx, dy in DIRECTIONS:
                nx = x + dx
                ny = y + dy
                if not self.isValidPosPowerUp(nx, ny):
                    continue
                while (nx, ny) not in Board.nodes and (nx, ny) != target:
                    nx += dx
                    ny += dy
                    if not self.isValidPosPowerUp(nx, ny):
                        break

                if (nx, ny) not in visited and self.isValidPosPowerUp(nx, ny)\
                    and (nx, ny) != (Object.pinkGhostX, Object.pinkGhostY) \
                    and (nx, ny) != (Object.blueGhostX, Object.blueGhostY) \
                    and (nx, ny) != (Object.orangeGhostX, Object.orangeGhostY) \
                    and (nx, ny) != (Object.pacmanX, Object.pacmanY): #check collision:
                    nh = self.heuristic(nx, ny)
                    nf = f - h + nh + abs(nx - x) + abs(ny - y)
                    heapq.heappush(heap, (nf, nh, nx, ny, path + [(nx, ny)]))
                    visited.add((nx, ny))
        
        return None
    
    def updatePosPowerUp(self, target):
        oldX, oldY = Object.redGhostX, Object.redGhostY
        targetPos = self.getTargetPosPowerUp((oldX, oldY), target)

        if targetPos:
            targetX, targetY = targetPos

            newX, newY = oldX, oldY
            if targetX != oldX:
                newX += (targetX - oldX) // abs(targetX - oldX) 
            if targetY != oldY:
                newY += (targetY - oldY) // abs(targetY - oldY)

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.RED_GHOST

            Object.redGhostX = newX
            Object.redGhostY = newY

    def getTargetPosRelive(self, ghost, target): # A*
        bfs_direction = [(0, -1), (0, 1), (-1, 0), (1, 0)] #trai, phai, tren, duoi
        queue = deque([ghost])
        visited = set([ghost])
        parent = {ghost : None} # con : cha

        if ghost == target: return None

        while queue:
            ghost_x, ghost_y = queue.popleft()

            #Neu gap target
            if (ghost_x, ghost_y) == target:     
                path = [] #list path
                while (ghost_x, ghost_y) != ghost:
                    path.append((ghost_x, ghost_y))
                    (ghost_x, ghost_y) = parent[(ghost_x, ghost_y)]
                path = path[::-1]
                return path[0]

            #Duyet BFS
            for x, y in bfs_direction:
                go_x = ghost_x + x
                go_y = ghost_y + y
                if 0 <= go_x < Board.ROWS and 0 <= go_y < Board.COLS:
                    if (0 <= Board.maze[go_x][go_y] <= 2 or Board.maze[go_x][go_y] == 9) and (go_x, go_y) not in visited:
                        queue.append((go_x, go_y))
                        visited.add((go_x, go_y))
                        parent[(go_x, go_y)] = (ghost_x, ghost_y)                        
        return None
   
    
    def updatePosRelive(self, target):
        oldX, oldY = Object.redGhostX, Object.redGhostY
        targetPos = self.getTargetPosRelive((oldX, oldY), target)

        if targetPos:
            targetX, targetY = targetPos

            newX, newY = oldX, oldY
            if targetX != oldX:
                newX += (targetX - oldX) // abs(targetX - oldX) 
            if targetY != oldY:
                newY += (targetY - oldY) // abs(targetY - oldY)

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.RED_GHOST

            Object.redGhostX = newX
            Object.redGhostY = newY

    def moveRelive(self):
        x, y = Object.redGhostX, Object.redGhostY

        targetX, targetY = Entity.getRealCoordinates((x, y), Object.RED_GHOST_SIZE) # tọa độ thực muốn đi đến
        realX, realY = Object.realRedGhostX, Object.realRedGhostY # tọa độ thực hiện tại

        dx, dy = (targetX - realX), (targetY - realY)
        sX = Config.p_height / 10
        sY = Config.p_width / 10
        if abs(dx) >= sX:
            realX = realX + dx / abs(dx) * sX
        else:
            realX = targetX
        
        if abs(dy) >= sY:
            realY = realY + dy / abs(dy) * sY
        else:
            realY = targetY

        Object.realRedGhostX = realX
        Object.realRedGhostY = realY
    