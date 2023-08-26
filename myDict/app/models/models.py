from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean,create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    meaning = Column(String, nullable=False)
    
    thesaurus = relationship('Thesaurus', back_populates='word')

class Thesaurus(Base):
    __tablename__ = 'thesaurus'
    id = Column(Integer, primary_key=True)
    synonym = Column(String, nullable=False)
    antonym = Column(String, nullable=False)
    word_id = Column(Integer, ForeignKey('words.id'), nullable=False)
    
    word = relationship('Word', back_populates='thesaurus')

class WordOfTheDay(Base):
    __tablename__ = 'word_of_the_day'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    meaning = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
