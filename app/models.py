from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class WardrobeItem(Base):
    __tablename__ = "wardrobe"  # ← ДВЕ подчеркивания ДО и ПОСЛЕ tablename!
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    color = Column(String)
    image_path = Column(String, nullable=True)  # ← добавила nullable=True на всякий случай

class FavoriteOutfit(Base):
    __tablename__ = "favorite_outfits"  # ← ДВЕ подчеркивания!
    
    id = Column(Integer, primary_key=True, index=True)
    outfit_data = Column(Text)
    rating = Column(Integer)
    occasion = Column(String)