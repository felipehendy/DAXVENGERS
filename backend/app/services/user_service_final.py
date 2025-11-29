from app.core.supabase_fixed import supabase
from app.models.user_models import UserCreate, UserResponse
from typing import Optional
import asyncio

class UserServiceFinal:
    
    @staticmethod
    async def create_user(user_data: UserCreate) -> Optional[UserResponse]:
        try:
            print(f"🚀 Criando usuário: {user_data.username}")
            
            # ETAPA 1: Criar usuário no Auth (com client normal)
            from supabase import create_client
            
            # Client normal para Auth (não precisa de service role)
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
            
            # Aguardar um pouco
            await asyncio.sleep(1)
            
            # ETAPA 2: Criar perfil na tabela users USANDO SERVICE ROLE (bypass RLS)
            print("📊 Criando perfil na tabela users...")
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
            
            try:
                # Usar o client com Service Role para bypass do RLS
                response = supabase.from_("users").insert(profile_data).execute()
                
                if response.data:
                    print("🎉 Usuário criado com sucesso!")
                    return UserResponse(**response.data[0])
                else:
                    print(f"⚠️ Nenhum dado retornado: {response}")
                    return None
                    
            except Exception as insert_error:
                print(f"❌ Erro na inserção: {insert_error}")
                return None
            
        except Exception as e:
            print(f"💥 Erro crítico: {e}")
            return None

# Instância global
user_service_final = UserServiceFinal()