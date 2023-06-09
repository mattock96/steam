from sqlalchemy import Column, DateTime, Integer, BigInteger, String, Text, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Perfil(Base):
    __tablename__ = 'perfil'
    __table_args__ = {'schema': 'api_steam'}

    steamID = Column(BigInteger, primary_key=True)
    personaname = Column(String(255))
    profileurl = Column(Text)
    avatar = Column(Text)
    personastate = Column(Integer)
    communityvisibilitystate = Column(Integer)
    profilestate = Column(Integer)
    lastlogoff = Column(TIMESTAMP)
    realname = Column(String(255))
    primaryclanid = Column(BigInteger)
    game_count = Column(Integer)


class JogoDoJogador(Base):
    __tablename__ = 'jogodojogador'
    __table_args__ = {'schema': 'api_steam'}

    steamID = Column(BigInteger, ForeignKey('api_steam.perfil.steamID'), primary_key=True)
    appid = Column(Integer, primary_key=True)
    playtime_2weeks = Column(Integer)
    playtime_forever = Column(Integer)
    perfil_jogador = relationship('Perfil')


class Jogos(Base):
    __tablename__ = 'jogos'
    __table_args__ = {'schema': 'api_steam'}

    appid = Column(Integer, primary_key=True)
    name = Column(String(200))


class Conquista_por_player(Base):
    __tablename__ = 'conquista_por_player'
    __table_args__ = {'schema': 'api_steam'}

    steamID = Column(BigInteger, ForeignKey('api_steam.perfil.steamID'), primary_key=True)
    appid = Column(Integer, primary_key=True)
    apiname = Column(String(100), primary_key=True)
    achieved = Column(Integer)
    unlocktime = Column(BigInteger)
    perfil_jogador = relationship('Perfil')
    jogo_jogador = relationship('Jogos')


class Conquista(Base):
    __tablename__ = 'conquista'
    __table_args__ = {'schema': 'api_steam'}

    apiname = Column(String(100), primary_key=True)
    appid = Column(Integer, ForeignKey('api_steam.jogos.appid'))
    name = Column(String(255))
    descricao = Column(String(255))
    conquista_jogo = relationship('Jogos')


class ListaDeAmigos(Base):
    __tablename__ = 'lista_de_amigos'
    __table_args__ = {'schema':'api_steam'}

    steamID = Column(BigInteger, ForeignKey('api_steam.perfil.steamID'), primary_key=True)
    friend_steamID = Column(BigInteger, ForeignKey('api_steam.perfil.steamID'), primary_key=True)
    relationship = Column(Enum('all', 'friend', name='relationship'), nullable=False)
    friend_since = Column(DateTime)

    perfil = relationship('Perfil', foreign_keys=[steamID])
    amigo = relationship('Perfil', foreign_keys=[friend_steamID])
