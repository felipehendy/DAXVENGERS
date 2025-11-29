"""
Modelos de dados para lições, missões e progresso do usuário
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class ExerciseType(str, Enum):
    """Tipos de exercícios disponíveis"""
    MULTIPLE_CHOICE = "multiple_choice"
    CODE = "code"
    FILL_BLANK = "fill_blank"
    DEBUG = "debug"
    OUTPUT_PREDICTION = "output_prediction"


class LessonType(str, Enum):
    """Tipos de lições"""
    THEORY = "theory"
    PRACTICE = "practice"
    CHALLENGE = "challenge"
    BOSS = "boss"


class Exercise(BaseModel):
    """Modelo de um exercício"""
    type: ExerciseType
    question: str
    options: Optional[List[str]] = None  # Para multiple choice
    correct: Optional[int] = None  # Índice da resposta correta
    solution: Optional[str] = None  # Para exercícios de código
    hints: List[str] = Field(default_factory=list)
    explanation: str
    xp_reward: int = 10

    class Config:
        schema_extra = {
            "example": {
                "type": "multiple_choice",
                "question": "O que significa DAX?",
                "options": [
                    "Data Analysis Expressions",
                    "Database Analysis eXcel",
                    "Dynamic Analysis X-ray",
                    "Data Advanced eXcel"
                ],
                "correct": 0,
                "explanation": "DAX = Data Analysis Expressions",
                "xp_reward": 10
            }
        }


class Lesson(BaseModel):
    """Modelo de uma lição"""
    id: int
    title: str
    icon: str
    description: str
    xp: int
    type: LessonType = LessonType.THEORY
    mission_id: str
    order: int
    
    # Conteúdo da lição
    theory: str
    theory_title: Optional[str] = "O que você vai aprender"
    key_concepts: List[str] = Field(default_factory=list)
    
    # Exercícios
    exercises: List[Exercise]
    
    # Metadados
    estimated_time: int = 5  # minutos
    prerequisites: List[int] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Introdução ao DAX",
                "icon": "📊",
                "description": "Aprenda o que é DAX e por que ele é importante",
                "xp": 50,
                "type": "theory",
                "mission_id": "dax-basics",
                "order": 1,
                "theory": "<p>DAX (Data Analysis Expressions) é a linguagem de fórmulas do Power BI...</p>",
                "key_concepts": ["DAX", "Medidas", "Colunas Calculadas"],
                "exercises": [],
                "estimated_time": 5
            }
        }


class Mission(BaseModel):
    """Modelo de uma missão (conjunto de lições)"""
    id: str
    name: str
    icon: str
    description: str
    total_lessons: int
    total_xp: int
    is_free: bool = True
    order: int
    badge_reward: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "id": "dax-basics",
                "name": "Funções Básicas DAX",
                "icon": "🦾",
                "description": "Domine as funções essenciais do DAX",
                "total_lessons": 5,
                "total_xp": 320,
                "is_free": True,
                "order": 1,
                "badge_reward": "Iron Man"
            }
        }


class UserProgress(BaseModel):
    """Modelo de progresso do usuário"""
    user_id: str
    mission_id: str
    completed_lessons: List[int] = Field(default_factory=list)
    current_lesson: int = 1
    total_xp: int = 0
    streak_days: int = 0
    last_activity: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "mission_id": "dax-basics",
                "completed_lessons": [1, 2, 3],
                "current_lesson": 4,
                "total_xp": 170,
                "streak_days": 5,
                "last_activity": "2025-11-27T10:30:00"
            }
        }


class ProgressUpdate(BaseModel):
    """Modelo para atualizar progresso"""
    user_id: str
    lesson_id: int
    xp_earned: int
    completed: bool = True
    time_spent: Optional[int] = None  # segundos
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "lesson_id": 1,
                "xp_earned": 50,
                "completed": True,
                "time_spent": 180
            }
        }


class Badge(BaseModel):
    """Modelo de badge/conquista"""
    id: str
    name: str
    icon: str
    description: str
    requirement: str
    xp_reward: int
    rarity: str = "common"  # common, rare, epic, legendary
    
    class Config:
        schema_extra = {
            "example": {
                "id": "iron_man",
                "name": "Iron Man",
                "icon": "🦾",
                "description": "Complete 5 lições",
                "requirement": "complete_5_lessons",
                "xp_reward": 100,
                "rarity": "rare"
            }
        }


class LeaderboardEntry(BaseModel):
    """Entrada do ranking"""
    user_id: str
    username: str
    total_xp: int
    completed_lessons: int
    streak_days: int
    badges: List[str] = Field(default_factory=list)
    rank: int
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "username": "DAXMaster",
                "total_xp": 1250,
                "completed_lessons": 25,
                "streak_days": 10,
                "badges": ["iron_man", "captain_america"],
                "rank": 1
            }
        }