import os
import subprocess
import tkinter as tk
from tkinter import filedialog


def select_file(entry):
    filename = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)


def select_files(entry):
    filenames = filedialog.askopenfilenames()
    entry.insert(tk.END, " ".join(filenames) + " ")


def select_folder(entry):
    foldername = filedialog.askdirectory()
    entry.insert(tk.END, foldername + " ")


def copy_to_clipboard(command):
    root.clipboard_clear()
    root.clipboard_append(command)
    root.update()
    output_label.config(text="Comando copiado para a área de transferência!")


def generate_command():
    main_script = main_entry.get()
    if not main_script or not os.path.isfile(main_script):
        output_label.config(text="Arquivo inválido!")
        return

    script_dir = os.path.dirname(main_script)

    assets = assets_entry.get().strip()
    assets_options = ""
    if assets:
        for item in assets.split(" "):
            if os.path.isdir(item):
                assets_options += f' --add-data "{item}":.'
            elif os.path.isfile(item):
                assets_options += f' --add-data "{item}":.'

    icon = icon_entry.get()
    icon_option = f'--icon="{icon}"' if icon else ""

    onefile_option = "--onefile" if onefile_var.get() == 1 else "--onedir"
    console_option = "--noconsole" if console_var.get() == 1 else "--console"

    command = f'cd "{script_dir}" && pyinstaller {onefile_option} {console_option} {icon_option} {assets_options} "{main_script}"'
    output_label.config(text=f"Comando gerado:\n{command}")

    copy_button.config(command=lambda: copy_to_clipboard(command))

    if execute_var.get():
        subprocess.run(command, shell=True)
        output_label.config(text="Compilação concluída!")


def create_gui():
    global root, main_entry, assets_entry, icon_entry, onefile_var, console_var, execute_var, output_label, copy_button

    root = tk.Tk()
    root.title("Gerador PyInstaller")
    root.geometry("750x550")
    root.configure(bg="#f0f0f0")

    def add_spacing(frame):
        for widget in frame.winfo_children():
            widget.grid_configure(padx=5, pady=5)

    frame_main = tk.Frame(root, bg="#f0f0f0")
    frame_main.pack(pady=10)
    tk.Label(frame_main, text="Arquivo Principal:", bg="#f0f0f0").grid(row=0, column=0)
    main_entry = tk.Entry(frame_main, width=50)
    main_entry.grid(row=0, column=1)
    tk.Button(
        frame_main, text="Selecionar", command=lambda: select_file(main_entry)
    ).grid(row=0, column=2)
    add_spacing(frame_main)

    frame_assets = tk.Frame(root, bg="#f0f0f0")
    frame_assets.pack(pady=10)
    tk.Label(frame_assets, text="Arquivos/Pastas Adicionais:", bg="#f0f0f0").grid(
        row=0, column=0
    )
    assets_entry = tk.Entry(frame_assets, width=50)
    assets_entry.grid(row=0, column=1)
    tk.Button(
        frame_assets,
        text="Adicionar Arquivo",
        command=lambda: select_files(assets_entry),
    ).grid(row=0, column=2)
    tk.Button(
        frame_assets,
        text="Adicionar Pasta",
        command=lambda: select_folder(assets_entry),
    ).grid(row=0, column=3)
    add_spacing(frame_assets)

    frame_icon = tk.Frame(root, bg="#f0f0f0")
    frame_icon.pack(pady=10)
    tk.Label(frame_icon, text="Ícone (.ico):", bg="#f0f0f0").grid(row=0, column=0)
    icon_entry = tk.Entry(frame_icon, width=50)
    icon_entry.grid(row=0, column=1)
    tk.Button(
        frame_icon, text="Selecionar", command=lambda: select_file(icon_entry)
    ).grid(row=0, column=2)
    add_spacing(frame_icon)

    options_frame = tk.Frame(root, bg="#f0f0f0")
    options_frame.pack(pady=10)

    tk.Label(options_frame, text="Modo de Empacotamento:", bg="#f0f0f0").grid(
        row=0, column=0
    )
    onefile_var = tk.IntVar(value=1)
    tk.Radiobutton(
        options_frame,
        text="Único arquivo (--onefile)",
        variable=onefile_var,
        value=1,
        bg="#f0f0f0",
    ).grid(row=0, column=1)
    tk.Radiobutton(
        options_frame,
        text="Pasta de arquivos (--onedir)",
        variable=onefile_var,
        value=0,
        bg="#f0f0f0",
    ).grid(row=0, column=2)

    tk.Label(options_frame, text="Modo do Console:", bg="#f0f0f0").grid(row=1, column=0)
    console_var = tk.IntVar(value=1)
    tk.Radiobutton(
        options_frame,
        text="Ocultar console (--noconsole)",
        variable=console_var,
        value=1,
        bg="#f0f0f0",
    ).grid(row=1, column=1)
    tk.Radiobutton(
        options_frame,
        text="Mostrar console (--console)",
        variable=console_var,
        value=0,
        bg="#f0f0f0",
    ).grid(row=1, column=2)

    execute_var = tk.BooleanVar()
    tk.Checkbutton(
        root, text="Executar comando após gerar", variable=execute_var, bg="#f0f0f0"
    ).pack(pady=10)

    tk.Button(root, text="Gerar Comando", command=generate_command).pack(pady=5)

    copy_button = tk.Button(root, text="Copiar Comando")
    copy_button.pack(pady=5)

    output_label = tk.Label(root, text="", wraplength=500, bg="#f0f0f0")
    output_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
