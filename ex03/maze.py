import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()

        master.title("迷えるこうかとん")
        master.resizable(width=False, height=False)

        self.image = tk.PhotoImage(file="fig/2.png")
        self.canvas = tk.Canvas(master, width=1500, height=900, bg="black")
        self.canvas.pack()

        self.cx = 300
        self.cy = 400
        self.canvas.create_image(self.cx,self.cy,image=self.image)

        self.key = ""
        master.bind("<KeyPress>", self.key_down)
        master.bind("<KeyRelease>", self.key_up)
    
    
    def key_down(self,e):
        self.key = e.keysym
        print(self.key)

    def key_up(self,e):
        self.key = ""
        print(self.key)




def main():
    win = tk.Tk()
    app = Application(master = win)
    app.mainloop()

if __name__ == "__main__":
    main()

