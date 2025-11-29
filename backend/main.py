"""
Servidor principal da API DAXVengers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Importar rotas (vamos criar em seguida)
# from app.api.lessons import router as lessons_router

# Criar app FastAPI
app = FastAPI(
    title="DAXVengers API",
    description="API para o jogo gamificado de aprendizado de Power BI e DAX",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota raiz
@app.get("/")
async def root():
    return {
        "service": "DAXVengers API",
        "version": "1.0.0",
        "status": "online",
        "message": "Bem-vindo à API do DAXVengers! 🦸‍♂️",
        "docs": "/docs"
    }

# Health check
@app.get("/api/health")
async def health_check():
    return {
        "status": "online",
        "service": "DAXVengers API"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )