from .Entity import Entity
import pygame
from Config import Config

class GhostInterface(Entity):
  def draw(self): # Vẽ ghost lên màn hình
    pass

  def getTargetPos(self, ghost, pacman): # Tọa độ (x,y) tiếp theo ghost sẽ đi tới
    pass
  
  def updatePos(self): # Cập nhật tọa độ mới cho ghost (cập nhật mảng coordinates)
    pass

  def move(self, position: tuple): # chưa biết để làm gì
    pass
