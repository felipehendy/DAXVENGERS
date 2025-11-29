from supabase import create_client, Client

# Teste com a API da versão 1.0.3
url = "https://nkutkbbprklquhkimhwu.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rdXRrYmJwcmtscXVoa2ltaHd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQzMDUyNjAsImV4cCI6MjA3OTg4MTI2MH0.muSz7gIUrNCBUi2OkyYN5Tmh6Lrs6c28HHMRCHgLecg"

print("🧪 Testando Supabase v1.0.3...")

try:
    client: Client = create_client(url, key)
    print("✅ Cliente Supabase criado!")
    
    # Testar consulta
    response = client.from_('users').select('*', count='exact').limit(1).execute()
    print(f"✅ Conexão OK! Usuários: {response.count}")
    
except Exception as e:
    print(f"❌ Erro: {e}")