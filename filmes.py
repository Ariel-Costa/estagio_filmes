from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json, os

app = FastAPI()
FILMES = "filmes.json"

class Filme(BaseModel):
    titulo: str
    ano: int
    genero: str

def carregar_filmes():
    if os.path.exists(FILMES):
        with open(FILMES, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def salvar_filmes(filmes):
    with open(FILMES, "w", encoding="utf-8") as f:
        json.dump(filmes, f, indent=4, ensure_ascii=False)

@app.get("/filmes")
def listar_filmes():
    return carregar_filmes()

@app.post("/filmes")
def adicionar_filme(filme: Filme):
    filmes = carregar_filmes()
    novo_id = max([f.get("id", 0) for f in filmes], default=0) + 1
    novo_filme = {"id": novo_id, **filme.dict()}
    filmes.append(novo_filme)
    salvar_filmes(filmes)
    return novo_filme

@app.get("/filmes/{id}")
def obter_filme(id: int):
    filmes = carregar_filmes()
    for filme in filmes:
        if filme["id"] == id:
            return filme
    raise HTTPException(status_code=404, detail="Filme não encontrado")
