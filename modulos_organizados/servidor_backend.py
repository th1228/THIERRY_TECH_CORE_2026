# ==========================================
# MÓDULO DE SERVIDOR BACKEND (FastAPI / Rotas)
# ==========================================
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Soberano Kernel Ativo", "porta": 801}
