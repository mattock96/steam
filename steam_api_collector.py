import requests
from config import STEAM_API_KEY, Session
from steam_api_converter import converter_json_para_conquista, converter_json_para_conquista_por_player, converter_json_para_jogo_do_jogador, converter_json_para_jogos, converter_json_para_perfil, converter_json_para_lista_de_amigos, inserir_dados_na_tabela
import tkinter as tk
from tools import run_check_steam_profiles
from config import engine
from sqlalchemy.orm import sessionmaker


def coletar_dados_e_inserir():
    print("Coletando dados via APIs e inserindo no banco de dados...")

    Session = sessionmaker(bind=engine)
    session = Session()

    # Coleta dados via API para a tabela Jogos
    #url_app_list = f'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
    #response_app_list = requests.get(url_app_list)
    #data_app_list = response_app_list.json()['applist']['apps']
    #jogos = [converter_json_para_jogos(jogo, session) for jogo in data_app_list]
    print('jogos coletados!')
    
    perfils=[]
    amigosG=[]
    #Chamada da função para gerar IDs steam publicos para uma melhor visualização do funcionamento da API e da aplicação
    steamIds = run_check_steam_profiles()

    # Coleta dados via API para a tabela Perfil
    for id in steamIds:
        url_player_summaries = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={id}'
        url_friend_list = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={STEAM_API_KEY}&steamid={id}&relationship=friend'
        response_player_summaries = requests.get(url_player_summaries)
        response_friend_list = requests.get(url_friend_list)
        data_player_summaries = response_player_summaries.json()['response']['players'][0]
        if 'friendslist' in response_friend_list.json() and 'friends' in response_friend_list.json()['friendslist']:
            data_friend_list = response_friend_list.json()['friendslist']['friends']
            amigos = [converter_json_para_lista_de_amigos(amigo, id, session) for amigo in data_friend_list]
            amigosG.extend(amigos)
        perfil = converter_json_para_perfil(data_player_summaries, session)
        perfils.append(perfil)

    print('Perfis coletados!')

    # Necessario adicionar os amigos como perfil no banco de dados assim como os perfis principais
    for amigo in amigosG:
        if amigo is not None: 
            url_player_summaries2 = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={amigo.friend_steamid}'
            response_player_summaries2 = requests.get(url_player_summaries2)
            data_player_summaries2 = response_player_summaries2.json()['response']['players'][0]
            perfil = converter_json_para_perfil(data_player_summaries2, session)
            perfils.append(perfil)
    
    print('Amigos coletados!')

    jogos_do_jogador=[]
    total_jogos_do_jogador= []

    # Coleta dados via API para a tabela JogoDoJogador
    for perfil in perfils:
        url_owned_games = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={perfil.steamid}'
        response_owned_games = requests.get(url_owned_games)
        #Verificar se o perfil possui jogos 
        if 'response' in response_owned_games.json() and 'games' in response_owned_games.json()['response']:
            data_owned_games = response_owned_games.json()['response']['games']
            jogos_do_jogador = [converter_json_para_jogo_do_jogador(jogo, perfil.steamid, session) for jogo in data_owned_games]
            total_jogos_do_jogador.extend(jogos_do_jogador)
    print('jogos dos perfis coletados!')

    conquistas=[]
    conquistas_do_jogador=[]
    total_conquistas=[]
    total_conquistas_do_jogador= []
   
    # Coleta dados via API para a tabela Conquista_por_player
    for jogo in total_jogos_do_jogador:
        #Existem valores nulos nesta lista devido à ausência de alguns jogos em nossa base de dados. Consequentemente, a conversão resultará em um valor nulo.
        #Necessário essa verificação
        if jogo is not None:
            url_player_achievements = f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?key={STEAM_API_KEY}&steamid={jogo.steamid}&appid={jogo.appid}'
            response_player_achievements = requests.get(url_player_achievements)
            # Verificar se o jogo possui achievements 
            if 'playerstats' in response_player_achievements.json() and 'achievements' in response_player_achievements.json()['playerstats']:
                data_player_achievements = response_player_achievements.json()['playerstats']['achievements']
                conquistas = [converter_json_para_conquista(conquista, jogo.appid, session) for conquista in data_player_achievements]
                conquistas_do_jogador = [converter_json_para_conquista_por_player(conquistad,jogo.steamid,jogo.appid, session) for conquistad in data_player_achievements]
                total_conquistas.extend(conquistas)
                total_conquistas_do_jogador.extend(conquistas_do_jogador)
            
    print('Conquistas coletados!')
    print('Conquistas dos perfis coletados!')
    
    # Insere os dados no banco de dadoss
    inserir_dados_na_tabela(session)
    print('Dados inseridos com sucesso!')
    session.close()

root = tk.Tk()

root.title("Steam_API")

root.geometry("200x100")  # Define o tamanho da janela para sua quantidade de pixels
root.configure(bg="#9499ac")

# Adicione o botão para iniciar a carga no banco via APIs
button_carga = tk.Button(root, text="Iniciar Carga", command=coletar_dados_e_inserir)
button_carga.pack(anchor="center")

root.mainloop()
