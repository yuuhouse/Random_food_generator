import tkinter as tk
from tkinter import ttk
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

def add_category():
    new_category = new_category_entry.get()
    if new_category and new_category not in categories:
        categories[new_category] = []
        category_menu['menu'].add_command(label=new_category, command=tk._setit(category_var, new_category))
        category_var.set(new_category)
        update_category()
        new_category_entry.delete(0, tk.END)
        save_data()

def delete_category():
    global current_category
    selected_category = category_var.get()
    if selected_category in categories:
        del categories[selected_category]
        category_menu['menu'].delete(selected_category)
        current_category = list(categories.keys())[0] if categories else ""
        category_var.set(current_category)
        update_category()
        save_data()

# 加載數據
categories = load_data()

# 創建主窗口
root = tk.Tk()
root.title("隨機吃啥產生器V3")
root.geometry("600x750")
root.configure(bg="#f0f0f0")

# 樣式設置
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#3498db", font=("Microsoft JhengHei", 10))
style.map("TButton", background=[('active', '#2980b9')])
style.configure("TEntry", padding=6, relief="flat", font=("Microsoft JhengHei", 10))
style.configure("TLabel", background="#f0f0f0", font=("Microsoft JhengHei", 10))

# 標題
title_label = tk.Label(root, text="隨機吃啥產生器V3", font=("Microsoft JhengHei", 18, "bold"), bg="#f0f0f0", fg="#2c3e50")
title_label.pack(pady=20)

# 選擇分類
category_frame = tk.Frame(root, bg="#f0f0f0")
category_frame.pack(pady=10)

category_label = tk.Label(category_frame, text="請選擇分類：", font=("Microsoft JhengHei", 12), bg="#f0f0f0")
category_label.pack(side=tk.LEFT, padx=5)

category_var = tk.StringVar(value="住宿區")
category_menu = tk.OptionMenu(category_frame, category_var, *categories.keys(), command=lambda _: update_category())
category_menu.config(font=("Microsoft JhengHei", 10))
category_menu.pack(side=tk.LEFT, padx=5)

# 添加和刪除分類
category_manage_frame = tk.Frame(root, bg="#f0f0f0")
category_manage_frame.pack(pady=10)

new_category_entry = ttk.Entry(category_manage_frame, font=("Microsoft JhengHei", 10))
new_category_entry.pack(side=tk.LEFT, padx=5)

add_category_button = tk.Button(category_manage_frame, text="添加分類", font=("Microsoft JhengHei", 9), command=add_category)
add_category_button.pack(side=tk.LEFT, padx=1)

delete_category_button = tk.Button(category_manage_frame, text="刪除分類", font=("Microsoft JhengHei", 9), command=delete_category)
delete_category_button.pack(side=tk.LEFT, padx=1)

# 餐廳列表
listbox_frame = tk.Frame(root, bg="#f0f0f0")
listbox_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

listbox_label = tk.Label(listbox_frame, text="餐廳列表：", font=("Microsoft JhengHei", 12), bg="#f0f0f0")
listbox_label.pack()

listbox = tk.Listbox(listbox_frame, font=("Microsoft JhengHei", 10))
listbox.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
update_restaurant_list()

# 隨機選擇按鈕
generate_button = tk.Button(root, text="吃什麼？", font=("Microsoft JhengHei", 12, "bold"), bg="#4CAF50", fg="white", command=get_random_restaurant)
generate_button.pack(pady=10)

# 顯示結果
result_label = tk.Label(root, text="", font=("Microsoft JhengHei", 12), bg="#f0f0f0")
result_label.pack(pady=10)

# 添加和刪除餐廳功能
entry_frame = tk.Frame(root, bg="#f0f0f0")
entry_frame.pack(pady=10)

entry = ttk.Entry(entry_frame, font=("Microsoft JhengHei", 10))
entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(entry_frame, text="添加餐廳", font=("Microsoft JhengHei", 10), bg="#2196F3", fg="white", command=add_restaurant)
add_button.pack(side=tk.LEFT, padx=3)

delete_button = tk.Button(root, text="刪除選中餐廳", font=("Microsoft JhengHei", 10), bg="#f44336", fg="white", command=delete_restaurant)
delete_button.pack(pady=20)
# 運行主循環
root.mainloop()
