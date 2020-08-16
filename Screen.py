from tkinter import *
import time
import math
import threading

from Stabilizer import Stabilizer

def getAngle(point1X, point1Y, point2X, point2Y):
    dx, dy = point2X - point1X, point2Y - point1Y

    if dx == 0:
        if dy < 0:
            return 90
        else:
            return -90

    angle = math.atan(dy / dx) * 180 / math.pi
    if dx > 0:
        angle += 180
    return angle

class Screen(Frame):

    def __init__(self, root):
        super().__init__()
        self.root = root

        self.cameraAngle = 90

        self.stabilizer = Stabilizer(self.cameraAngle, 50, 0.02, 1, 180)

        self.mouseX = 0
        self.mouseY = 0
        self.centerX = 200
        self.centerY = 200
        self.initUI()

    def initUI(self):

        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.draw()

    def draw(self):
        lineLength = 100
        mouseDistance = math.sqrt((self.mouseX - self.centerX) * (self.mouseX - self.centerX) + (self.mouseY - self.centerY) * (self.mouseY - self.centerY))
        point2X = self.centerX + (self.mouseX - self.centerX) * lineLength / mouseDistance
        point2Y = self.centerY + (self.mouseY - self.centerY) * lineLength / mouseDistance

        cameraX = self.centerX + lineLength * math.cos(math.radians(self.cameraAngle + 180))
        cameraY = self.centerY + lineLength * math.sin(math.radians(self.cameraAngle + 180))

        self.canvas.delete("all")

        self.canvas.create_line(self.centerX, self.centerY, point2X, point2Y, fill='black')
        self.canvas.create_line(self.centerX, self.centerY, cameraX, cameraY, fill='red')

        self.canvas.pack(fill=BOTH, expand=1)

    def motion(self, event):
        self.mouseX, self.mouseY = event.x, event.y
        self.draw()

    def retrieveMousePosition(self):
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_rooty()

        self.mouseX, self.mouseY = abs_coord_x, abs_coord_y

        self.updateStabilizer()

    def updateStabilizer(self):
        angle = getAngle(self.centerX, self.centerY, self.mouseX, self.mouseY)
        self.cameraAngle = self.stabilizer.measure(angle)

def mainLoop(root, screen):
    while(True):
        screen.retrieveMousePosition()
        screen.draw()
        time.sleep(0.01)

def main():

    root = Tk()
    screen = Screen(root)
    root.geometry("400x400+100+100")
    #root.bind('<Motion>', screen.motion)

    #mainLoop(root, screen)

    #x = threading.Thread(target=mainLoop, args=(screen,), daemon=True)
    #x.start()

    #root.mainloop()

    while(True):
        root.update()
        screen.retrieveMousePosition()
        screen.draw()
        time.sleep(0.01)


if __name__ == '__main__':
    main()