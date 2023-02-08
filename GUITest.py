from tkinter import *
from multiprocessing import Process, Manager
from joysticController import input_test
import pydirectinput as pyd
import gspeech
import time

target_word = ""
target_key = ""
x_map = ""
y_map = ""
a_map = ""
b_map = ""
left_map = "left"
right_map = "right"
up_map = "up"
down_map = "down"

class GUIMaker(object):
    def __init__(self):
        self.target_word = ""
        self.target_key = ""
        self.x_map = ""
        self.y_map = ""
        self.a_map = ""
        self.b_map = ""

        self.up_map = "up"
        self.down_map = "down"
        self.left_map = "left"
        self.right_map = "right"

        self.tk = Tk()
        self.tk.title('Voice Controller')
        self.entry0 = Entry(self.tk)  # 목표단어
        self.entry1 = Entry(self.tk)  # 맵핑키
        self.entry2 = Entry(self.tk)  # X맵핑
        self.entry3 = Entry(self.tk)  # Y맵핑
        self.entry4 = Entry(self.tk)  # A맵핑
        self.entry5 = Entry(self.tk)  # B맵핑
        self.entry6 = Entry(self.tk)  # left
        self.entry7 = Entry(self.tk)  # right
        self.entry8 = Entry(self.tk)  # up
        self.entry9 = Entry(self.tk)  # down

        self.labelword = Label(self.tk,text='목표 단어').grid(row=0, column=0)
        self.labelkey = Label(self.tk,text='맵핑 키').grid(row=1, column=0)
        self.entry0.grid(row=0,column=1)
        self.entry1.grid(row=1,column=1)

        self.labelX = Label(self.tk,text='X 맵핑').grid(row=2,column=0)
        self.labelY = Label(self.tk,text='Y 맵핑').grid(row=2,column=2)
        self.entry2.grid(row=2,column=1)
        self.entry3.grid(row=2,column=3)

        self.labelA = Label(self.tk,text='A 맵핑').grid(row=3, column=0)
        self.labelB = Label(self.tk,text='B 맵핑').grid(row=3, column=2)
        self.entry4.grid(row=3,column=1)
        self.entry5.grid(row=3,column=3)

        self.labelX = Label(self.tk,text='Left 맵핑').grid(row=4,column=0)
        self.labelY = Label(self.tk,text='Right 맵핑').grid(row=4,column=2)
        self.entry6.grid(row=4,column=1)
        self.entry7.grid(row=4,column=3)

        self.labelA = Label(self.tk,text='Up 맵핑').grid(row=5, column=0)
        self.labelB = Label(self.tk,text='Down 맵핑').grid(row=5, column=2)
        self.entry8.grid(row=5,column=1)
        self.entry9.grid(row=5,column=3)

        self.btn = Button(self.tk,text='Mapping',bg='black',fg='white',command=self.mapping).grid(row=6,column=0)


    def mapping(self):
        global target_word, target_key, x_map, y_map, a_map, b_map, left_map, right_map, up_map, down_map
        self.target_word = self.entry0.get()
        self.target_key = self.entry1.get()
        self.x_map = self.entry2.get()
        self.y_map = self.entry3.get()
        self.a_map = self.entry4.get()
        self.b_map = self.entry5.get()

        self.left_map = self.entry6.get()
        self.right_map = self.entry7.get()
        self.up_map = self.entry8.get()
        self.down_map = self.entry9.get()

        target_word = self.target_word
        target_key = self.target_key
        x_map = self.x_map
        y_map = self.y_map
        a_map = self.a_map
        b_map = self.b_map

        left_map = self.left_map
        right_map = self.right_map
        up_map = self.up_map
        down_map = self.down_map
        """
        key_dict["target_word"] = self.target_word
        key_dict["target_key"] = self.target_key

        key_dict["x_map"] = self.x_map
        key_dict["y_map"] = self.y_map
        key_dict["a_map"] = self.a_map
        key_dict["b_map"] = self.b_map

        key_dict["left_map"] = self.left_map
        key_dict["right_map"] = self.right_map
        key_dict["up_map"] = self.up_map
        key_dict["down_map"] = self.down_map
        """
        #print(key_dict)
        print("mapping")
        self.tk.destroy()
        """        
        print("Key Mapping")
        print(self.target_word)
        print(self.target_key)
        print(self.x_map)
        print(self.y_map)
        print(self.a_map)
        print(self.b_map)
        print(self.up_map)
        print(self.down_map)
        print(self.left_map)
        print(self.right_map)"""


    def run(self):
        self.tk.mainloop()

    def set_initial_setting(self, target_word, target_key, x_map, y_map, a_map, b_map, left_map='left', right_map='right', up_map='up', down_map='down'):
        self.entry0.insert(0, target_word)
        self.entry1.insert(0, target_key)
        self.entry2.insert(0, x_map)
        self.entry3.insert(0, y_map)
        self.entry4.insert(0, a_map)
        self.entry5.insert(0, b_map)
        self.entry6.insert(0, left_map)
        self.entry7.insert(0, right_map)
        self.entry8.insert(0, up_map)
        self.entry9.insert(0, down_map)

        self.target_word = self.entry0.get()
        self.target_key = self.entry1.get()
        self.x_map = self.entry2.get()
        self.y_map = self.entry3.get()
        self.a_map = self.entry4.get()
        self.b_map = self.entry5.get()

        self.left_map = self.entry6.get()
        self.right_map = self.entry7.get()
        self.up_map = self.entry8.get()
        self.down_map = self.entry9.get()

    def get_target_setting(self):
        return [self.target_word, self.target_key]
    def get_button_setting(self):
        return [self.x_map, self.y_map, self.a_map, self.b_map]
    def get_joystic_setting(self):
        return [self.left_map, self.right_map, self.up_map, self.down_map]


def STT_Speech(target_word, target_key):
    gsp = gspeech.Gspeech()
    print("STT code Start")
    print("Target_word : ", target_word, "target_key : ", target_key)
    while True:
        # 음성 인식 될때까지 대기 한다.
        stt = gsp.getText()
        if stt is None:
            break
        print(stt)
        if SamepleTextInChecker(stt, target_word):
            pyd.press([target_key])
        time.sleep(0.001)
        if ('끝' in stt):
            break

def SamepleTextInChecker(stt, target_word):
    text_length = len(target_word)
    user_score = 0
    for i in range(text_length):
        if target_word[i] in stt:
            user_score += 1
    if text_length != 0:
        if user_score/text_length > 0.4:
            return True
    else:
        return False

def Joystic_controller(left_map, right_map, up_map, down_map, x_map,y_map, a_map, b_map):
    #parameter_checker()
    program = input_test()
    program.init()
    program.Axis_Setting(0, [left_map, right_map, up_map, down_map])
    program.Button_Setting_Inst([x_map,y_map, a_map, b_map])
    program.run()  # This function should never return

def parameter_checker():
    global target_word, target_key, x_map, y_map, a_map, b_map, left_map, right_map, up_map, down_map
    print("Key Mapping")
    print(target_word)
    print(target_key)
    print(x_map)
    print(y_map)
    print(a_map)
    print(b_map)
    print(up_map)
    print(down_map)
    print(left_map)
    print(right_map)


if __name__ == "__main__":

    GUI = GUIMaker()
    GUI.set_initial_setting("가", "d", "a", "s", "", "f")
    GUI.run()
    p1 = Process(target=Joystic_controller, args=(left_map, right_map, up_map, down_map, x_map, y_map, a_map, b_map))
    p2 = Process(target=STT_Speech, args=(target_word, target_key))
    p1.start()
    p2.start()
