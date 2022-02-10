import time
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import random

Builder.load_file('game.kv')

time_start = 0.0
time_sum = 0.0
# 点击次数
num_tap = 0
# 地雷数
mine_num = 0
# 地雷坐标列表
mine_pos = []
# 按键坐标字典
dict_btn_pos = {}
# 功能标签
func = [4]
# 地雷周边数字标签
tips_Mine = {}
# 数字颜色字典
color_num = {1: '[color=0000FF]1[/color]', 2: '[color=00FF00]2[/color]', 3: '[color=FF0000]3[/color]',
             4: '[color=0000CD]4[/color]', 5: '[color=CD2626]5[/color]', 6: '[color=2E8B57]6[/color]',
             7: '[color=FFFF00]7[/color]', 8: '[color=CD9B1D]8[/color]'}


class GameWin(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 把每个btn的id和变量绑定
        for i in range(12):
            for j in range(8):
                # 一个键对应一个方格
                dict_btn_pos[i * 10 + j] = self.ids['b' + str(i * 10 + j)]
                dict_btn_pos[i * 10 + j].name = str(i * 10 + j)
                dict_btn_pos[i * 10 + j].bind(on_release=self.tap_func)
        tap = self.ids.tap
        flag = self.ids.flag
        q_mk = self.ids.not_sure
        # quit = self.ids.quit
        tap.bind(on_release=self.tap_func)
        flag.bind(on_release=self.tap_func)
        q_mk.bind(on_release=self.tap_func)
        # quit.bind(on_release=self.quit_game)

    # 功能选择
    def tap_func(self, instance):
        # 首先确认要标记的方式:排雷、插旗、？
        global num_tap
        global mine_num
        if instance.text == 'Tap':  # 普通排雷
            func[0] = 0
            self.ids.info.text = '[color=00FF00]Tap Function[/color]'
            instance.background_color = (1.0, 0.0, 1.0, 1)
            self.ids.flag.background_color = (1.0, 0.65, 0.0, 1)
            self.ids.not_sure.background_color = (1.0, 0.65, 0.0, 1)
        elif instance.text == 'Flag':
            func[0] = 1
            self.ids.info.text = '[color=00FF00]Flag Function[/color]'
            instance.background_color = (1.0, 0.0, 1.0, 1)
            self.ids.tap.background_color = (1.0, 0.65, 0.0, 1)
            self.ids.not_sure.background_color = (1.0, 0.65, 0.0, 1)
        elif instance.text == '?':
            func[0] = 2
            self.ids.info.text = '[color=00FF00]? Function[/color]'
            instance.background_color = (1.0, 0.0, 1.0, 1)
            self.ids.tap.background_color = (1.0, 0.65, 0.0, 1)
            self.ids.flag.background_color = (1.0, 0.65, 0.0, 1)
        elif instance.text == '' and func[0] == 4:
            self.ids.info.text = '[color=00FF00]Please choose\none function below[/color]'
        else:
            # 如果是普通排雷功能
            if func[0] == 0:
                num_tap += 1
                if num_tap == 1:
                    # 当排雷次数为1时才开始生成地雷并开始计时
                    Random_mine_pos(mine_num, int(instance.name))
                self.time_count(num_tap)
                self.show(instance)
                # 当排雷次数等于格子数-地雷数（即除了地雷外都排完），则胜利
                if num_tap == 12 * 8 - mine_num:
                    self.ids.info.text = '[color=FFD700]You Win[/color]'
                    for i in mine_pos:
                        self.ids['b' + str(i)].text = '[color=FF0000]M[/color]'
                        self.ids['b' + str(i)].font_size = 22
                        self.ids['b' + str(i)].markup = True
                        self.ids['b' + str(i)].disabled = True

            elif func[0] == 1:
                self.flag_mine(instance)
            elif func[0] == 2:
                self.q_mark(instance)

    # 排雷
    def show(self, instance):
        global num_tap
        temp = int(instance.name)
        # 如果排到地雷,显示所有地雷,并禁用所有功能键
        if temp in mine_pos:
            self.ids.info.text = '[color=FF0000]You Fail[/color]'
            self.ids.tap.disabled = True
            self.ids.flag.disabled = True
            self.ids.not_sure.disabled = True
            self.time_count(num_tap)
            func[0] = 5
            for i in mine_pos:
                self.ids['b' + str(i)].text = '[color=FF0000]M[/color]'
                self.ids['b' + str(i)].font_size = 22
                self.ids['b' + str(i)].markup = True
                self.ids['b' + str(i)].disabled = True

        elif (temp in tips_Mine) and (temp not in mine_pos) and (temp in dict_btn_pos):
            self.ids['b' + str(temp)].disabled = True
            self.ids['b' + str(temp)].text = color_num[tips_Mine[temp]]
            self.ids['b' + str(temp)].markup = True
            self.ids['b' + str(temp)].font_size = 22
        # 如果碰到空砖块，则显示空格直到遇到数字为止
        elif temp not in tips_Mine and temp not in mine_pos:
            self.clear_E(temp)

    # 递归排除空格
    def clear_E(self, temp):
        global num_tap
        self.ids['b' + str(temp)].disabled = True
        if (temp - 1 not in tips_Mine) and (temp - 1 in dict_btn_pos) and (temp - 1 not in mine_pos) and (
                self.ids['b' + str(temp - 1)].disabled != True):
            self.ids['b' + str(temp - 1)].disabled = True
            num_tap += 1
            self.clear_E(temp - 1)
        elif (temp - 1 in tips_Mine) and (temp - 1 in dict_btn_pos) and (temp - 1 not in mine_pos) and (
                self.ids['b' + str(temp - 1)].disabled != True):
            self.ids['b' + str(temp - 1)].disabled = True
            self.ids['b' + str(temp - 1)].text = color_num[tips_Mine[temp - 1]]
            self.ids['b' + str(temp - 1)].markup = True
            self.ids['b' + str(temp - 1)].font_size = 22
            num_tap += 1

        if (temp + 1 not in tips_Mine) and (temp + 1 in dict_btn_pos) and (temp + 1 not in mine_pos) and (
                self.ids['b' + str(temp + 1)].disabled != True):
            self.ids['b' + str(temp + 1)].disabled = True
            num_tap += 1
            self.clear_E(temp + 1)
        elif (temp + 1 in tips_Mine) and (temp + 1 in dict_btn_pos) and (temp + 1 not in mine_pos) and (
                self.ids['b' + str(temp + 1)].disabled != True):
            self.ids['b' + str(temp + 1)].disabled = True
            self.ids['b' + str(temp + 1)].text = color_num[tips_Mine[temp + 1]]
            self.ids['b' + str(temp + 1)].markup = True
            self.ids['b' + str(temp + 1)].font_size = 22
            num_tap += 1

        if (temp + 10 not in tips_Mine) and (temp + 10 in dict_btn_pos) and (temp + 10 not in mine_pos) and (
                self.ids['b' + str(temp + 10)].disabled != True):
            self.ids['b' + str(temp + 10)].disabled = True
            num_tap += 1
            self.clear_E(temp + 10)
        elif (temp + 10 in tips_Mine) and (temp + 10 in dict_btn_pos) and (temp + 10 not in mine_pos) and (
                self.ids['b' + str(temp + 10)].disabled != True):
            self.ids['b' + str(temp + 10)].disabled = True
            self.ids['b' + str(temp + 10)].text = color_num[tips_Mine[temp + 10]]
            self.ids['b' + str(temp + 10)].markup = True
            self.ids['b' + str(temp + 10)].font_size = 22
            num_tap += 1

        if (temp - 10 not in tips_Mine) and (temp - 10 in dict_btn_pos) and (temp - 10 not in mine_pos) and (
                self.ids['b' + str(temp - 10)].disabled != True):
            self.ids['b' + str(temp - 10)].disabled = True
            num_tap += 1
            self.clear_E(temp - 10)
        elif (temp - 10 in tips_Mine) and (temp - 10 in dict_btn_pos) and (temp - 10 not in mine_pos) and (
                self.ids['b' + str(temp - 10)].disabled != True):
            self.ids['b' + str(temp - 10)].disabled = True
            self.ids['b' + str(temp - 10)].text = color_num[tips_Mine[temp - 10]]
            self.ids['b' + str(temp - 10)].markup = True
            self.ids['b' + str(temp - 10)].font_size = 22
            num_tap += 1

    # 插旗
    def flag_mine(self, instance):
        if instance.text == '[color=FF3030]F[/color]':
            instance.text = ''
        else:
            instance.text = '[color=FF3030]F[/color]'
            instance.font_size = 25
            instance.markup = True

    # 疑问
    def q_mark(self, instance):
        if instance.text == '[color=000000]?[/color]':
            instance.text = ''
        else:
            instance.text = '[color=000000]?[/color]'
            instance.font_size = 25
            instance.markup = True

    # 计时
    def time_count(self, tap_time):
        global time_sum, time_start
        temp = 1
        if temp == tap_time:
            time_start = time.time()
        if temp != tap_time:
            time_end = time.time()
            time_sum = time_end - time_start
            a = time.ctime(time_sum)
            self.ids.time.text = '[color=FF0000]' + a[14:19] + '[/color]'

    # 返回主界面
    def quit_game(self):
        self.parent.parent.current = 'scrn_beg'
        self.clear_widgets()
        self.__init__()
        init_data()


# 生成地雷坐标并加入列表
def Random_mine_pos(Num_mine, first_grid):
    num = 0
    while num < Num_mine:
        i = random.randint(0, 11)
        j = random.randint(0, 7)
        pos = i * 10 + j
        if pos in mine_pos or pos == first_grid:
            continue
        else:
            mine_pos.append(pos)
            num += 1
            Tips_init(pos)
    print(mine_pos)



def Tips_init(Mine_pos):
    ge = Mine_pos % 10
    shi = int((Mine_pos - ge) / 10 % 10)
    bai = int(Mine_pos / 100) % 10
    for i in range(ge - 1, ge + 2):
        for j in range(shi - 1, shi + 2):
            tips_pos = (bai * 100) + (j * 10) + i
            if tips_pos not in mine_pos:
                tips_Mine.setdefault(tips_pos, 0)
                tips_Mine[tips_pos] += 1

# 根据地雷坐标生成提示数字并存储到字典中
# def Tips_init2(Mine_pos):
#     tips_Mine.setdefault(Mine_pos-10, 0)
#     tips_Mine[Mine_pos-10] += 1
#     tips_Mine.setdefault(Mine_pos - 9, 0)
#     tips_Mine[Mine_pos - 9] += 1
#     tips_Mine.setdefault(Mine_pos - 11, 0)
#     tips_Mine[Mine_pos - 11] += 1
#     tips_Mine.setdefault(Mine_pos - 1, 0)
#     tips_Mine[Mine_pos - 1] += 1
#     tips_Mine.setdefault(Mine_pos + 10, 0)
#     tips_Mine[Mine_pos + 10] += 1
#     tips_Mine.setdefault(Mine_pos + 9, 0)
#     tips_Mine[Mine_pos + 9] += 1
#     tips_Mine.setdefault(Mine_pos + 11, 0)
#     tips_Mine[Mine_pos + 11] += 1
#     tips_Mine.setdefault(Mine_pos + 1, 0)
#     tips_Mine[Mine_pos + 1] += 1

# 根据难度传递地雷数
def Create_num_mine(Num):
    global mine_num
    mine_num = Num


# 初始化所有数据
def init_data():
    global num_tap, time_sum, time_start, time_end
    time_sum = 0.0
    num_tap = 0
    time_start = 0.0

    mine_pos.clear()
    func[0] = 4
    tips_Mine.clear()

# class gameApp(App):
#     def build(self):
#         return GameWin()
#
#
# if __name__ == '__main__':
#     gameApp().run()
