import tkinter as tk

root = tk.Tk()

def create_table(parent, rows, cols):
    for r in range(rows):
        for c in range(cols):
            label = tk.Label(parent, text=f"R{r}C{c}", font=('Courier', 10), relief="solid", padx=5, pady=5)
            label.grid(row=r, column=c, sticky="nsew")

    # Set column and row weights so they behave nicely when resizing
    for c in range(cols):
        parent.grid_columnconfigure(c, weight=1)
    for r in range(rows):
        parent.grid_rowconfigure(r, weight=1)

table_frame = tk.Frame(root)
table_frame.pack(padx=10, pady=10)

create_table(table_frame, 2, 27)

root.mainloop()
