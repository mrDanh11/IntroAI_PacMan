# # BFS
from .Entity import Entity
from .GhostInterface import GhostInterface
from Config import Config, Material, Board, Object, Mode
from collections import deque

class BlueGhost(GhostInterface):
    def draw(self):#hàm này vẽ con ma xanh
        realX = Object.realBlueGhostX
        realY = Object.realBlueGhostY
        if Mode.BlueGhost == Mode.CHASING:
            Config.screen.blit(Material.BlueGhostImage, (realY, realX))
        elif Mode.BlueGhost == Mode.POWER_UP:
            if Mode.powerupTime <= 60 * 2:
                if Mode.powerupTime // 15 % 2 == 0: 
                    Config.screen.blit(Material.PowerupImage, (realY, realX))
                else:
                    Config.screen.blit(Material.BlueGhostImage, (realY, realX))
            else:
                Config.screen.blit(Material.PowerupImage, (realY, realX))
        else: #dead
            Config.screen.blit(Material.DeadGhostImage, (realY, realX))

    def move(self):#Hàm animation
        x, y = Object.blueGhostX, Object.blueGhostY
        targetX, targetY = Entity.getRealCoordinates((x, y), Object.BLUE_GHOST_SIZE) # tọa độ thực muốn đi đến
        realX, realY = Object.realBlueGhostX, Object.realBlueGhostY # tọa độ thực hiện tại

        dx, dy = (targetX - realX), (targetY - realY)
        sX = Config.p_height / 15
        sY = Config.p_width / 15
        if abs(dx) >= sX:
            realX = realX + dx / abs(dx) * sX
        else:
            realX = targetX
        
        if abs(dy) >= sY:
            realY = realY + dy / abs(dy) * sY
        else:
            realY = targetY

        Object.realBlueGhostX = realX
        Object.realBlueGhostY = realY

    #Hàm tìm đường
    def getTargetPos(self, ghost, pacman):#Tính ô kế tiếp phải đi, phù hợp nếu Pacman di chuyển bởi người chơi.
        bfs_direction = [(0, -1), (0, 1), (-1, 0), (1, 0)] #trai, phai, tren, duoi
        queue = deque([ghost]) #Tạo 1 de-que chứa các tọa độ (x,y)
        visited = set([ghost]) #Tập hợp chứa các tọa độ đã duyệt
        parent = {ghost : None} # node sau : node trước

        if ghost == pacman: return None

        while queue:
            ghost_x, ghost_y = queue.popleft()

            #Nếu gặp Pacman
            if (ghost_x, ghost_y) == pacman:     
                path = [] #list path
                while (ghost_x, ghost_y) != ghost:#Lưu lại các tọa độ đã đi từ Pacman về tọa độ Ghost ban đầu
                    path.append((ghost_x, ghost_y))
                    (ghost_x, ghost_y) = parent[(ghost_x, ghost_y)]#Lấy ra node trước
                path = path[::-1]#Đảo ngược lại list do sau khi lặp, path chứa đường đi từ Pacman về Ghost
                return path[0]

            #Duyet BFS
            for x, y in bfs_direction:
                go_x = ghost_x + x
                go_y = ghost_y + y
                if 0 <= go_x < Board.ROWS and 0 <= go_y < Board.COLS: #Kiểm tra tọa độ MỚI có trong mê cung không
                    if (0 <= Board.maze[go_x][go_y] <= 2 or Board.maze[go_x][go_y] == 9) and (go_x, go_y) not in visited\
                        and (go_x, go_y) != (Object.pinkGhostX, Object.pinkGhostY) \
                        and (go_x, go_y) != (Object.orangeGhostX, Object.orangeGhostY) \
                        and (go_x, go_y) != (Object.redGhostX, Object.redGhostY): #Kiểm tra va chạm với con ma khác và tọa độ MỚI đã được visit chưa
                        queue.append((go_x, go_y))                                  
                        visited.add((go_x, go_y))
                        parent[(go_x, go_y)] = (ghost_x, ghost_y) #Lưu đường đi đến ô tọa độ MỚI (muốn đi đến go_x, go_y phải đi qua ghost_x, ghost_y)                     
        return None
    
    #Hàm tìm đường
    def getTargetPathInformation(self, ghost, pacman): #Dùng trong trường hợp Pacman đứng im, nếu Pacman di chuyển qua tọa độ mới, path trả về ko đúng nữa
        #Khác hàm trên là hàm này có trả về node đã đi và path (list)
        bfs_direction = [(0, -1), (0, 1), (-1, 0), (1, 0)] #trai, phai, tren, duoi
        queue = deque([ghost])
        visited = set([ghost])
        parent = {ghost : None} # con : cha

        expanded_nodes = 0

        if ghost == pacman: return None

        while queue:
            ghost_x, ghost_y = queue.popleft()
            expanded_nodes += 1

            #Neu gap pacman
            if (ghost_x, ghost_y) == pacman:     
                path = [] #list path
                while (ghost_x, ghost_y) != ghost:
                    path.append((ghost_x, ghost_y))
                    (ghost_x, ghost_y) = parent[(ghost_x, ghost_y)]
                path = path[::-1]
                return path, expanded_nodes

            #Duyet BFS
            for x, y in bfs_direction:
                go_x = ghost_x + x
                go_y = ghost_y + y
                if 0 <= go_x < Board.ROWS and 0 <= go_y < Board.COLS:
                    if (0 <= Board.maze[go_x][go_y] <= 2 or Board.maze[go_x][go_y] == 9) and (go_x, go_y) not in visited\
                        and (go_x, go_y) != (Object.pinkGhostX, Object.pinkGhostY) \
                        and (go_x, go_y) != (Object.orangeGhostX, Object.orangeGhostY) \
                        and (go_x, go_y) != (Object.redGhostX, Object.redGhostY):  #check collision::
                        queue.append((go_x, go_y))
                        visited.add((go_x, go_y))
                        parent[(go_x, go_y)] = (ghost_x, ghost_y)                        
        return None, expanded_nodes
    
    def updatePos(self):
        oldX, oldY = Object.blueGhostX, Object.blueGhostY
        newPos = self.getTargetPos((oldX, oldY), (Object.pacmanX, Object.pacmanY))
        
        if newPos:
            newX, newY = newPos

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.BLUE_GHOST

            Object.blueGhostX = newX
            Object.blueGhostY = newY

    def updatePosForEachLv(self, newPos):
        oldX, oldY = Object.blueGhostX, Object.blueGhostY        
        if newPos:
            newX, newY = newPos

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.BLUE_GHOST

            Object.blueGhostX = newX
            Object.blueGhostY = newY

    def getTargetPosPowerUp(self, ghost, target): #Hàm này tránh Pacman khi Pacman ăn viên sức mạnh
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
                #path.append((ghost_x, ghost_y))
                path = path[::-1]
                return path[0]

            #Duyet BFS
            for x, y in bfs_direction:
                go_x = ghost_x + x
                go_y = ghost_y + y
                if 0 <= go_x < Board.ROWS and 0 <= go_y < Board.COLS:
                    if (0 <= Board.maze[go_x][go_y] <= 2 or Board.maze[go_x][go_y] == 9) and (go_x, go_y) not in visited\
                        and (go_x, go_y) != (Object.pinkGhostX, Object.pinkGhostY) \
                        and (go_x, go_y) != (Object.orangeGhostX, Object.orangeGhostY) \
                        and (go_x, go_y) != (Object.redGhostX, Object.redGhostY) \
                        and (go_x, go_y) != (Object.pacmanX, Object.pacmanY): #Thêm tránh va chạm với Pacman, còn lại giống hàm getTargetPos
                        queue.append((go_x, go_y))
                        visited.add((go_x, go_y))
                        parent[(go_x, go_y)] = (ghost_x, ghost_y)                        
        return None
    
    def updatePosPowerUp(self, target):
        oldX, oldY = Object.blueGhostX, Object.blueGhostY
        newPos = self.getTargetPosPowerUp((oldX, oldY), target)
        
        if newPos:
            newX, newY = newPos

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.BLUE_GHOST

            Object.blueGhostX = newX
            Object.blueGhostY = newY

    def getTargetPosRelive(self, ghost, target): #Hàm tìm đường về nơi hồi sinh của Ghost khi bị Pacman ăn trong lúc tăng sức mạnh
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
                #Ma chết thì có thể đi xuyên các con ma khác và pacman
                if 0 <= go_x < Board.ROWS and 0 <= go_y < Board.COLS:
                    if (0 <= Board.maze[go_x][go_y] <= 2 or Board.maze[go_x][go_y] == 9) and (go_x, go_y) not in visited:
                        queue.append((go_x, go_y))
                        visited.add((go_x, go_y))
                        parent[(go_x, go_y)] = (ghost_x, ghost_y)                        
        return None
   
    def updatePosRelive(self, target):
        oldX, oldY = Object.blueGhostX, Object.blueGhostY
        newPos = self.getTargetPosRelive((oldX, oldY), target)
        
        if newPos:
            newX, newY = newPos

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.BLUE_GHOST

            Object.blueGhostX = newX
            Object.blueGhostY = newY
    
    def moveRelive(self):#Hàm animation
        x, y = Object.blueGhostX, Object.blueGhostY

        targetX, targetY = Entity.getRealCoordinates((x, y), Object.BLUE_GHOST_SIZE) # tọa độ thực muốn đi đến
        realX, realY = Object.realBlueGhostX, Object.realBlueGhostY # tọa độ thực hiện tại

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

        Object.realBlueGhostX = realX
        Object.realBlueGhostY = realY

    