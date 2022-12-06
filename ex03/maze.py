import tkinter as tk
import maze_maker as mm
import copy
import pickle as cPickle


class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()

        master.title("迷えるこうかとん")            #ウィンドウ設定
        master.resizable(width=False, height=False)

        self.image = tk.PhotoImage(file="fig/2.png")
        self.canvas = tk.Canvas(master, width=1500, height=900, bg="black")        # cavas配置
        self.canvas.pack()

        self.mx,self.my = 1, 1
        self.bird = self.canvas.create_image(150,150,image=self.image)              # 画像配置

        self.HP_bar = self.canvas.create_rectangle(
            0, 5, 1500, 20, fill="#00ff00")

        self.key = ""
        master.bind("<KeyPress>", self.key_down)                                    # key反応配置
        master.bind("<KeyRelease>", self.key_up)

        self.maze = mm.make_maze(15, 9)
        self.maze_after1 = cPickle.loads(cPickle.dumps(self.maze, -1))
        for i in range(1, 14):
            for j in range(1, 8):
                if (i + j) % 2 == 0:
                    self.maze_after1[i][j] = 4
        self.maze_after1[1][1] = 2
        self.maze_after1[13][7] = 3

        self.maze_after2 = cPickle.loads(cPickle.dumps(self.maze, -1))
        for i in range(1, 14):
            for j in range(1, 8):
                if (i + j) % 2 == 1:
                    self.maze_after2[i][j] = 4
        self.maze_after2[1][1] = 2
        self.maze_after2[13][7] = 3


        self.timer = 0
        self.HP = 300
        self.tick = 0
        self.main_proc()
        self.rythm()
    

    def key_down(self,e):               #ボタンを押したとき、keyをself.keyに保存
        self.key = e.keysym


    def key_up(self,e):
        self.key = ""

    def main_proc(self):
        if self.timer == 0:
            if self.key == "Right": self.move_detect_wall("mx", 1)             #矢印で移動を行う
            if self.key == "Left": self.move_detect_wall("mx", -1)
            if self.key == "Down": self.move_detect_wall("my", 1)
            if self.key == "Up": self.move_detect_wall("my", -1)
        if self.key == "":
            self.timer = 0
        else:
            self.timer += 1
            if self.timer >= 25:
                self.timer = 0
        
        if (self.tick == 1 and self.maze_after1[self.mx][self.my] == 4) or (self.tick == 0 and self.maze_after2[self.mx][self.my] == 4):
            self.HP -= 1
            if self.HP <= 0:
                self.mx, self.my = 1, 1
                self.HP = 300

        self.cx = self.mx*100 + 50
        self.cy = self.my*100 + 50
        self.canvas.coords(self.bird, self.cx, self.cy)             #計算後反映
        self.canvas.coords(self.HP_bar, 0,5,1500*self.HP/300,20)
        self.canvas.tag_raise(self.bird)
        self.canvas.tag_raise(self.HP_bar)
        self.master.after(4, self.main_proc)


    def move_detect_wall(self, direction, num):                     #壁を判定しつつ移動処理を行う。
        buff_x, buff_y = self.mx,self.my
        if direction == "mx":
            self.mx += num
        elif direction == "my":
            self.my += num
        if self.maze[self.mx][self.my] == 1:
            self.mx, self.my = buff_x, buff_y


    def rythm(self):
        self.canvas.delete("map")
        if self.tick == 0:
            mm.show_maze(self.canvas, self.maze_after1)
            self.tick = 1
        else:
            mm.show_maze(self.canvas, self.maze_after2)
            self.tick = 0
        self.master.after(500, self.rythm)


def main():
    win = tk.Tk()
    app = Application(master = win)
    
    app.mainloop()


if __name__ == "__main__":
    main()

