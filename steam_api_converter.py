from sqlalchemy.orm import sessionmaker
from config import Session
from models import Perfil, Jogos_por_perfil, Jogos, Conquista_por_perfil, Conquista, Lista_de_amigos
from datetime import datetime

def converter_json_para_perfil(json_data, session):
    steamID = json_data['steamid']
    personaname = json_data['personaname']
    profileurl = json_data['profileurl']
    avatar = json_data['avatar']
    personastate = json_data['personastate']
    communityvisibilitystate = json_data['communityvisibilitystate']
    if json_data.get('profilestate') is not None:
        profilestate = json_data['profilestate']
    else:
        profilestate = 0

    if json_data.get('lastlogoff') is not None:
        lastlogoff = datetime.fromtimestamp(json_data['lastlogoff'])
    else:
        lastlogoff = None

    if json_data.get('realname') is not None:
        realname = json_data['realname']
    else:
        realname = None

    if json_data.get('primaryclanid') is not None:
        primaryclanid = json_data['primaryclanid']
    else:
        primaryclanid = 0
    
    if json_data.get('locstatecode') is not None:
        locstatecodeA = json_data['locstatecode'][:2]  # Truncate to 2 characters
    else:
        locstatecodeA = None
    
    if json_data.get('loccountrycode') is not None:
        loccountrycodeA = json_data['loccountrycode']
    else:
        loccountrycodeA = None
    
    if json_data.get('timecreated') is not None:
        timecreatedA = datetime.fromtimestamp(json_data['timecreated'])
    else:
        timecreatedA = None


    novo_perfil= Perfil(
        steamid =steamID,
        personaname=personaname,
        profileurl=profileurl,
        avatar=avatar,
        personastate=personastate,
        communityvisibilitystate=communityvisibilitystate,
        profilestate=profilestate,
        lastlogoff=lastlogoff,
        realname=realname,
        primaryclanid=primaryclanid,
        locstatecode = locstatecodeA,
        loccountrycode = loccountrycodeA,
        timecreated = timecreatedA
    )
    session.add(novo_perfil)
    return novo_perfil

def converter_json_para_lista_de_amigos(json_data, steamID, session):
    steamIDA = steamID
    friend_steamIDA = json_data['steamid']
    relationshipA = json_data['relationship']
    friend_sinceA = datetime.fromtimestamp(json_data['friend_since'])

    novo_amigo= Lista_de_amigos(
        steamid=steamIDA,
        friend_steamid = friend_steamIDA,
        relacao = relationshipA,
        friend_since = friend_sinceA    
    )
    session.add(novo_amigo)
    return novo_amigo
    

def converter_json_para_jogo_do_jogador(json_data,steamid, session):
    steamID = steamid
    appidA = json_data['appid']

    # verificar se esse valor está presente no jason 
    if json_data.get('playtime_2weeks') is not None:
        playtime_2weeks = json_data['playtime_2weeks']
    else:
        playtime_2weeks = 0  

    playtime_forever = json_data['playtime_forever']

    jogo_existente = session.query(Jogos).filter_by(appid=appidA).first()
    
    #Se o jogo existe, é possivel adicionalo na tabela
    if jogo_existente:
        novo_jogoDoJogaodor= Jogos_por_perfil(
            steamid=steamID,
            appid=appidA,
            playtime_2weeks=playtime_2weeks,
            playtime_forever=playtime_forever
        )
        session.add(novo_jogoDoJogaodor)
        return novo_jogoDoJogaodor
    else:
        return

def converter_json_para_jogos(json_data, session):
    appidA = json_data['appid']
    nameA = json_data['name']

    jogo_existente = session.query(Jogos).filter_by(appid=appidA).first()

    if jogo_existente:
        # Atualiza os dados do registro existente
        jogo_existente.name = nameA
        jogo_atualizado = session.merge(jogo_existente)
        return jogo_atualizado
    else:
        # Cria um novo registro
        jogo = Jogos(appid=appidA, name=nameA)
        session.add(jogo)
        return Jogos(
            appid=appidA,
            name=nameA
        )
    

def converter_json_para_conquista_por_player(json_data,steamid,app, session):
    steamID = steamid
    appidA = app
    apinameA = json_data['apiname']
    achievedA = json_data['achieved']
    unlocktimeA = datetime.fromtimestamp(json_data['unlocktime'])
    
    #filtrar se o jogo existe primeiramentes
    jogo_existente = session.query(Jogos).filter_by(appid=appidA).first()

    #se o o jogo existe, é possivel adicionar suas conquistas
    if jogo_existente:
        nova_conquista = Conquista_por_perfil(
        steamid=steamID,
        appid=appidA,
        apiname=apinameA,
        achieved=achievedA,
        unlocktime=unlocktimeA
        )
        session.add(nova_conquista)
        return nova_conquista
    else:
        return

def converter_json_para_conquista(json_data, appid, session):
    
    appidA = appid
    apinameA = json_data['apiname']

    #filtrar as conquistas existentes 
    conquista_existente = session.query(Conquista).filter_by(apiname=apinameA).first()

    if conquista_existente:
        return
    else:
        conquistaNova = Conquista(
        apiname=apinameA,
        appid=appidA,
        )
        session.add(conquistaNova)
        return conquistaNova

def inserir_dados_na_tabela(session):
    #session.bulk_save_objects(dados)
    session.commit()
