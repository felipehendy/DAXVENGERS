from app.core.supabase_fixed import supabase
from app.models.user_models import UserCreate, UserResponse, UserUpdate
from typing import Optional, List

class UserService:
    
    @staticmethod
    async def create_user(user_data: UserCreate) -> Optional[UserResponse]:
        try:
            print(f"📝 Criando usuário: {user_data.username}")
            
            # Criar usuário no Supabase Auth
            auth_response = supabase.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password
            })
            
            if auth_response.user:
                print(f"✅ Usuário auth criado: {auth_response.user.id}")
                
                # Criar perfil na tabela users
                profile_data = {
                    "id": auth_response.user.id,
                    "username": user_data.username,
                    "email": user_data.email,
                    "xp": 0,
                    "coins": 0,
                    "level": 1,
                    "streak_days": 0,
                    "is_premium": False
                }
                
                response = supabase.from_("users").insert(profile_data).execute()
                
                if response.data:
                    print(f"✅ Perfil criado na tabela users")
                    return UserResponse(**response.data[0])
            
            return None
            
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            return None
    
    @staticmethod
    async def login_user(email: str, password: str) -> Optional[dict]:
        try:
            print(f"🔐 Tentando login: {email}")
            
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                print(f"✅ Login bem-sucedido: {response.user.id}")
                
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
            
            return None
            
        except Exception as e:
            print(f"❌ Error logging in: {e}")
            return None
    
    @staticmethod
    async def get_user(user_id: str) -> Optional[UserResponse]:
        try:
            response = supabase.from_("users")\
                .select("*")\
                .eq("id", user_id)\
                .execute()
            
            if response.data:
                return UserResponse(**response.data[0])
            return None
            
        except Exception as e:
            print(f"❌ Error getting user: {e}")
            return None
    
    @staticmethod
    async def update_user_xp(user_id: str, xp_earned: int, coins_earned: int = 0) -> Optional[UserResponse]:
        try:
            print(f"🎯 Adicionando XP: {xp_earned} para usuário {user_id}")
            
            # Primeiro buscar usuário atual
            current_user = await UserService.get_user(user_id)
            if not current_user:
                return None
            
            # Calcular novo nível (1 nível a cada 1000 XP)
            new_xp = current_user.xp + xp_earned
            new_coins = current_user.coins + coins_earned
            new_level = max(1, new_xp // 1000 + 1)
            
            print(f"📊 Novo status - XP: {new_xp}, Moedas: {new_coins}, Nível: {new_level}")
            
            # Atualizar no banco
            response = supabase.from_("users")\
                .update({
                    "xp": new_xp,
                    "coins": new_coins,
                    "level": new_level
                })\
                .eq("id", user_id)\
                .execute()
            
            if response.data:
                return UserResponse(**response.data[0])
            return None
            
        except Exception as e:
            print(f"❌ Error updating user XP: {e}")
            return None