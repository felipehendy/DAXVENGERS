"""
Rotas da API para lições e missões
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime

from app.models.lesson import (
    Lesson, Mission, UserProgress, ProgressUpdate, LeaderboardEntry
)
from app.services.lesson_service import lesson_service

router = APIRouter(prefix="/api", tags=["lessons"])


# ============================================
# ROTAS DE MISSÕES
# ============================================

@router.get("/missions", response_model=List[Mission])
async def get_all_missions():
    """
    Retorna todas as missões disponíveis
    
    **Retorna:**
    - Lista de missões ordenadas por ordem de progressão
    """
    missions = lesson_service.get_all_missions()
    return missions


@router.get("/missions/{mission_id}", response_model=Mission)
async def get_mission(mission_id: str):
    """
    Retorna uma missão específica
    
    **Parâmetros:**
    - mission_id: ID da missão (ex: 'dax-basics')
    
    **Retorna:**
    - Dados completos da missão
    """
    mission = lesson_service.get_mission(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada")
    return mission


@router.get("/missions/{mission_id}/lessons", response_model=List[Lesson])
async def get_mission_lessons(mission_id: str):
    """
    Retorna todas as lições de uma missão
    
    **Parâmetros:**
    - mission_id: ID da missão
    
    **Retorna:**
    - Lista de lições da missão, ordenadas
    """
    mission = lesson_service.get_mission(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada")
    
    lessons = lesson_service.get_lessons_by_mission(mission_id)
    return lessons


# ============================================
# ROTAS DE LIÇÕES
# ============================================

@router.get("/lessons/{lesson_id}", response_model=Lesson)
async def get_lesson(lesson_id: int):
    """
    Retorna uma lição específica com todo o conteúdo
    
    **Parâmetros:**
    - lesson_id: ID numérico da lição
    
    **Retorna:**
    - Dados completos da lição incluindo teoria e exercícios
    """
    lesson = lesson_service.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lição não encontrada")
    return lesson


@router.get("/lessons/{lesson_id}/next", response_model=Lesson)
async def get_next_lesson(lesson_id: int, mission_id: str):
    """
    Retorna a próxima lição da sequência
    
    **Parâmetros:**
    - lesson_id: ID da lição atual
    - mission_id: ID da missão
    
    **Retorna:**
    - Próxima lição ou 404 se for a última
    """
    next_lesson = lesson_service.get_next_lesson(lesson_id, mission_id)
    if not next_lesson:
        raise HTTPException(
            status_code=404, 
            detail="Não há próxima lição (você completou a missão!)"
        )
    return next_lesson


# ============================================
# ROTAS DE PROGRESSO
# ============================================

@router.get("/progress/{user_id}", response_model=UserProgress)
async def get_user_progress(user_id: str, mission_id: str = "dax-basics"):
    """
    Retorna o progresso do usuário em uma missão
    
    **Parâmetros:**
    - user_id: ID do usuário
    - mission_id: ID da missão (padrão: 'dax-basics')
    
    **Retorna:**
    - Progresso completo do usuário
    
    **TODO:** Integrar com banco de dados real (Supabase)
    """
    # Por enquanto retorna dados mockados
    # Em produção, buscar do Supabase
    return UserProgress(
        user_id=user_id,
        mission_id=mission_id,
        completed_lessons=[],
        current_lesson=1,
        total_xp=0,
        streak_days=1,
        last_activity=datetime.now().isoformat()
    )


@router.post("/progress")
async def save_progress(progress: ProgressUpdate):
    """
    Salva o progresso do usuário ao completar uma lição
    
    **Body:**
    - user_id: ID do usuário
    - lesson_id: ID da lição completada
    - xp_earned: XP ganho na lição
    - completed: Se a lição foi completada
    - time_spent: Tempo gasto na lição (opcional)
    
    **Retorna:**
    - Confirmação e progresso atualizado
    
    **TODO:** Persistir no Supabase
    """
    # Validar lição existe
    lesson = lesson_service.get_lesson(progress.lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lição não encontrada")
    
    # Validar XP corresponde
    if progress.xp_earned > lesson.xp:
        raise HTTPException(
            status_code=400, 
            detail="XP ganho não pode ser maior que XP da lição"
        )
    
    # TODO: Salvar no Supabase
    # supabase_client.table('user_progress').upsert({
    #     'user_id': progress.user_id,
    #     'lesson_id': progress.lesson_id,
    #     'completed': progress.completed,
    #     'xp_earned': progress.xp_earned,
    #     'completed_at': datetime.now()
    # })
    
    return {
        "success": True,
        "message": f"Progresso salvo! +{progress.xp_earned} XP",
        "lesson_completed": progress.completed,
        "next_lesson_id": progress.lesson_id + 1
    }


@router.post("/progress/reset/{user_id}")
async def reset_progress(user_id: str, mission_id: str = "dax-basics"):
    """
    Reseta o progresso do usuário em uma missão
    
    **Parâmetros:**
    - user_id: ID do usuário
    - mission_id: ID da missão a resetar
    
    **Retorna:**
    - Confirmação do reset
    
    **CUIDADO:** Essa ação é irreversível!
    """
    # TODO: Implementar reset no Supabase
    return {
        "success": True,
        "message": f"Progresso resetado para missão {mission_id}",
        "user_id": user_id
    }


# ============================================
# ROTAS DE LEADERBOARD
# ============================================

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(limit: int = 10):
    """
    Retorna o ranking dos top jogadores
    
    **Parâmetros:**
    - limit: Número de jogadores a retornar (padrão: 10)
    
    **Retorna:**
    - Lista dos top jogadores ordenados por XP
    
    **TODO:** Buscar dados reais do Supabase
    """
    # Dados mockados para exemplo
    mock_leaderboard = [
        LeaderboardEntry(
            user_id="user1",
            username="DAXMaster",
            total_xp=1250,
            completed_lessons=25,
            streak_days=15,
            badges=["iron_man", "captain_america"],
            rank=1
        ),
        LeaderboardEntry(
            user_id="user2",
            username="BIHero",
            total_xp=980,
            completed_lessons=20,
            streak_days=10,
            badges=["iron_man"],
            rank=2
        )
    ]
    
    return mock_leaderboard[:limit]


# ============================================
# ROTA DE HEALTH CHECK
# ============================================

@router.get("/health")
async def health_check():
    """
    Verifica se a API está funcionando
    
    **Retorna:**
    - Status da API e estatísticas
    """
    total_lessons = len(lesson_service.lessons_db)
    total_missions = len(lesson_service.missions_db)
    
    return {
        "status": "online",
        "service": "DAXVengers API",
        "version": "1.0.0",
        "total_lessons": total_lessons,
        "total_missions": total_missions,
        "timestamp": datetime.now().isoformat()
    }