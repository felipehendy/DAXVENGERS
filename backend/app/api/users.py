from fastapi import APIRouter, HTTPException, Depends
from app.models.user_models import UserCreate, UserResponse, LoginRequest
from app.services.user_service_ultimate import user_service_ultimate
from app.core.supabase_fixed import supabase

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    """Registrar novo usuário - VERSÃO ULTIMATE"""
    user = await user_service_ultimate.create_user(user_data)
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Erro ao criar usuário. Tente um email diferente."
        )
    return user

@router.post("/login")
async def login_user(login_data: LoginRequest):
    """Login do usuário"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": login_data.email,
            "password": login_data.password
        })
        
        if response.user:
            # Buscar dados do usuário
            user_data = supabase.from_("users")\
                .select("*")\
                .eq("id", response.user.id)\
                .execute()
            
            if user_data.data:
                return {
                    "user": UserResponse(**user_data.data[0]),
                    "session": response.session
                }
        
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Erro no login")

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Buscar dados do usuário"""
    try:
        response = supabase.from_("users")\
            .select("*")\
            .eq("id", user_id)\
            .execute()
        
        if response.data:
            return UserResponse(**response.data[0])
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao buscar usuário")

@router.post("/{user_id}/add-xp")
async def add_user_xp(user_id: str, xp_earned: int = 100, coins_earned: int = 10):
    """Adicionar XP e moedas ao usuário"""
    try:
        # Buscar usuário atual
        current = supabase.from_("users")\
            .select("*")\
            .eq("id", user_id)\
            .execute()
        
        if not current.data:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        current_user = current.data[0]
        
        # Calcular novos valores
        new_xp = current_user['xp'] + xp_earned
        new_coins = current_user['coins'] + coins_earned
        new_level = max(1, new_xp // 1000 + 1)
        
        # Atualizar
        response = supabase.from_("users")\
            .update({
                "xp": new_xp,
                "coins": new_coins,
                "level": new_level
            })\
            .eq("id", user_id)\
            .execute()
        
        if response.data:
            return {
                "message": f"🎉 +{xp_earned} XP e +{coins_earned} moedas!",
                "user": UserResponse(**response.data[0])
            }
        
        raise HTTPException(status_code=400, detail="Erro ao atualizar")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/check/connection")
async def check_connection():
    """Verificar conexão com banco"""
    try:
        result = supabase.from_("users").select("id", count="exact").execute()
        return {
            "status": "connected",
            "users_count": result.count,
            "message": "✅ Conexão com Supabase estabelecida!"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@router.post("/manual-create")
async def manual_create_user(username: str, email: str):
    """Criar usuário manualmente para testes"""
    # Gerar um ID fake para teste
    import uuid
    user_id = str(uuid.uuid4())
    
    user = await user_service_ultimate.manual_create_user(user_id, username, email)
    if not user:
        raise HTTPException(status_code=400, detail="Erro na criação manual")
    return user