import tkinter as tk
from tkinter import ttk

def abrir_ui(instruments):

    def atualizar_status():
        for row in tree.get_children():
            tree.delete(row)

        for name, inst in instruments.items():
            status = "Tocando" if inst.is_playing() else "Pausado"
            tree.insert("", "end", values=(name, status, inst.bpm, f"{inst.volume:.2f}"))

        root.after(2000, atualizar_status)

    root = tk.Tk()
    root.title("🎚 DJ Monitor")
    root.geometry("400x250")

    cols = ("Instrumento", "Status", "BPM", "Volume")
    tree = ttk.Treeview(root, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(expand=True, fill="both")

    atualizar_status()

    root.mainloop()
