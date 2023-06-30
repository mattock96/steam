from sqlalchemy import Column, DateTime, Integer, BigInteger, String, Text, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata

class RelationshipEnum(Enum):
    all = 'all'
    friend = 'friend'

class Perfil(Base):
    __tablename__ = 'perfil'
    __table_args__ = {'schema': 'api_steam'}

    steamid = Column(BigInteger, primary_key=True)
    personaname = Column(String(500))
    profileurl = Column(Text)
    avatar = Column(Text)
    personastate = Column(Integer)
    communityvisibilitystate = Column(Integer)
    profilestate = Column(Integer)
    lastlogoff = Column(TIMESTAMP, nullable=True)
    realname = Column(String(500), nullable=True)
    primaryclanid = Column(BigInteger)
    game_count = Column(Integer)
    locstatecode = Column(String(2), nullable=True)
    loccountrycode = Column(String(2), nullable=True)
    timecreated = Column(TIMESTAMP, nullable=True)

class Jogos_por_perfil(Base):
    __tablename__ = 'jogos_por_perfil'
    __table_args__ = {'schema': 'api_steam'}

    steamid = Column(BigInteger, ForeignKey('api_steam.perfil.steamid'), primary_key=True)
    appid = Column(Integer, primary_key=True)
    playtime_2weeks = Column(Integer)
    playtime_forever = Column(Integer)
    perfil_jogador = relationship('Perfil',foreign_keys=[steamid])


class Jogos(Base):
    __tablename__ = 'jogos'
    __table_args__ = {'schema': 'api_steam'}

    appid = Column(Integer, primary_key=True)
    name = Column(String(200))

    

class Conquista(Base):
    __tablename__ = 'conquista'
    __table_args__ = {'schema': 'api_steam'}

    apiname = Column(String(500), primary_key=True)
    appid = Column(Integer, ForeignKey('api_steam.jogos.appid'))
    jogo_conquista = relationship('Jogos',foreign_keys=[appid])


class Conquista_por_perfil(Base):
    __tablename__ = 'conquista_por_perfil'
    __table_args__ = {'schema': 'api_steam'}

    steamid = Column(BigInteger,ForeignKey('api_steam.perfil.steamid'), primary_key=True)
    appid = Column(Integer,ForeignKey('api_steam.jogos.appid'), primary_key=True)
    apiname = Column(String(500),ForeignKey('api_steam.conquista.apiname'), primary_key=True)
    achieved = Column(Integer)
    unlocktime = Column(TIMESTAMP, nullable=True)
    perfil_jogador = relationship('Perfil',foreign_keys=[steamid])
    jogo_jogador = relationship('Jogos',foreign_keys=[appid])
    conquista_jogo = relationship('Conquista',foreign_keys=[apiname])

class Lista_de_amigos(Base):
    __tablename__ = 'lista_de_amigos'
    __table_args__ = {'schema': 'api_steam'}

    steamid = Column(BigInteger, primary_key=True)
    friend_steamid = Column(BigInteger, primary_key=True)
    relacao = Column(Enum('all', 'friend', name='relationship'), nullable=False)
    friend_since = Column(TIMESTAMP, nullable=False)

    # Relacionamento com a tabela 'Perfil'
    perfil_jogador = relationship('Perfil', foreign_keys=[steamid], primaryjoin='Lista_de_amigos.steamid == Perfil.steamid')
    friend_perfil = relationship('Perfil', foreign_keys=[friend_steamid], primaryjoin='Lista_de_amigos.friend_steamid == Perfil.steamid')
    


