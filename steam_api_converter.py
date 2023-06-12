from sqlalchemy.orm import sessionmaker
from config import Session
from models import Perfil, JogoDoJogador, Jogos, Conquista_por_player, Conquista
from datetime import datetime

def converter_json_para_perfil(json_data):
    steamID = json_data['steamid']
    personaname = json_data['personaname']
    profileurl = json_data['profileurl']
    avatar = json_data['avatar']
    personastate = json_data['personastate']
    communityvisibilitystate = json_data['communityvisibilitystate']
    profilestate = json_data['profilestate']

    if json_data.get('lastlogoff') is not None:
        lastlogoff = datetime.fromtimestamp(json_data['lastlogoff'])
    else:
        lastlogoff = datetime.utcnow()

    if json_data.get('realname') is not None:
         realname = json_data['realname']
    else:
         realname = ''

    primaryclanid = json_data['primaryclanid']

    return Perfil(
        steamid =steamID,
        personaname=personaname,
        profileurl=profileurl,
        avatar=avatar,
        personastate=personastate,
        communityvisibilitystate=communityvisibilitystate,
        profilestate=profilestate,
        lastlogoff=lastlogoff,
        realname=realname,
        primaryclanid=primaryclanid
    )

def converter_json_para_jogo_do_jogador(json_data,steamid):
    steamID = steamid
    appid = json_data['appid']

    # verificar se esse valor está presente no jason 
    if 'playtime_2weeks' in json_data:
        playtime_2weeks = json_data['playtime_2weeks']
    else:
        playtime_2weeks = 0  

    playtime_forever = json_data['playtime_forever']

    return JogoDoJogador(
        steamid=steamID,
        appid=appid,
        playtime_2weeks=playtime_2weeks,
        playtime_forever=playtime_forever
    )

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
    

def converter_json_para_conquista_por_player(json_data,steamid,app):
    steamID = steamid
    appidA = app
    apinameA = json_data['apiname']
    achievedA = json_data['achieved']
    unlocktimeA = json_data['unlocktime']

    return Conquista_por_player(
        steamid=steamID,
        appid=appidA,
        apiname=apinameA,
        achieved=achievedA,
        unlocktime=unlocktimeA
    )

def converter_json_para_conquista(json_data, appid):
    
    appidA = appid
    apiname = json_data['apiname']

    # verificar se esse valor está presente no json, pois o atributo é opcional  
    if json_data.get('name') is not None:
        name = json_data['name']
    else:
        name = ''  
    
    # verificar se esse valor está presente no json, pois o atributo é opcional  
    if json_data.get('description') is not None:
        descricao = json_data['description']
    else:
        descricao = ''  

    return Conquista(
        apiname=apiname,
        appid=appidA,
        name=name,
        descricao=descricao
    )



def inserir_dados_na_tabela(session, dados):
    session.bulk_save_objects(dados)
    session.commit()
