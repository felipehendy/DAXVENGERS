import os
from supabase import create_client, Client
from dotenv import load_dotenv

# SOLUÇÃO DEFINITIVA - Carregar .env de múltiplas localizações
def load_environment():
    # Tentar diferentes caminhos possíveis
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'),  # Raiz do projeto
        os.path.join(os.path.dirname(__file__), '..', '..', '.env'),        # Pasta backend
        os.path.join(os.getcwd(), '.env'),                                  # Diretório atual
        'C:\\Users\\felipe.silva\\Desktop\\DAX GAME\\.env'                  # Caminho absoluto
    ]
    
    for env_path in possible_paths:
        print(f"🔍 Tentando carregar .env de: {env_path}")
        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"✅ .env carregado de: {env_path}")
            return True
    
    print("❌ Nenhum arquivo .env encontrado nos caminhos tentados")
    return False

# Carregar ambiente
load_environment()

class SupabaseClient:
    def __init__(self):
        # Usar valores padrão se não encontrar no .env
        self.url: str = os.getenv("SUPABASE_URL", "https://nkutkbbprklquhkimhwu.supabase.co")
        self.key: str = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rdXRrYmJwcmtscXVoa2ltaHd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQzMDUyNjAsImV4cCI6MjA3OTg4MTI2MH0.muSz7gIUrNCBUi2OkyYN5Tmh6Lrs6c28HHMRCHgLecg")
        
        print(f"🔧 SUPABASE_URL: {self.url}")
        print(f"🔧 SUPABASE_ANON_KEY: {self.key[:20]}..." if self.key else "❌ Chave não encontrada")
        
        if not self.url or not self.key:
            raise ValueError("Supabase credentials not found")
        
        try:
            self.client: Client = create_client(self.url, self.key)
            print("✅ Supabase client initialized successfully!")
        except Exception as e:
            print(f"❌ Erro ao criar cliente Supabase: {e}")
            raise

    def get_client(self) -> Client:
        return self.client

# Instância global com tratamento de erro robusto
try:
    supabase = SupabaseClient()
    print("🎉 Supabase configurado com sucesso!")
except Exception as e:
    print(f"💥 Falha crítica ao inicializar Supabase: {e}")
    # Criar um cliente mock para desenvolvimento
    supabase = None