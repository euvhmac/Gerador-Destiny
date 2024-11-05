# src/interface.py

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

# Imports do projeto
from dados import gerar_nome, gerar_login, gerar_cpf

# Função para obter o caminho absoluto para arquivos de recurso
def resource_path(relative_path):
    """ Retorna o caminho absoluto do arquivo, compatível com executáveis """
    try:
        base_path = sys._MEIPASS  # Caminho temporário do executável cx_Freeze ou PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Função para ajustar a opacidade da imagem
def ajustar_opacidade(imagem_path, opacidade):
    if not os.path.exists(imagem_path):
        print(f"Arquivo não encontrado: {imagem_path}")
        return None

    imagem = Image.open(imagem_path).convert("RGBA")
    alpha = imagem.split()[3]  # Obtém o canal alfa (transparência)
    
    # Ajusta a opacidade
    alpha = alpha.point(lambda p: p * opacidade)
    imagem.putalpha(alpha)
    
    return imagem

# Função para copiar texto usando o clipboard da janela principal
def copiar_para_clipboard(texto, divisoria):
    janela.clipboard_clear()
    janela.clipboard_append(texto)
    janela.update()  # Mantém os dados no clipboard
    
    # Inicia a animação da linha divisória
    animar_divisoria(divisoria)

# Função para animar a linha divisória (ficar verde e depois voltar ao normal)
def animar_divisoria(divisoria):
    divisoria.config(bg="#00FF00")
    janela.after(500, lambda: divisoria.config(bg="#555555"))

# Função para atualizar os dados na interface
def atualizar_dados():
    novo_nome = gerar_nome()
    novo_login = gerar_login(novo_nome)
    novo_cpf = gerar_cpf()

    # Debug para verificar dados gerados
    print(f"Debug - Novo Nome: {novo_nome}, Novo Login: {novo_login}, Novo CPF: {novo_cpf}")

    usuario_label.config(text=novo_login)
    nome_label.config(text=novo_nome)
    cpf_label.config(text=novo_cpf)

    # Atualiza os comandos dos botões de copiar com os novos dados
    copiar_usuario_btn['command'] = lambda: copiar_para_clipboard(novo_login, divisoria_usuario)
    copiar_nome_btn['command'] = lambda: copiar_para_clipboard(novo_nome, divisoria_nome)
    copiar_cpf_btn['command'] = lambda: copiar_para_clipboard(novo_cpf, divisoria_cpf)

# Função principal para criar a interface completa
def criar_interface():
    global janela, usuario_label, nome_label, cpf_label
    global copiar_usuario_btn, copiar_nome_btn, copiar_cpf_btn
    global divisoria_usuario, divisoria_nome, divisoria_cpf

    janela = tk.Tk()
    janela.title("Destiny Bot")
    janela.geometry("260x420")
    janela.configure(bg="#333333")
    janela.resizable(False, False)

    # src/interface.py (dentro da função criar_interface)
    icon_path = resource_path("assets/icone.ico")
    if os.path.exists(icon_path):
        janela.iconbitmap(icon_path)
    else:
        print("Ícone não encontrado.")


# Carregar a imagem de fundo com opacidade ajustada
imagem_path = resource_path("assets/background.jpg")
imagem_fundo = ajustar_opacidade(imagem_path, 0.1)  # Opacidade de 10%

if imagem_fundo is not None:
    imagem_fundo_tk = ImageTk.PhotoImage(imagem_fundo)
    background_label = tk.Label(janela, image=imagem_fundo_tk, bg="#333333")
    background_label.place(relwidth=1, relheight=1)
    background_label.lower()
else:
    print("Imagem de fundo não encontrada.")


    # Frame principal para sobrepor os elementos na imagem de fundo
    frame_principal = tk.Frame(janela, bg="#333333", padx=10, pady=10)
    frame_principal.place(relx=0.5, rely=0.5, anchor="center")

    # Estilo da interface usando ttk
    style = ttk.Style()
    style.configure("TLabel", background="#333333", foreground="#CCCCCC", font=("Helvetica", 10))
    style.configure("TButton", font=("Helvetica", 9, "bold"))

    # Configura os elementos de texto e botões da interface
    # USUÁRIO
    tk.Label(frame_principal, text="USUÁRIO", bg="#333333", fg="#CCCCCC", font=("Helvetica", 10, "bold")).pack(anchor="w")
    linha_frame_usuario = tk.Frame(frame_principal, bg="#333333")
    linha_frame_usuario.pack(fill="x", pady=5)

    usuario_label = tk.Label(linha_frame_usuario, text="", bg="#444444", fg="#FFFFFF", font=("Helvetica", 10))
    usuario_label.pack(side="left", expand=True, fill="x", padx=(0, 5))

    copiar_usuario_btn = tk.Button(linha_frame_usuario, text="Copiar", background="#555555", fg="#FFFFFF", relief="flat", cursor="hand2", font=("Helvetica", 9))
    copiar_usuario_btn.pack(side="right")
    
    divisoria_usuario = tk.Frame(frame_principal, bg="#555555", height=2)
    divisoria_usuario.pack(fill="x", pady=(5, 10))

    # NOME
    tk.Label(frame_principal, text="NOME", bg="#333333", fg="#CCCCCC", font=("Helvetica", 10, "bold")).pack(anchor="w")
    linha_frame_nome = tk.Frame(frame_principal, bg="#333333")
    linha_frame_nome.pack(fill="x", pady=5)

    nome_label = tk.Label(linha_frame_nome, text="", bg="#444444", fg="#FFFFFF", font=("Helvetica", 10))
    nome_label.pack(side="left", expand=True, fill="x", padx=(0, 5))

    copiar_nome_btn = tk.Button(linha_frame_nome, text="Copiar", background="#555555", fg="#FFFFFF", relief="flat", cursor="hand2", font=("Helvetica", 9))
    copiar_nome_btn.pack(side="right")
    
    divisoria_nome = tk.Frame(frame_principal, bg="#555555", height=2)
    divisoria_nome.pack(fill="x", pady=(5, 10))

    # CPF
    tk.Label(frame_principal, text="CPF", bg="#333333", fg="#CCCCCC", font=("Helvetica", 10, "bold")).pack(anchor="w")
    linha_frame_cpf = tk.Frame(frame_principal, bg="#333333")
    linha_frame_cpf.pack(fill="x", pady=5)

    cpf_label = tk.Label(linha_frame_cpf, text="", bg="#444444", fg="#FFFFFF", font=("Helvetica", 10))
    cpf_label.pack(side="left", expand=True, fill="x", padx=(0, 5))

    copiar_cpf_btn = tk.Button(linha_frame_cpf, text="Copiar", background="#555555", fg="#FFFFFF", relief="flat", cursor="hand2", font=("Helvetica", 9))
    copiar_cpf_btn.pack(side="right")
    
    divisoria_cpf = tk.Frame(frame_principal, bg="#555555", height=2)
    divisoria_cpf.pack(fill="x", pady=(5, 10))

    # Botão para gerar novos dados
    gerar_btn = tk.Button(frame_principal, text="Gerar", command=atualizar_dados, background="#555555", fg="#FFFFFF", relief="flat", cursor="hand2", font=("Helvetica", 10, "bold"))
    gerar_btn.pack(pady=10)

    # Checkbox para manter sempre no topo
    manter_topo_var = tk.BooleanVar()
    topo_check = tk.Checkbutton(frame_principal, text="Manter sempre no topo", variable=manter_topo_var, 
                                command=lambda: janela.attributes('-topmost', manter_topo_var.get()),
                                bg="#333333", fg="#FFFFFF", selectcolor="#555555", font=("Helvetica", 9))
    topo_check.pack(pady=(5, 0))

    janela.mainloop()
