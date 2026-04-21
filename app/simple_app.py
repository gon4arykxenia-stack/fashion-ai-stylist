from fastapi import FastAPI
import uvicorn
import random

app = FastAPI(title="Fashion AI Platform 🎀")

# Временное хранилище вместо базы данных
wardrobe = []

@app.get("/")
def home():
    return {"message": "Добро пожаловать в Fashion AI! 💕"}

@app.get("/wardrobe")
def get_wardrobe():
    return {"wardrobe": wardrobe}

@app.post("/add-item")
def add_item(name: str, category: str, color: str):
    new_item = {
        "id": len(wardrobe) + 1,
        "name": name,
        "category": category,
        "color": color
    }
    wardrobe.append(new_item)
    return {"message": "Вещь добавлена! 🎀", "item": new_item}

@app.get("/generate-outfit")
def generate_outfit():
    if not wardrobe:
        return {"message": "Добавь вещи в гардероб сначала! 💕"}
    
    tops = [item for item in wardrobe if item["category"] in ["top", "dress"]]
    bottoms = [item for item in wardrobe if item["category"] == "bottom"]
    shoes = [item for item in wardrobe if item["category"] == "shoes"]
    
    outfit = {}
    if tops:
        top = random.choice(tops)
        outfit["top"] = f"{top['color']} {top['name']}"
    
    if bottoms:
        bottom = random.choice(bottoms)
        outfit["bottom"] = f"{bottom['color']} {bottom['name']}"
    
    if shoes:
        shoe = random.choice(shoes)
        outfit["shoes"] = f"{shoe['color']} {shoe['name']}"
    
    return {"outfit": outfit, "message": "Вот твой образ! ✨"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    global wardrobe
    for i, item in enumerate(wardrobe):
        if item["id"] == item_id:
            deleted_item = wardrobe.pop(i)
            return {"message": f"Удалено: {deleted_item['name']}"}
    return {"error": "Вещь не найдена"}

if __name__ == "__main__":
    print("🚀 Запускаю упрощенную версию Fashion AI...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")