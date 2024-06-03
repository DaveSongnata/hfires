import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess

def verificar(dbpath):
    if dbpath:
        command = f'gfix -v -full -user SYSDBA -password masterkey "{dbpath}"'
        execute_command(command)
    else:
        messagebox.showwarning("Atenção", "Por favor, selecione o caminho do banco de dados.")

def reparar(dbpath):
    if dbpath:
        command = f'gfix -mend -user SYSDBA -password masterkey "{dbpath}"'
        execute_command(command)
    else:
        messagebox.showwarning("Atenção", "Por favor, selecione o caminho do banco de dados.")

def backup(dbpath, backupdir):
    if dbpath and backupdir:
        command = f'gfix -mode read_only -user SYSDBA -password masterkey "{dbpath}" && gbak -b -v -ignore -user SYSDBA -password masterkey "{dbpath}" "{backupdir}/backup.fbk"'
        execute_command(command)
    else:
        messagebox.showwarning("Atenção", "Por favor, selecione o caminho do banco de dados e o diretório de backup.")

def restaurar(backupdir, dbpath):
    if dbpath and backupdir:
        command = f'gbak -c -v -user SYSDBA -password masterkey "{backupdir}/backup.fbk" "{dbpath}_restored.FDB" && gfix -mode read_write -user SYSDBA -password masterkey "{dbpath}_restored.FDB"'
        execute_command(command)
    else:
        messagebox.showwarning("Atenção", "Por favor, selecione o caminho do banco de dados e o diretório de backup.")

def execute_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        messagebox.showinfo("Sucesso", "Operação concluída com sucesso!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar o comando:\n{e}")

def selecionar_arquivo(entry):
    filepath = filedialog.askopenfilename(filetypes=[("Firebird DB Files", "*.FDB")])
    entry.delete(0, ctk.END)
    entry.insert(0, filepath)

def selecionar_diretorio(entry):
    directory = filedialog.askdirectory()
    entry.delete(0, ctk.END)
    entry.insert(0, directory)

# Configuração da aparência do customtkinter
ctk.set_appearance_mode("dark")  # Outros modos: "light", "system"
ctk.set_default_color_theme("blue")  # Outros temas: "dark-blue", "green"

# Criação da janela principal
root = ctk.CTk()
root.title("HELLAFIRE")

frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label_title = ctk.CTkLabel(frame, text="HELLAFIRE", font=ctk.CTkFont(size=24, weight="bold"))
label_title.pack(pady=10)

dbpath_label = ctk.CTkLabel(frame, text="Caminho do Banco de Dados (.FDB):")
dbpath_label.pack(pady=5)
dbpath_entry = ctk.CTkEntry(frame, width=400)
dbpath_entry.pack(pady=5)
dbpath_button = ctk.CTkButton(frame, text="Selecionar", command=lambda: selecionar_arquivo(dbpath_entry))
dbpath_button.pack(pady=5)

backupdir_label = ctk.CTkLabel(frame, text="Diretório de Backup:")
backupdir_label.pack(pady=5)
backupdir_entry = ctk.CTkEntry(frame, width=400)
backupdir_entry.pack(pady=5)
backupdir_button = ctk.CTkButton(frame, text="Selecionar", command=lambda: selecionar_diretorio(backupdir_entry))
backupdir_button.pack(pady=5)

button_frame = ctk.CTkFrame(frame)
button_frame.pack(pady=20)

verificar_button = ctk.CTkButton(button_frame, text="Verificar", command=lambda: verificar(dbpath_entry.get()))
verificar_button.pack(side="left", padx=10)

reparar_button = ctk.CTkButton(button_frame, text="Reparar", command=lambda: reparar(dbpath_entry.get()))
reparar_button.pack(side="left", padx=10)

backup_button = ctk.CTkButton(button_frame, text="Backup", command=lambda: backup(dbpath_entry.get(), backupdir_entry.get()))
backup_button.pack(side="left", padx=10)

restaurar_button = ctk.CTkButton(button_frame, text="Restaurar", command=lambda: restaurar(backupdir_entry.get(), dbpath_entry.get()))
restaurar_button.pack(side="left", padx=10)

root.mainloop()
