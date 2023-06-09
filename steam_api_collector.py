import requests
from config import STEAM_API_KEY
from steam_api_converter import converter_json_para_conquista, converter_json_para_conquista_por_player, converter_json_para_jogo_do_jogador, converter_json_para_jogos, converter_json_para_lista_de_amigos, converter_json_para_perfil, inserir_dados_na_tabela
import tkinter as tk
from config import engine
from sqlalchemy.orm import sessionmaker
from steam_api_collector import coletar_dados_api_steam

def coletar_dados_e_inserir():
    # Implemente aqui a lógica para coletar os dados via APIs e inserir no banco de dados
    print("Coletando dados via APIs e inserindo no banco de dados...")

    steamID = '123456789'  # Insira o SteamID desejado

    # Coleta dados via API para a tabela Perfil
    url_player_summaries = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steamID}'
    response_player_summaries = requests.get(url_player_summaries)
    data_player_summaries = response_player_summaries.json()['response']['players'][0]
    perfil = converter_json_para_perfil(data_player_summaries)

    # Coleta dados via API para a tabela Jogos
    url_app_list = f'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
    response_app_list = requests.get(url_app_list)
    data_app_list = response_app_list.json()['applist']['apps']
    jogos = [converter_json_para_jogos(jogo) for jogo in data_app_list]

    # Coleta dados via API para a tabela JogoDoJogador
    url_owned_games = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steamID}'
    response_owned_games = requests.get(url_owned_games)
    data_owned_games = response_owned_games.json()['response']
    jogos_do_jogador = [converter_json_para_jogo_do_jogador(jogo) for jogo in data_owned_games['games']]

    # Coleta dados via API para a tabela Conquista_por_player
    url_player_achievements = f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?key={STEAM_API_KEY}&steamid={steamID}'
    response_player_achievements = requests.get(url_player_achievements)
    data_player_achievements = response_player_achievements.json()['playerstats']['achievements']
    conquistas_do_jogador = [converter_json_para_conquista_por_player(conquista) for conquista in data_player_achievements]

    # Insere os dados no banco de dados
    Session = sessionmaker(bind=engine)
    session = Session()
    inserir_dados_na_tabela(session, [perfil] + jogos + jogos_do_jogador + conquistas_do_jogador)
    session.close()


def coletar_dados_api_steam(steamID):
    url_player_summaries = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steamID}'
    url_owned_games = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steamID}'
    url_friend_list = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={STEAM_API_KEY}&steamid={steamID}'
    url_player_achievements = f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?key={STEAM_API_KEY}&steamid={steamID}'

    response_player_summaries = requests.get(url_player_summaries)
    response_owned_games = requests.get(url_owned_games)
    response_friend_list = requests.get(url_friend_list)
    response_player_achievements = requests.get(url_player_achievements)

    data_player_summaries = response_player_summaries.json()['response']['players'][0]
    data_owned_games = response_owned_games.json()['response']
    data_friend_list = response_friend_list.json()['friendslist']['friends']
    data_player_achievements = response_player_achievements.json()['playerstats']['achievements']
    
    url_app_list = f'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
    response_app_list = requests.get(url_app_list)
    data_app_list = response_app_list.json()['applist']['apps']

    perfil = converter_json_para_perfil(data_player_summaries)
    jogos = [converter_json_para_jogos(jogo) for jogo in data_app_list]
    jogos_do_jogador = [converter_json_para_jogo_do_jogador(jogo) for jogo in data_owned_games['games']]
    amigos = [converter_json_para_lista_de_amigos(amigo) for amigo in data_friend_list]
    conquistas = [converter_json_para_conquista(conquista) for conquista in data_player_achievements]
    conquistas_do_jogador = [converter_json_para_conquista_por_player(conquista) for conquista in data_player_achievements]

    dados = [perfil] + jogos + jogos_do_jogador + amigos + conquistas + conquistas_do_jogador

    inserir_dados_na_tabela(requests.session, dados)
    
    return data_player_summaries, data_owned_games, data_friend_list, data_player_achievements

def atualizar_dados():
    steamID = '123456789'  # Insira o SteamID desejado
    session = Session()
    coletar_dados_api_steam(steamID, session)
    session.close()
    print('Dados atualizados com sucesso!')

root = tk.Tk()

# Adicione o primeiro botão para atualizar dados
button_atualizar = tk.Button(root, text="Atualizar Dados", command=atualizar_dados)
button_atualizar.pack()

# Adicione o segundo botão para iniciar a carga no banco via APIs
button_carga = tk.Button(root, text="Iniciar Carga", command=coletar_dados_e_inserir)
button_carga.pack()

root.mainloop()