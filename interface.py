import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
import logging
from dados import gerar_nome, gerar_login, gerar_cpf_valido, gerar_numero_celular_completo

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para obter o caminho absoluto para arquivos de recurso
def resource_path(relative_path):
    """Retorna o caminho absoluto do arquivo, compatível com executáveis."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Função para ajustar a opacidade da imagem
def ajustar_opacidade(imagem_path, opacidade):
    """Ajusta a opacidade da imagem especificada."""
    if not os.path.exists(imagem_path):
        logging.warning(f"Arquivo não encontrado: {imagem_path}")
        return None

    imagem = Image.open(imagem_path).convert("RGBA")
    alpha = imagem.split()[3]
    alpha = alpha.point(lambda p: p * opacidade)
    imagem.putalpha(alpha)
    return imagem

# Função para copiar texto usando o clipboard da janela principal
def copiar_para_clipboard(texto, divisoria):
    """Copia o texto para o clipboard e anima a divisória."""
    janela.clipboard_clear()
    janela.clipboard_append(texto)
    janela.update()
    animar_divisoria(divisoria)

# Função para animar a linha divisória (ficar verde e depois voltar ao normal)
def animar_divisoria(divisoria):
    """Anima a divisória mudando de cor temporariamente."""
    divisoria.config(bg="#00FF00")
    janela.after(500, lambda: divisoria.config(bg="#555555"))

# Função para atualizar os dados na interface
def atualizar_dados():
    """Gera e exibe novos dados na interface."""
    genero_selecionado = genero_var.get()
    novo_nome = gerar_nome(genero_selecionado)
    novo_login = gerar_login(novo_nome)
    novo_cpf = gerar_cpf_valido()
    novo_celular_formatado, numero_para_copiar = gerar_numero_celular_completo()  # Gera ambos os formatos

    usuario_label.config(text=novo_login)
    nome_label.config(text=novo_nome)
    cpf_label.config(text=novo_cpf)
    celular_label.config(text=novo_celular_formatado)  # Exibe o número formatado

    copiar_usuario_btn['command'] = lambda: copiar_para_clipboard(novo_login, divisoria_usuario)
    copiar_nome_btn['command'] = lambda: copiar_para_clipboard(novo_nome, divisoria_nome)
    copiar_cpf_btn['command'] = lambda: copiar_para_clipboard(novo_cpf, divisoria_cpf)
    copiar_celular_btn['command'] = lambda: copiar_para_clipboard(numero_para_copiar, divisoria_celular)  # Copia sem formatação

# Função principal para criar a interface completa
def criar_interface():
    """Configura e inicia a interface gráfica principal."""
    global janela, usuario_label, nome_label, cpf_label, celular_label
    global copiar_usuario_btn, copiar_nome_btn, copiar_cpf_btn, copiar_celular_btn
    global divisoria_usuario, divisoria_nome, divisoria_cpf, divisoria_celular
    global genero_var

    janela = tk.Tk()
    janela.title("Gerador Destiny")
    janela.geometry("260x520")
    janela.configure(bg="#333333")
    janela.resizable(False, False)

    # Carrega o ícone da janela
    icon_path = resource_path("assets/icone.ico")
    if os.path.exists(icon_path):
        janela.iconbitmap(icon_path)
    else:
        logging.warning("Ícone não encontrado.")

    # Carregar a imagem de fundo com opacidade ajustada
    imagem_path = resource_path("assets/background.jpg")
    imagem_fundo = ajustar_opacidade(imagem_path, 0.1)

    if imagem_fundo is not None:
        imagem_fundo_tk = ImageTk.PhotoImage(imagem_fundo)
        background_label = tk.Label(janela, image=imagem_fundo_tk, bg="#333333")
        background_label.place(relwidth=1, relheight=1)
        background_label.lower()
    else:
        logging.warning("Imagem de fundo não encontrada.")

    # Frame principal para sobrepor os elementos na imagem de fundo
    frame_principal = tk.Frame(janela, bg="#333333", padx=10, pady=10)
    frame_principal.place(relx=0.5, rely=0.5, anchor="center")

    # Estilo da interface usando ttk
    style = ttk.Style()
    style.configure("TLabel", background="#333333", foreground="#CCCCCC", font=("Helvetica", 10))
    style.configure("TButton", font=("Helvetica", 9, "bold"))

    # Seleção de Gênero
    genero_var = tk.StringVar(value="N")
    tk.Label(frame_principal, text="SELEÇÃO DE GÊNERO", bg="#333333", fg="#CCCCCC", font=("Helvetica", 10, "bold")).pack(anchor="w")
    genero_frame = tk.Frame(frame_principal, bg="#333333")
    genero_frame.pack(fill="x", pady=5)

    tk.Radiobutton(genero_frame, text="M", variable=genero_var, value="M", bg="#333333", fg="#CCCCCC", selectcolor="#555555", font=("Helvetica", 9)).pack(side="left", padx=5)
    tk.Radiobutton(genero_frame, text="F", variable=genero_var, value="F", bg="#333333", fg="#CCCCCC", selectcolor="#555555", font=("Helvetica", 9)).pack(side="left", padx=5)
    tk.Radiobutton(genero_frame, text="N", variable=genero_var, value="N", bg="#333333", fg="#CCCCCC", selectcolor="#555555", font=("Helvetica", 9)).pack(side="left", padx=5)

    configurar_elementos_interface(frame_principal)

    janela.mainloop()

def configurar_elementos_interface(frame_principal):
    """Configura os elementos da interface."""
    # USUÁRIO
    tk.Label(frame_principal, text="USUÁRIO", bg="#333333", fg="#CCCCCC", font=("Helvetica", 10, "bold")).pack(anchor="w")
    linha_frame_usuario = tk.Frame(frame_principal, bg="#333333")
    linha_frame_usuario.pack(fill="x", pady=5)

    global usuario_label, copiar_usuario_btn, divisoria_usuario
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

    global nome_label, copiar_nome_btn, divisoria_nome
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

    global cpf_label, copiar_cpf_btn, divisoria_cpf
    cpf_label = tk.Label(linha_frame_cpf, text="", bg="#444444", fg="#FFFFFF", font=("Helvetica", 10))
    cpf_label.pack(side="left", expand=True, fill="x", padx=(0, 5))

    copiar_cpf_btn = tk.Button(linha_frame_cpf, text="Copiar", background="#555555", fg="#FFFFFF", relief="flat", cursor="hand2", font=("Helvetica", 9))
    copiar_cpf_btn.pack(side="right")
    
    divisoria_cpf = tk.Frame(frame_principal, bg="#555555", height=2)
    divisoria_cpf.pack(fill="x", pady=(5, 10))

    # CELULAR
    tk.Label(frame_principal, text="CELULAR", bg="#333333", fg="#CCCCCC", font=("Helvetica", 10, "bold")).pack(anchor="w")
    linha_frame_celular = tk.Frame(frame_principal, bg="#333333")
    linha_frame_celular.pack(fill="x", pady=5)

    global celular_label, copiar_celular_btn, divisoria_celular
    celular_label = tk.Label(linha_frame_celular, text="", bg="#444444", fg="#FFFFFF", font=("Helvetica", 10))
    celular_label.pack(side="left", expand=True, fill="x", padx=(0, 5))

    copiar_celular_btn = tk.Button(linha_frame_celular, text="Copiar", background="#555555", fg="#FFFFFF", relief="flat", cursor="hand2", font=("Helvetica", 9))
    copiar_celular_btn.pack(side="right")

    divisoria_celular = tk.Frame(frame_principal, bg="#555555", height=2)
    divisoria_celular.pack(fill="x", pady=(5, 10))

    # Botão para gerar novos dados
    gerar_btn = tk.Button(frame_principal, text="Gerar", command=atualizar_dados, background="#555555", fg="#FFFFFF", relief="flat", cursor="hand2", font=("Helvetica", 10, "bold"))
    gerar_btn.pack(pady=10)

    # Checkbox para manter sempre no topo
    manter_topo_var = tk.BooleanVar()
    topo_check = tk.Checkbutton(frame_principal, text="Manter sempre no topo", variable=manter_topo_var, 
                                command=lambda: janela.attributes('-topmost', manter_topo_var.get()),
                                bg="#333333", fg="#FFFFFF", selectcolor="#555555", font=("Helvetica", 9))
    topo_check.pack(pady=(5, 0))

# Chamada principal
if __name__ == "__main__":
    criar_interface()
