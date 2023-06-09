from sqlalchemy.orm import sessionmaker
from models import Perfil, JogoDoJogador, Jogos, Conquista_por_player, Conquista, ListaDeAmigos

def converter_json_para_perfil(json_data):
    steamID = json_data['steamID']
    personaname = json_data['personaname']
    profileurl = json_data['profileurl']
    avatar = json_data['avatar']
    personastate = json_data['personastate']
    communityvisibilitystate = json_data['communityvisibilitystate']
    profilestate = json_data['profilestate']
    lastlogoff = json_data['lastlogoff']
    realname = json_data.get('realname', '')
    primaryclanid = json_data['primaryclanid']
    game_count = json_data.get('game_count', 0)

    return Perfil(
        steamID=steamID,
        personaname=personaname,
        profileurl=profileurl,
        avatar=avatar,
        personastate=personastate,
        communityvisibilitystate=communityvisibilitystate,
        profilestate=profilestate,
        lastlogoff=lastlogoff,
        realname=realname,
        primaryclanid=primaryclanid,
        game_count=game_count
    )

def converter_json_para_jogo_do_jogador(json_data):
    steamID = json_data['steamID']
    appid = json_data['appid']
    playtime_2weeks = json_data['playtime_2weeks']
    playtime_forever = json_data['playtime_forever']

    return JogoDoJogador(
        steamID=steamID,
        appid=appid,
        playtime_2weeks=playtime_2weeks,
        playtime_forever=playtime_forever
    )

def converter_json_para_jogos(json_data):
    appid = json_data['appid']
    name = json_data['name']

    return Jogos(
        appid=appid,
        name=name
    )

def converter_json_para_conquista_por_player(json_data):
    steamID = json_data['steamID']
    appid = json_data['appid']
    apiname = json_data['apiname']
    achieved = json_data['achieved']
    unlocktime = json_data['unlocktime']

    return Conquista_por_player(
        steamID=steamID,
        appid=appid,
        apiname=apiname,
        achieved=achieved,
        unlocktime=unlocktime
    )

def converter_json_para_conquista(json_data):
    apiname = json_data['apiname']
    appid = json_data['appid']
    name = json_data['name']
    descricao = json_data['description']

    return Conquista(
        apiname=apiname,
        appid=appid,
        name=name,
        descricao=descricao
    )

def converter_json_para_lista_de_amigos(json_data):
    steamID = json_data['steamID']
    friend_steamID = json_data['friend_steamID']
    relationship = json_data['relationship']
    friend_since = json_data['friend_since']

    return ListaDeAmigos(
        steamID=steamID,
        friend_steamID=friend_steamID,
        relationship=relationship,
        friend_since=friend_since
    )

def inserir_dados_na_tabela(session, dados):
    session.bulk_save_objects(dados)
    session.commit()
