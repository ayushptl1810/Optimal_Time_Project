import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil
import os
root1 = tk.Tk()
root1.geometry("800x800")
dept_name = ["coding","mech","elex","marketing"]
priority_name = ["Juniors","Seniors","All"]

def upload_image():
            file_path = filedialog.askopenfilename()
            if file_path: 
                save_image(file_path)

def save_image(file_path):
        save_dir = "C:\\Users\\Lenovo\\OneDrive\\Desktop\\CodingTask1Phnx"
        filename = os.path.basename(file_path)
        shutil.copy(file_path, os.path.join(save_dir, filename))
        print("Image saved to:", os.path.join(save_dir, filename))

def insertion():
    input_no = int(insert_box.get("1.0","2.0"))
    for root in range(input_no):
        image_uploaded=False
        root = tk.Tk()
        root.title("Uploader")
        root.geometry("500x500")
        name = tk.Label(root,text="Enter name:",font=('Arial',18))
        name.pack(padx=10,pady=10)
        textbox1 = tk.Text(root,height=2,font=(12))
        textbox1.pack(padx=10,pady=10)

        x=tk.IntVar()
        for i in range(len(dept_name)):
            dept = tk.Radiobutton(root,text=dept_name[i],variable=x,value=i)
            dept.pack(padx=10,pady=10)
        x=tk.IntVar()    
        for i in range(len(priority_name)):
            type = tk.Radiobutton(root,text=priority_name[i],variable=x,value=i)
            type.pack(padx=10,pady=10)  

        upload_button = tk.Button(root, text="Upload Image", command=upload_image)
        upload_button.pack(pady=10)
        image_label = tk.Label(root)
        image_label.pack()

        input_no+=1

insert_label = tk.Label(text="Insert no of people:")
insert_label.pack(padx=10,pady=10)
insert_box = tk.Text(root1,height=4)
insert_box.pack()
insert_button = tk.Button(text="Insert",command=insertion)
insert_button.pack(padx=10,pady=10)

root1.mainloop()
