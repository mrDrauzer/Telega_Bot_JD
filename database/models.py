from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class NewsItem(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    source = Column(String)
    published_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<NewsItem(title='{self.title}', source='{self.source}')>"