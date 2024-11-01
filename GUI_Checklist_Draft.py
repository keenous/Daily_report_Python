# ver 1.0.001 希望:1. 重新整理代码,优化打印功能。2. 增加内容框内鼠标三连击,状态改为(已处理,等待对方操作中). 已经增加了任务列别中的任务上下移动功能. 历史：增加打印文件名称按照当天日期名称保存功能。
# Bug：在Entry空间中输入内容后，点击Enter. 内容显示在listbox中，用键盘向下案件选择该任务，点击回车，无法实现在任务内容后增加“（Accomplished）”功能。因为Accomplished功能跟着鼠标光标走，而不是跟着键盘选择走。
# Bug2: 如何实现PDF中显示中文和日语。
# Bug3: 希望实现在输出的PDF中, 上面自动加一列文字显示今天的日期, 如"30-09-2024".
# Bug4: 在输出的PDF中增加当日日期信息.
# 已解决Bug5: 因为目前竖屏(portrait) 导致比较长的任务名称无法显示完整, 希望实现输出的PDF用横屏(Landscape)方式呈现. - 解决方式: 修改代码, 解决日期: 31/10/2024.
# 解决中Bug6: 用Git管理VSCode中修改过的代码. 实现更改后的代码成功stage, 并Comit为一个新生成文件.
# ver 1.0.007 Add 'Daily report' title. Adjust to landscape layout.
# ver 1.0.008 解决Bug7: 解决恢复任务功能不良.　实现点击任务恢复键，双击回车快捷键实现恢复任务至未完成初始状态．解决方法: 调整            original_task = task。£ ver 1.0.009 
# ver 1.0.009 增加撤销(Undo)功能. 在GUI界面中增加撤销功能.



import tkinter as tk  
from tkinter import Listbox, Button, Entry, END, simpledialog, Menu, messagebox
from reportlab.pdfgen import canvas  
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import landscape, A4  
from datetime import datetime  
  
# 字典用于跟踪任务的完成状态  
task_states = {}  

def add_task():  
    task = entry.get()  
    if task:  
        tasks_listbox.insert(END, task)  
        task_states[task] = False  # 默认任务未完成  
        entry.delete(0, tk.END)  
  
def edit_task():  
    selection = tasks_listbox.curselection()  
    if selection:  
        index = selection[0]  
        task = tasks_listbox.get(index)  
        new_task = simpledialog.askstring("编辑任务 (Ctrl+Shift+E)", "输入新的任务名称:", parent=root, initialvalue=task)  
        if new_task:  
            # 更新列表框和任务状态  
            tasks_listbox.delete(index)  
            tasks_listbox.insert(index, new_task)  
            task_states.pop(task, None)  # 移除旧的任务状态（如果不存在则不报错）  
            task_states[new_task] = task_states.get(task, False)  # 使用旧的状态或默认为False  

def restore_task():  
    selection = tasks_listbox.curselection()  
    if selection:  
        index = selection[0]  
        task = tasks_listbox.get(index)  
        if task.endswith('(Accomplished)'):  
            original_task = task[:-15]  
            # 注意：这里没有更新task_states，因为它可能只是简单的布尔值映射  
            tasks_listbox.delete(index)  
            tasks_listbox.insert(index, original_task)  
            # 如果需要，您可以在这里添加逻辑来重置task_states中的值，但这取决于您的具体需求
 
def mark_task_done():  
    selection = tasks_listbox.curselection()  
    if selection:  
        index = selection[0]  
        task = tasks_listbox.get(index)  
        if not task.endswith('(Accomplished)'):  # 确保不会重复添加"(Accomplished)"  
            # 更新任务状态为Accomplished（假设您有这个逻辑）  
            task_states[task] = True  
            # 修改任务字符串，在末尾添加"(Accomplished)"  
            marked_task = task + ' (Accomplished)'  
            # 从列表中删除原始任务，并插入修改后的任务  
            tasks_listbox.delete(index)  
            tasks_listbox.insert(index, marked_task)  
  
def delete_task():  
    selection = tasks_listbox.curselection()  
    if selection:  
        index = selection[0]  
        task = tasks_listbox.get(index)  
        tasks_listbox.delete(index)  
        task_states.pop(task, None)  # 从任务状态中移除该任务

def mark_task_done_if_selected():  
    selection = tasks_listbox.curselection()  
    if selection:  
        mark_task_done()  # 调用现有的 delete_task 函数  
   
def clear_all():  
    # 清除所有 [Ctrl + Delete]任务，并重置任务状态  
    tasks_listbox.delete(0, tk.END)  
    task_states.clear() 

    # 添加一个新函数来检查是否有选中的任务，如果有，则调用 Clear_all_task  


# 全局调用 
# 双击放大缩小
def toggle_maximize(event):  
    # 检查窗口当前状态，如果已最大化则还原，否则最大化  
    if root.wm_state() == 'zoomed':  
        root.wm_state('normal')  
    else:  
        root.wm_state('zoomed')  

# 键盘上下箭头选择
def select_task_with_arrow_keys(event):  
    if event.keysym in ('Up', 'Down'):  
        current_index = tasks_listbox.curselection()  
        if current_index:  
            current_index = current_index[0]  
        else:  
            current_index = 0  # 如果没有选中的项，则从第一项开始  
  
        if event.keysym == 'Up':  
            new_index = max(0, current_index - 1)  
        else:  # event.keysym == 'Down'  
            new_index = min(len(tasks_listbox.get(0, tk.END)) - 1, current_index + 1)  
  
        tasks_listbox.selection_clear(0, tk.END)  # 清除所有 [Ctrl + Delete]选择  
        tasks_listbox.selection_set(new_index)  # 设置新的选择  
        tasks_listbox.see(new_index)  # 确保新选中的项可见  

# 直接调用 clear_all 函数，无论是否有选中项
def clear_all_task_if_selected():  
    clear_all()  

# 定义任务上下移动
def move_task_up():  
    selection = tasks_listbox.curselection()  
    if selection and selection[0] > 0:  
        index = selection[0]  
        current_task = tasks_listbox.get(index)  
        tasks_listbox.delete(index)  
        tasks_listbox.insert(index - 1, current_task)  
        tasks_listbox.selection_set(index - 1)  
  
def move_task_down():  
    selection = tasks_listbox.curselection()  
    if selection and selection[0] < len(tasks_listbox.get(0, tk.END)) - 1:  
        index = selection[0]  
        current_task = tasks_listbox.get(index)  
        tasks_listbox.delete(index)  
        tasks_listbox.insert(index + 1, current_task)  
        tasks_listbox.selection_set(index + 1)  

# 与cursor selection有关的调用
# 对鼠标选择Listbox特定任务 编辑
def edit_task_if_selected():  
    selection = tasks_listbox.curselection()  
    if selection:  
        edit_task()  # 调用现有的 delete_task 函数  

# 鼠标选择Listbox特定任务 完成 
def on_listbox_return(event):  
    if tasks_listbox.curselection():  
        mark_task_done()  

# 对鼠标选择Listbox特定任务 恢复
def on_listbox_doublereturn(event):  
    if tasks_listbox.curselection():  
        restore_task()

# 对鼠标选择Listbox特定任务 删除
def delete_task_if_selected():  
    selection = tasks_listbox.curselection()  
    if selection:  
        delete_task()  # 调用现有的 delete_task 函数  


# 其他定义
# 定义同时按下 Ctrl+Shift+E
def on_shift_e(event):  
    if event.keysym == 'e' and (event.state & 4) and (event.state & 1):  # 检查是否同时按下了 Ctrl、Shift 和 e  
        edit_task()

# 退出确认选项
def on_exit():  
    # 这里可以添加退出前的清理工作，但在这个简单例子中，我们直接销毁主窗口  
    root.destroy()   




   

# 有关pdf print

# 获取当前日期，并格式化为字符串，例如："2023-04-01"  
today_date = datetime.now().strftime("%Y-%m-%d")  

  
def generate_pdf(filename, tasks):  
    # 注册字体，确保文件路径和文件名正确  
    pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))  
   # 设置页面为横屏模式  
    c = canvas.Canvas(filename, pagesize=landscape(A4))  
    y = 350  # 初始y位置，根据PDF页面大小调整  
       # 获取当前日期和星期  
    today = datetime.now()  
    weekday = today.strftime("%A")  # 星期几的英文  
    formatted_date = today.strftime("%d-%m-%Y")  # DD-MM-YYYY  
    full_date_str = f"{formatted_date} ({weekday}) Daily Report"  
      
    # 设置字体和大小  
    c.setFont('SimHei', 12)  
      
    # 绘制日期到PDF的起始位置  
    c.drawString(350, 570, full_date_str)  # 调整x和y位置以适应你的页面布局 
    task_start_y = 540 
    for task in tasks:  
        # 直接使用drawString绘制文本  
        c.drawString(15, task_start_y, task)  # 绘制文本，调整x位置  
        task_start_y -= 20  # 向下移动以绘制下一个任务  
    c.save()
  
def print_tasks():  
    tasks = tasks_listbox.get(0, tk.END)  # 获取所有任务  
    pdf_filename = f"{today_date}_Task list.pdf"  
    generate_pdf(pdf_filename, tasks)  
    import os  
    os.startfile(pdf_filename)

# 创建主窗口  
root = tk.Tk()  
root.title("待办事项")  
  

# 创建一个菜单栏  
menubar = Menu(root) 

# 添加第一个菜单
taskmenu = Menu(menubar, tearoff=0)  
taskmenu.add_command(label="一键输出为PDF", command=print_tasks)  
taskmenu.add_separator()  # 添加一个分隔符  
taskmenu.add_command(label="退出", command=on_exit)   
menubar.add_cascade(label="文件", menu=taskmenu)  

# 添加第二个菜单
taskmenu2 = Menu(menubar, tearoff=0)  
taskmenu2.add_command(label="添加任务 [Enter]", command=add_task)  
taskmenu2.add_command(label="编辑任务 [Ctrl+Shift+E]", command=edit_task_if_selected)  # 绑定到选择后的编辑  
taskmenu2.add_command(label="完成任务 [回车]", command=mark_task_done_if_selected)  # 绑定到选择后的完成  
taskmenu2.add_command(label="恢复任务 [两次回车]", command=on_listbox_doublereturn)  # 假设你需要一个函数来处理选中后的恢复  
taskmenu2.add_command(label="删除任务 [Delete]", command=delete_task_if_selected)  
taskmenu2.add_command(label="清除所有 [Ctrl + Delete]", command=clear_all)  
menubar.add_cascade(label="操作", menu=taskmenu2)  

# 将菜单栏配置到窗口中  
root.config(menu=menubar)  




# 创建控件  
entry = tk.Entry(root, width=100)  
entry.pack(pady=10)  

# 设置Entry控件获得焦点  
entry.focus_set()  # 在这里设置焦点  

# 绑定箭头键到主窗口  
root.bind('<Up>', select_task_with_arrow_keys)  
root.bind('<Down>', select_task_with_arrow_keys)  
  


entry.bind('<Return>', lambda e: add_task())  



# 创建文本栏来 
format_label = tk.Label(root, text="格式示例：いっぷん 1. Johnson-刘佳, e, UDZSTE-175.6B Quotation.")  
format_label.pack(pady=10)  # 使用pack布局管理器，并添加一些垂直填充  

# 创建任务栏
tasks_listbox = Listbox(root, height=30, width=100)  
tasks_listbox.pack(pady=10)  

# 双击邮件启动程序最大化功能  
tasks_listbox.bind('<Double-3>', toggle_maximize)   

# 将各种按键绑定在根窗口上  
root.bind('<Delete>', lambda e: delete_task_if_selected())  
root.bind('<Control-Shift-e>', lambda e: edit_task_if_selected())  
root.bind('<Control-Shift-E>', lambda e: edit_task_if_selected())  
root.bind('<Control-KeyPress-Delete>', lambda e: clear_all_task_if_selected())  
root.bind('<Key>', on_shift_e)  

tasks_listbox.bind('<Return>', on_listbox_return)  
tasks_listbox.bind('<Double-Return>', on_listbox_doublereturn)  

# 程序中的按钮
add_button = Button(root, text="添加任务 [Enter]", command=add_task)  
add_button.pack(side=tk.LEFT, padx=10)  
  
edit_button = Button(root, text="编辑任务 [Ctrl+SHIFT+E]", command=edit_task)  
edit_button.pack(side=tk.LEFT, padx=10)  
  
restore_button = Button(root, text="恢复任务 [两次回车]", command=restore_task)  
restore_button.pack(side=tk.LEFT, padx=10)  
  
done_button = Button(root, text="完成任务 [回车]", command=mark_task_done)  
done_button.pack(side=tk.LEFT, padx=10)  
 
delete_button = Button(root, text="删除任务 [Delete]", command=delete_task)    
delete_button.pack(side=tk.LEFT, padx=10)  

clear_button = Button(root, text="清除所有 [Ctrl + Delete]", command=clear_all)  
clear_button.pack(side=tk.RIGHT, padx=10)  

# 添加向上和向下移动任务的按钮  
move_up_button = Button(root, text="向上移动任务", command=move_task_up)  
move_up_button.pack(side=tk.LEFT, padx=10)  
  
move_down_button = Button(root, text="向下移动任务", command=move_task_down)  
move_down_button.pack(side=tk.LEFT, padx=10)


# 启动事件循环  
root.mainloop()
