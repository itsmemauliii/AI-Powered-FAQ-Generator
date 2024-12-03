from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Business(Base):
    __tablename__ = 'businesses'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    industry = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    faqs = relationship('FAQ', back_populates='business')

    def __repr__(self):
        return f"<Business(name={self.name}, industry={self.industry})>"

class FAQ(Base):
    __tablename__ = 'faqs'

    id = Column(Integer, primary_key=True)
    question = Column(String(255), nullable=False)
    answer = Column(Text, nullable=False)
    topic = Column(String(255), nullable=False)
    business_id = Column(Integer, ForeignKey('businesses.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    business = relationship('Business', back_populates='faqs')

    def __repr__(self):
        return f"<FAQ(question={self.question}, topic={self.topic})>"

# Create the database tables
def create_tables(engine):
    Base.metadata.create_all(engine)
