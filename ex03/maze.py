import tkinter as tk
import maze_maker as mm


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

        self.key = ""
        master.bind("<KeyPress>", self.key_down)                                    # key反応配置
        master.bind("<KeyRelease>", self.key_up)

        self.main_proc()

        self.maze = mm.make_maze(15,9)
        mm.show_maze(self.canvas, self.maze)
    
    def key_down(self,e):               #ボタンを押したとき、keyをself.keyに保存
        self.key = e.keysym

    def key_up(self,e):
        self.key = ""

    def main_proc(self):
        if self.key == "Right": self.move_detect_wall("mx", 1)             #矢印で移動を行う
        if self.key == "Left": self.move_detect_wall("mx", -1)
        if self.key == "Down": self.move_detect_wall("my", 1)
        if self.key == "Up": self.move_detect_wall("my", -1)

        self.cx = self.mx*100 + 50
        self.cy = self.my*100 + 50
        self.canvas.coords(self.bird, self.cx, self.cy)             #計算後反映
        self.canvas.tag_raise(self.bird)
        self.master.after(100, self.main_proc)
    

    def move_detect_wall(self, direction, num):                     #壁を判定しつつ移動処理を行う。
        buff_x, buff_y = self.mx,self.my
        if direction == "mx":
            self.mx += num
        elif direction == "my":
            self.my += num
        if self.maze[self.mx][self.my] == 1:
            self.mx, self.my = buff_x, buff_y




def main():
    win = tk.Tk()
    app = Application(master = win)
    
    app.mainloop()

if __name__ == "__main__":
    main()

