import tkinter as tk
from tkinter import ttk
import psycopg2
from tabulate import tabulate

# Variáveis globais para os Combobox e Entry
combo_parametro_perfil = None
combo_parametro_jogos = None
entry_filtro_perfil = None
entry_filtro_jogos = None
entry_filtro_amigos = None
entry_filtro_conquistas = None

# Função para executar a consulta no banco de dados e exibir o resultado na mesma janela
def consultar():
    # Obter os valores selecionados pelos usuários
    tabela = combo_tabela.get()

    if tabela == "Perfil + Jogos por perfil":
        parametros = [cb_parametro.cget("text") for cb_parametro in checkboxes_parametro_perfil if cb_parametro.var.get() == 1]
        filtro = int(entry_filtro_perfil.get())
    elif tabela == "Jogos + Jogos por perfil":
        parametro = combo_parametro_jogos.get()
        filtro = int(entry_filtro_jogos.get())
    elif tabela == "Perfil + Conquistas por perfil + Lista de amigos":
        filtro_amigos = int(entry_filtro_amigos.get())
        filtro_conquistas = int(entry_filtro_conquistas.get())

    # Conectar ao banco de dados
    conn = psycopg2.connect(
        host="localhost",
        database="steam",
        user="postgres",
        password="admin"
    )

    # Criar o cursor para executar as consultas
    cursor = conn.cursor()

    # Consultar a tabela de acordo com a escolha do usuário
    if tabela == "Perfil + Jogos por perfil":
        # Construir a consulta SQL para a tabela Perfil
        query = f"SELECT p.steamID, p.personaname, SUM(jpp.playtime_forever) AS total_playtime FROM api_steam.perfil p INNER JOIN api_steam.jogos_por_perfil jpp ON p.steamID = jpp.steamID WHERE p.loccountrycode IN {tuple(parametros)} AND jpp.playtime_forever >= {filtro} GROUP BY p.steamID, p.personaname;"
    elif tabela == "Jogos + Jogos por perfil":
        # Construir a consulta SQL para a tabela Jogos
        query = f"SELECT * FROM api_steam.jogos WHERE name LIKE '{parametro}%' AND appid IN (SELECT appid FROM api_steam.jogos_por_perfil GROUP BY appid HAVING COUNT(*) >= {filtro});"
    elif tabela == "Perfil + Conquistas por perfil + Lista de amigos":
        # Construir a consulta SQL para a tabela Amigos e conquistas
        query = f"""
        SELECT p.steamID, p.personaname, amigos.total_amigos, conquistas.total_conquistas
        FROM api_steam.perfil p
        LEFT JOIN (
            SELECT steamID, COUNT(friend_steamid) AS total_amigos
            FROM api_steam.lista_de_amigos
            GROUP BY steamID
            HAVING COUNT(friend_steamid) >= {filtro_amigos}
        ) amigos ON p.steamID = amigos.steamID
        LEFT JOIN (
            SELECT steamID, COUNT(apiname) AS total_conquistas
            FROM api_steam.conquista_por_perfil
            GROUP BY steamID
            HAVING COUNT(apiname) >= {filtro_conquistas}
        ) conquistas ON p.steamID = conquistas.steamID
        WHERE amigos.total_amigos IS NOT NULL AND conquistas.total_conquistas IS NOT NULL;
        """

    # Executar a consulta SQL
    cursor.execute(query)

    # Obter os resultados da consulta
    resultados = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Exibir os resultados na janela principal
    tabela_resultado = tabulate(resultados, headers=[desc[0] for desc in cursor.description], tablefmt="psql")
    texto_resultado.delete(1.0, tk.END)
    texto_resultado.insert(tk.END, tabela_resultado)


# Função para exibir os parâmetros e filtros de acordo com a tabela selecionada
def mostrar_parametros(event):
    tabela = combo_tabela.get()

    if tabela == "Perfil + Jogos por perfil":
        # Limpar os widgets existentes
        for widget in frame_parametros.winfo_children():
            widget.destroy()

        global checkboxes_parametro_perfil
        global entry_filtro_perfil

        # Label e Checkboxes para selecionar o país do perfil
        label_parametro = tk.Label(frame_parametros, text="Escolha o país do perfil:")
        label_parametro.pack(side=tk.LEFT)

        paises = ["RU", "CN", "US"]
        checkboxes_parametro_perfil = []
        for pais in paises:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(frame_parametros, text=pais, variable=var)
            checkbox.var = var  # Armazenar a variável como um atributo do widget
            checkbox.pack(side=tk.LEFT)
            checkboxes_parametro_perfil.append(checkbox)

        # Label e Entry para inserir a quantidade mínima de minutos jogados
        label_filtro = tk.Label(frame_parametros, text="Escolha o número mínimo de minutos jogados:")
        label_filtro.pack(side=tk.LEFT)

        entry_filtro_perfil = tk.Entry(frame_parametros)
        entry_filtro_perfil.pack(side=tk.LEFT)

    elif tabela == "Jogos + Jogos por perfil":
        # Limpar os widgets existentes
        for widget in frame_parametros.winfo_children():
            widget.destroy()

        global combo_parametro_jogos
        global entry_filtro_jogos

        # Label e Combobox para selecionar a letra inicial do jogo
        label_parametro = tk.Label(frame_parametros, text="Escolha a letra inicial do jogo:")
        label_parametro.pack(side=tk.LEFT)

        combo_parametro_jogos = ttk.Combobox(frame_parametros, values=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"])
        combo_parametro_jogos.pack(side=tk.LEFT)

        # Label e Entry para inserir a quantidade mínima de jogadores
        label_filtro = tk.Label(frame_parametros, text="Escolha o número mínimo de jogadores:")
        label_filtro.pack(side=tk.LEFT)

        entry_filtro_jogos = tk.Entry(frame_parametros)
        entry_filtro_jogos.pack(side=tk.LEFT)

    elif tabela == "Perfil + Conquistas por perfil + Lista de amigos":
        # Limpar os widgets existentes
        for widget in frame_parametros.winfo_children():
            widget.destroy()

        global entry_filtro_amigos
        global entry_filtro_conquistas

        # Label e Entry para inserir a quantidade mínima de amigos
        label_filtro_amigos = tk.Label(frame_parametros, text="Escolha a quantidade mínima de amigos:")
        label_filtro_amigos.pack(side=tk.LEFT)

        entry_filtro_amigos = tk.Entry(frame_parametros)
        entry_filtro_amigos.pack(side=tk.LEFT)

        # Label e Entry para inserir a quantidade mínima de conquistas
        label_filtro_conquistas = tk.Label(frame_parametros, text="Escolha a quantidade mínima de conquistas:")
        label_filtro_conquistas.pack(side=tk.LEFT)

        entry_filtro_conquistas = tk.Entry(frame_parametros)
        entry_filtro_conquistas.pack(side=tk.LEFT)


# Função para obter os países selecionados nos checkboxes
def obter_paises_selecionados():
    paises_selecionados = []
    for checkbox in checkboxes_parametro_perfil:
        if checkbox.var.get() == 1:
            paises_selecionados.append(checkbox['text'])
    return paises_selecionados


# Função para executar a consulta no banco de dados e exibir o resultado na mesma janela
def consultar():
    # Obter os valores selecionados pelos usuários
    tabela = combo_tabela.get()

    if tabela == "Perfil + Jogos por perfil":
        paises = obter_paises_selecionados()
        filtro = int(entry_filtro_perfil.get())
    elif tabela == "Jogos + Jogos por perfil":
        parametro = combo_parametro_jogos.get()
        filtro = int(entry_filtro_jogos.get())
    elif tabela == "Perfil + Conquistas por perfil + Lista de amigos":
        filtro_amigos = int(entry_filtro_amigos.get())
        filtro_conquistas = int(entry_filtro_conquistas.get())

    # Conectar ao banco de dados
    conn = psycopg2.connect(
        host="localhost",
        database="steam",
        user="postgres",
        password="admin"
    )

    # Criar o cursor para executar as consultas
    cursor = conn.cursor()

    # Consultar a tabela de acordo com a escolha do usuário
    if tabela == "Perfil + Jogos por perfil":
        # Construir a consulta SQL para a tabela Perfil
        paises_str = ", ".join([f"'{pais}'" for pais in paises])
        query = f"SELECT p.steamID, p.personaname, SUM(jpp.playtime_forever) AS total_playtime FROM api_steam.perfil p INNER JOIN api_steam.jogos_por_perfil jpp ON p.steamID = jpp.steamID WHERE p.loccountrycode IN ({paises_str}) AND jpp.playtime_forever >= {filtro} GROUP BY p.steamID, p.personaname;"
    elif tabela == "Jogos + Jogos por perfil":
        # Construir a consulta SQL para a tabela Jogos
        query = f"SELECT * FROM api_steam.jogos WHERE name LIKE '{parametro}%' AND appid IN (SELECT appid FROM api_steam.jogos_por_perfil GROUP BY appid HAVING COUNT(*) >= {filtro});"
    elif tabela == "Perfil + Conquistas por perfil + Lista de amigos":
        # Construir a consulta SQL para a tabela Amigos e conquistas
        query = f"""
        SELECT p.steamID, p.personaname, amigos.total_amigos, conquistas.total_conquistas
        FROM api_steam.perfil p
        LEFT JOIN (
            SELECT steamID, COUNT(friend_steamid) AS total_amigos
            FROM api_steam.lista_de_amigos
            GROUP BY steamID
            HAVING COUNT(friend_steamid) >= {filtro_amigos}
        ) amigos ON p.steamID = amigos.steamID
        LEFT JOIN (
            SELECT steamID, COUNT(apiname) AS total_conquistas
            FROM api_steam.conquista_por_perfil
            GROUP BY steamID
            HAVING COUNT(apiname) >= {filtro_conquistas}
        ) conquistas ON p.steamID = conquistas.steamID
        WHERE amigos.total_amigos IS NOT NULL AND conquistas.total_conquistas IS NOT NULL;
        """

    # Executar a consulta SQL
    cursor.execute(query)

    # Obter os resultados da consulta
    resultados = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Exibir os resultados na janela principal
    tabela_resultado = tabulate(resultados, headers=[desc[0] for desc in cursor.description], tablefmt="psql")
    texto_resultado.delete(1.0, tk.END)
    texto_resultado.insert(tk.END, tabela_resultado)


# Criação da janela principal
janela = tk.Tk()
janela.title("Consulta Steam")

# Adicionar espaçamento superior com um rótulo vazio
espacamento_superior = tk.Label(janela, text="")
espacamento_superior.pack()

# Combobox para selecionar a tabela
combo_tabela = ttk.Combobox(janela, values=["Perfil + Jogos por perfil", "Jogos + Jogos por perfil", "Perfil + Conquistas por perfil + Lista de amigos"], width=50)
combo_tabela.pack()

# Adicionar padding nas bordas da janela
janela.geometry("1000x600")

# Frame para exibir os parâmetros e filtros
frame_parametros = tk.Frame(janela)
frame_parametros.pack()

# Label e Entry para exibir o resultado
label_resultado = tk.Label(janela, text="Resultado:")
label_resultado.pack()

texto_resultado = tk.Text(janela, height=10, width=80)
texto_resultado.pack()

# Botão para executar a consulta
botao_consultar = tk.Button(janela, text="Consultar", command=consultar)
botao_consultar.pack()

# Evento para exibir os parâmetros e filtros de acordo com a tabela selecionada
combo_tabela.bind("<<ComboboxSelected>>", mostrar_parametros)

# Adicionar espaçamento inferior com um rótulo vazio
espacamento_inferior = tk.Label(janela, text="")
espacamento_inferior.pack()

janela.mainloop()
