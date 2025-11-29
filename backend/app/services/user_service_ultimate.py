from app.core.supabase_fixed import supabase
from app.models.user_models import UserCreate, UserResponse
from typing import Optional
import asyncio

class UserServiceUltimate:
    
    @staticmethod
    async def create_user(user_data: UserCreate) -> Optional[UserResponse]:
        try:
            print(f"🚀 ULTIMATE - Criando usuário: {user_data.username}")
            
            # ETAPA 1: Criar usuário no Auth
            from supabase import create_client
            
            # Client para Auth
            auth_client = create_client(
                "https://nkutkbbprklquhkimhwu.supabase.co",
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rdXRrYmJwcmtscXVoa2ltaHd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQzMDUyNjAsImV4cCI6MjA3OTg4MTI2MH0.muSz7gIUrNCBUi2OkyYN5Tmh6Lrs6c28HHMRCHgLecg"
            )
            
            auth_response = auth_client.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password
            })
            
            if not auth_response.user:
                print("❌ Falha no Auth")
                return None
            
            user_id = auth_response.user.id
            print(f"✅ Auth criado - ID: {user_id}")
            
            # Aguardar para garantir que o Auth foi processado
            await asyncio.sleep(2)
            
            # ETAPA 2: Criar perfil na tabela users COM MÚLTIPLAS TENTATIVAS
            print("📊 Tentando criar perfil na tabela users...")
            profile_data = {
                "id": user_id,
                "username": user_data.username,
                "email": user_data.email,
                "xp": 0,
                "coins": 0,
                "level": 1,
                "streak_days": 0,
                "is_premium": False
            }
            
            # Tentativa 1
            try:
                response = supabase.from_("users").insert(profile_data).execute()
                if response.data:
                    print("🎉 Usuário criado com sucesso na 1ª tentativa!")
                    return UserResponse(**response.data[0])
            except Exception as e1:
                print(f"⚠️ Tentativa 1 falhou: {e1}")
            
            # Tentativa 2 - Aguardar mais e tentar novamente
            await asyncio.sleep(3)
            try:
                response = supabase.from_("users").insert(profile_data).execute()
                if response.data:
                    print("🎉 Usuário criado com sucesso na 2ª tentativa!")
                    return UserResponse(**response.data[0])
            except Exception as e2:
                print(f"⚠️ Tentativa 2 falhou: {e2}")
            
            # Tentativa 3 - Verificar se usuário já foi criado
            await asyncio.sleep(2)
            try:
                existing = supabase.from_("users").select("*").eq("id", user_id).execute()
                if existing.data:
                    print("✅ Usuário já existe na tabela (recuperado)")
                    return UserResponse(**existing.data[0])
            except Exception as e3:
                print(f"⚠️ Tentativa 3 falhou: {e3}")
            
            print("❌ Todas as tentativas falharam")
            return None
            
        except Exception as e:
            print(f"💥 Erro crítico: {e}")
            return None
    
    @staticmethod
    async def manual_create_user(user_id: str, username: str, email: str) -> Optional[UserResponse]:
        """Criar usuário manualmente se o automático falhar"""
        try:
            profile_data = {
                "id": user_id,
                "username": username,
                "email": email,
                "xp": 0,
                "coins": 0,
                "level": 1,
                "streak_days": 0,
                "is_premium": False
            }
            
            response = supabase.from_("users").insert(profile_data).execute()
            if response.data:
                print(f"🎉 Usuário {username} criado manualmente!")
                return UserResponse(**response.data[0])
            return None
        except Exception as e:
            print(f"❌ Erro criação manual: {e}")
            return None

# Instância global
user_service_ultimate = UserServiceUltimate()