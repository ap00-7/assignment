from sqlalchemy import Column, Integer, String, Text, Date, Time, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class HCPInteraction(Base):
    __tablename__ = 'hcp_interactions'

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(200), nullable=False)
    interaction_type = Column(String(100), nullable=False)
    date = Column(String(50), nullable=False)
    time = Column(String(50), nullable=False)
    attendees = Column(String(500), nullable=True)
    topics = Column(Text, nullable=True)
    sentiment = Column(String(20), nullable=True)
    outcomes = Column(Text, nullable=True)
    follow_up = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    materials = relationship('Material', back_populates='interaction', cascade='all, delete-orphan')
    samples = relationship('Sample', back_populates='interaction', cascade='all, delete-orphan')

class Material(Base):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey('hcp_interactions.id', ondelete='CASCADE'))
    name = Column(String(300), nullable=False)
    interaction = relationship('HCPInteraction', back_populates='materials')

class Sample(Base):
    __tablename__ = 'samples'
    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey('hcp_interactions.id', ondelete='CASCADE'))
    name = Column(String(300), nullable=False)
    quantity = Column(String(100), nullable=True)
    interaction = relationship('HCPInteraction', back_populates='samples')
