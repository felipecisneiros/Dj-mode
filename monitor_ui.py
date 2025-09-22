import tkinter as tk
from tkinter import ttk

def abrir_ui(instruments):
    """Abre uma janela Tkinter que mostra o status dos instrumentos em tempo real"""

    def atualizar_status():
        for row in tree.get_children():
            tree.delete(row)

        for name, inst in instruments.items():
            status = "Tocando" if inst.is_playing() else "Pausado"
            cor = "green" if inst.is_playing() else "red"

            tree.insert("", "end", values=(name, status, inst.bpm, f"{inst.volume:.2f}"),
                        tags=(cor,))

        for widget in barra_frame.winfo_children():
            widget.destroy()

        for name, inst in instruments.items():
            tk.Label(barra_frame, text=f"{name}", anchor="w").pack(fill="x")
            vol = ttk.Progressbar(barra_frame, maximum=1.0, value=inst.volume, length=200)
            vol.pack(fill="x", pady=2)

        root.after(2000, atualizar_status)

    root = tk.Tk()
    root.title("🎚 DJ Monitor")
    root.geometry("600x400")

    style = ttk.Style(root)
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
    style.configure("Treeview", font=("Arial", 10))

    cols = ("Instrumento", "Status", "BPM", "Volume")
    tree = ttk.Treeview(root, columns=cols, show="headings", height=8)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    tree.tag_configure("green", foreground="green")
    tree.tag_configure("red", foreground="red")
    tree.pack(side="top", expand=True, fill="both", pady=10)

    barra_frame = tk.Frame(root)
    barra_frame.pack(side="bottom", fill="x", padx=10, pady=10)

    atualizar_status()

    root.mainloop()
