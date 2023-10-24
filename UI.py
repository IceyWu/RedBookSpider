import customtkinter
import os
from PIL import Image
from search import Search


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title("小红书")
        self.geometry("700x450")

        # 颜色配置
        customtkinter.set_default_color_theme("assets/theme/theme.json")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/icons")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")),
                                                       size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                                 size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        # search icon
        self.image_icon_search = customtkinter.CTkImage(Image.open(os.path.join(image_path, "search.png")),
                                                        size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="小红书内容提取",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        # 设置默认值-平潭岛
        # self.navigation_frame_label.configure(text="平潭岛")
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="根据搜索爬取",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="根据个人",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="根据热度",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w",
                                                      command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # 搜索框
        self.entry = customtkinter.CTkEntry(self.home_frame, placeholder_text="请输入搜索内容")
        self.entry.grid(row=1, column=0, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        # 搜索按钮
        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="",width=20,
         fg_color="transparent",
         image=self.image_icon_search,
                                                           command=self.button_function)
        self.home_frame_button_1.grid(row=1, column=2)
        # 笔记类型
        self.optionmenu_type = customtkinter.CTkOptionMenu(self.home_frame, dynamic_resizing=False,
                                                           values=["全部", "视频", "图片"])
        self.optionmenu_type.grid(row=2, column=0, padx=(20, 0), pady=(20, 20), sticky="nsw")
        # 排序方式 general: 综合排序 popularity_descending: 热门排序 time_descending: 最新排序
        self.optionmenu_sort = customtkinter.CTkOptionMenu(self.home_frame, dynamic_resizing=False,
                                                           values=["综合排序", "热门排序", "最新排序"])
        self.optionmenu_sort.grid(row=2, column=1, padx=(20, 0), pady=(20, 20), sticky="nsw")
        # 获取的数量（5，10，20，50，100），默认5
        self.optionmenu_num = customtkinter.CTkOptionMenu(self.home_frame, dynamic_resizing=False,
                                                            values=["5", "10", "20", "50", "100"])
        self.optionmenu_num.grid(row=2, column=2, padx=(10, 0), pady=(20, 20), sticky="nsw")

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "根据搜索爬取" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "根据个人" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "根据热度" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

        # 点击事件
        # 获取note_type值并返回
    def get_note_type(self):
        temp_type = self.optionmenu_type.get()
        if temp_type == "全部":
            note_type = 0
        elif temp_type == "视频":
            note_type = 1
        elif temp_type == "图片":
            note_type = 2
        else:
            note_type = 0
        return note_type
        #     获取sort_type值并返回
    def get_sort_type(self):
        temp_type = self.optionmenu_sort.get()
        if temp_type == "综合排序":
            sort_type = "general"
        elif temp_type == "热门排序":
            sort_type = "popularity_descending"
        elif temp_type == "最新排序":
            sort_type = "time_descending"
        else:
            sort_type = "general"
        return sort_type

    def button_function(self):
        # 获取值并打印
        print("搜索内容为：", self.entry.get())
        # 获取type值并打印
        note_type = self.get_note_type()
        print("笔记类型为：", note_type)
        # 获取sort_type值并打印
        sort_type = self.get_sort_type()
        print("排序方式为：", sort_type)
        # 获取num值并打印
        num = self.optionmenu_num.get()
        print("获取的数量为：", num)
        # 将num转为int
        num = int(num)

        # 如果内容为空，则提示，用messagebox
        if self.entry.get() == "":
            print("搜索内容不能为空")
            return


        get_data = Search()
        get_data.main(self.entry.get(), num, sort_type, note_type)
        




if __name__ == "__main__":
    app = App()
    app.mainloop()
