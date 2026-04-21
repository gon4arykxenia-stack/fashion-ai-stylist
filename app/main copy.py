from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app import models, database
import uvicorn
import os
import shutil
import random

# Создаем таблицы в базе данных
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Fashion AI Platform 🎀")

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Создаем папку для загрузки фото
UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Зависимость для получения базы данных
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========== ГЛАВНАЯ СТРАНИЦА ==========
@app.get("/")
def home():
    return {"message": "Добро пожаловать в Fashion AI! 💕"}

# ========== ВЕБ-ИНТЕРФЕЙС ==========
@app.get("/ui")
def get_ui():
    return FileResponse("app/templates/index.html")

# ========== ГАРДЕРОБ ==========
@app.get("/wardrobe")
def get_wardrobe(db: Session = Depends(get_db)):
    items = db.query(models.WardrobeItem).all()
    return {"wardrobe": items}

@app.get("/wardrobe-with-images")
def get_wardrobe_with_images(db: Session = Depends(get_db)):
    items = db.query(models.WardrobeItem).all()
    return {
        "wardrobe": [
            {
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "color": item.color,
                "image_url": item.image_path if item.image_path else None
            }
            for item in items
        ]
    }

# ========== ДОБАВЛЕНИЕ ВЕЩЕЙ ==========
@app.post("/add-item")
def add_item(name: str, category: str, color: str, db: Session = Depends(get_db)):
    new_item = models.WardrobeItem(
        name=name,
        category=category,
        color=color
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"message": "Вещь добавлена в гардероб! 🎀", "item": new_item}

# ========== ЗАГРУЗКА С ФОТО ==========
@app.post("/upload-item")
async def upload_item(
    name: str = Form(...),
    category: str = Form(...),
    color: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Сохраняем файл
    safe_name = name.replace(" ", "_")
    file_path = os.path.join(UPLOAD_DIR, f"{safe_name}_{image.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Создаем запись в базе
    new_item = models.WardrobeItem(
        name=name,
        category=category,
        color=color,
        image_path=f"/static/uploads/{safe_name}_{image.filename}"
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return {
        "message": "Вещь с фото добавлена! 📸", 
        "item": new_item,
        "image_url": new_item.image_path
    }

# ========== ГЕНЕРАЦИЯ ОБРАЗОВ ==========
@app.get("/generate-outfit")
def generate_outfit(db: Session = Depends(get_db)):
    items = db.query(models.WardrobeItem).all()
    if not items:
        return {"message": "Добавь вещи в гардероб сначала! 💕"}
    
    tops = [item for item in items if item.category in ['top', 'dress']]
    bottoms = [item for item in items if item.category == 'bottom']
    shoes = [item for item in items if item.category == 'shoes']
    
    outfit = {}
    if tops:
        outfit["top"] = random.choice(tops).name
    if bottoms:
        outfit["bottom"] = random.choice(bottoms).name
    if shoes:
        outfit["shoes"] = random.choice(shoes).name
    
    return {"generated_outfit": outfit}

# ========== ПОГОДНЫЙ СТИЛИСТ ==========
@app.get("/weather-outfit")
def generate_weather_outfit(temperature: int = 20, precipitation: str = "no", db: Session = Depends(get_db)):
    items = db.query(models.WardrobeItem).all()
    if not items:
        return {"message": "Добавь вещи в гардероб сначала! 💕"}
    
    def get_weather_recommendation(temp):
        if temp > 25:
            return "Жарко - легкая одежда"
        elif temp > 15:
            return "Тепло - легкие слои"
        elif temp > 5:
            return "Прохладно - утепляйтесь"
        else:
            return "Холодно - теплая одежда"
    
    tops = [item for item in items if item.category in ['top', 'dress']]
    bottoms = [item for item in items if item.category == 'bottom']
    shoes = [item for item in items if item.category == 'shoes']
    
    outfit = {}
    if tops:
        outfit["top"] = random.choice(tops).name
    if bottoms:
        outfit["bottom"] = random.choice(bottoms).name
    if shoes:
        outfit["shoes"] = random.choice(shoes).name
    
    return {
        "generated_outfit": outfit,
        "weather_advice": {"description": get_weather_recommendation(temperature)}
    }

# ========== ИЗБРАННОЕ ==========
@app.post("/save-favorite")
def save_favorite(outfit_data: str, rating: int = 5, occasion: str = "casual", db: Session = Depends(get_db)):
    favorite = models.FavoriteOutfit(
        outfit_data=outfit_data,
        rating=rating,
        occasion=occasion
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return {"message": "Образ сохранен в избранное! ❤️", "favorite_id": favorite.id}

@app.get("/favorites")
def get_favorites(db: Session = Depends(get_db)):
    favorites = db.query(models.FavoriteOutfit).all()
    return {"favorites": favorites}

@app.get("/ai-outfit")
def generate_ai_outfit(db: Session = Depends(get_db)):
    items = db.query(models.WardrobeItem).all()
    if not items:
        return {"message": "Добавь вещи в гардероб сначала! 💕"}
    
    tops = [item for item in items if item.category in ['top', 'dress']]
    bottoms = [item for item in items if item.category == 'bottom']
    shoes = [item for item in items if item.category == 'shoes']
    
    outfit = {}
    if tops:
        outfit["top"] = random.choice(tops).name
    if bottoms:
        outfit["bottom"] = random.choice(bottoms).name
    if shoes:
        outfit["shoes"] = random.choice(shoes).name
    
    return {
        "generated_outfit": outfit,
        "message": "Вот AI-образ! 🧠✨",
        "ai_enhanced": True
    }

# ========== ЗАПУСК СЕРВЕРА ==========
if __name__ == "__main__":
    print("🚀 Запускаю Fashion AI Platform...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")