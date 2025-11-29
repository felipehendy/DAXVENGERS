from supabase import create_client, Client

# USAR SERVICE ROLE KEY para bypass do RLS quando necessário
SUPABASE_URL = "https://nkutkbbprklquhkimhwu.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rdXRrYmJwcmtscXVoa2ltaHd1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDMwNTI2MCwiZXhwIjoyMDc5ODgxMjYwfQ.pzVFo4c7eZdupRFrphuxX9HKqN8L5KENV2X-6uD_CyM"

print("🔧 Inicializando Supabase Client com Service Role...")

try:
    # Usar SERVICE ROLE KEY para operações administrativas
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    print("✅ Supabase Client (Service Role) criado com sucesso!")
    
    # Testar conexão
    test_response = supabase.from_('users').select('*', count='exact').execute()
    print(f"📊 Teste de conexão: {len(test_response.data)} usuários")
    
except Exception as e:
    print(f"❌ Erro ao criar Supabase Client: {e}")
    supabase = None