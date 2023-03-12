from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models, schemas

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def list_game(session: Session = Depends(get_db)):
    games = session.query(models.Game).all()
    return games

@app.get("/{id}")
def get_game_by_id(id: int, session: Session = Depends(get_db)):
    game = session.query(models.Game).filter(models.Game.id == id).first()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@app.post("/")
def create_game(game: schemas.Game, session: Session = Depends(get_db)):
    new_game = models.Game(name=game.name, developer=game.developer)
    session.add(new_game)
    session.commit()
    session.refresh(new_game)
    return new_game

@app.put("/{id}")
def update_game(id: int, game: schemas.Game, session: Session = Depends(get_db)):
    game_update = session.query(models.Game).get(id)
    
    if game_update is None:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game_update.name = game.name
    game_update.developer = game.developer
    session.commit()
    return game_update

@app.delete("/{id}")
def delete_game(id: int, session: Session = Depends(get_db)):
    game_del = session.query(models.Game).get(id)
    
    if game_del is None:
        raise HTTPException(status_code=404, detail="Game not found")
    
    session.delete(game_del)
    session.commit()
    session.close()
    return 'Game was deleted'

