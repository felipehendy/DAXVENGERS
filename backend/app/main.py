"""
Servidor principal da API DAXVengers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Importar rotas
from app.api.lessons import router as lessons_router

# Criar app FastAPI
app = FastAPI(
    title="DAXVengers API",
    description="API para o jogo gamificado de aprendizado de Power BI e DAX",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Configurar CORS para permitir frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite/Svelte dev server
        "http://localhost:3000",
        "http://localhost:8080",
        "https://daxvengers.vercel.app",  # Produção
        "*"  # Permitir todos (apenas para desenvolvimento)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(lessons_router)


# ============================================
# ROTA RAIZ
# ============================================

@app.get("/")
async def root():
    """
    Endpoint raiz da API
    """
    return {
        "service": "DAXVengers API",
        "version": "1.0.0",
        "status": "online",
        "message": "Bem-vindo à API do DAXVengers! 🦸‍♂️",
        "docs": "/docs",
        "health": "/api/health"
    }


# ============================================
# TRATAMENTO DE ERROS
# ============================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handler para erros 404"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "O recurso solicitado não foi encontrado",
            "path": str(request.url)
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handler para erros 500"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Ocorreu um erro interno no servidor",
            "detail": str(exc)
        }
    )


# ============================================
# STARTUP/SHUTDOWN EVENTS
# ============================================

@app.on_event("startup")
async def startup_event():
    """Executado quando o servidor inicia"""
    print("🚀 DAXVengers API iniciada!")
    print("📚 Lições carregadas com sucesso")
    print("🌐 Servidor rodando em: http://localhost:8000")
    print("📖 Documentação em: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Executado quando o servidor desliga"""
    print("👋 DAXVengers API encerrada")


# ============================================
# EXECUTAR SERVIDOR
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload em desenvolvimento
        log_level="info"
    )