import tkinter as tk
import random
import json
import os

# 餐廳列表
categories = {
    "住宿區": ["家鄉水餃", "山洞點", "甘泉鴨肉麵", "民生炒手", "民族鍋+其他", "50嵐", 
              "麥當勞", "肯德基", "必勝客", "真功夫", "阿滿早餐", "7-11"],
    "工作區": ["工作區餐廳1", "工作區餐廳2", "工作區餐廳3", "工作區餐廳4", "工作區餐廳5"],
    "遠區": ["遠區餐廳1", "遠區餐廳2", "遠區餐廳3", "遠區餐廳4", "遠區餐廳5"]
}

# 保存文件的路徑
SAVE_FILE = "restaurants.json"

# 當前選擇的分類
current_category = "住宿區"

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return categories

def save_data():
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(categories, file, ensure_ascii=False, indent=4)

def update_category():
    global current_category
    current_category = category_var.get()
    update_restaurant_list()

def update_restaurant_list():
    listbox.delete(0, tk.END)
    for item in categories[current_category]:
        listbox.insert(tk.END, item)

def get_random_restaurant():
    if categories[current_category]:
        restaurant = random.choice(categories[current_category])
        result_label.config(text=f"你可以去: {restaurant}")
    else:
        result_label.config(text="沒有可選擇的餐廳")

def add_restaurant():
    new_restaurant = entry.get()
    if new_restaurant:
        categories[current_category].append(new_restaurant)
        update_restaurant_list()
        entry.delete(0, tk.END)
        save_data()

def delete_restaurant():
    selected_restaurant = listbox.get(tk.ACTIVE)
    if selected_restaurant in categories[current_category]:
        categories[current_category].remove(selected_restaurant)
        update_restaurant_list()
        save_data()

# 加載數據
categories = load_data()

# 創建主窗口
root = tk.Tk()
root.title("隨機吃啥產生器")

# 選擇分類
category_var = tk.StringVar(value="住宿區")
category_label = tk.Label(root, text="請選擇分類：")
category_label.pack(pady=5)

category_menu = tk.OptionMenu(root, category_var, "住宿區", "工作區", "遠區", command=lambda _: update_category())
category_menu.pack(pady=5)

# 餐廳列表
listbox = tk.Listbox(root)
listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
update_restaurant_list()

# 隨機選擇按鈕
generate_button = tk.Button(root, text="吃什麼？", command=get_random_restaurant)
generate_button.pack(pady=5)

# 顯示結果
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# 添加和刪除餐廳功能
entry = tk.Entry(root)
entry.pack(pady=5)

add_button = tk.Button(root, text="添加餐廳", command=add_restaurant)
add_button.pack(pady=5)

delete_button = tk.Button(root, text="刪除選中餐廳", command=delete_restaurant)
delete_button.pack(pady=5)

# 運行主循環
root.mainloop()
