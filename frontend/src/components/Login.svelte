<script>
  import { supabase } from '../supabaseClient.js'
  
  export let showLanding = true
  export let onBackToLanding = () => {}
  
  let email = ''
  let password = ''
  let username = ''
  let isLogin = true
  let loading = false
  let errorMessage = ''
  let successMessage = ''

  async function handleSubmit() {
    loading = true
    errorMessage = ''
    successMessage = ''

    try {
      if (isLogin) {
        // LOGIN
        console.log('🔐 Tentando fazer login com:', email)
        
        const { data, error } = await supabase.auth.signInWithPassword({
          email,
          password
        })
        
        console.log('📊 Resposta do login:', { data, error })
        
        if (error) throw error
        
        successMessage = '✅ Login realizado com sucesso!'
        console.log('✅ Usuário logado:', data)
        
        setTimeout(() => {
          window.location.reload()
        }, 1000)
        
      } else {
        // REGISTRO
        console.log('📝 Tentando registrar:', email, username)
        
        const { data, error } = await supabase.auth.signUp({
          email,
          password,
          options: {
            data: {
              username: username
            }
          }
        })
        
        console.log('📊 Resposta do registro:', { data, error })
        
        if (error) throw error
        
        if (data.user && !data.session) {
          successMessage = '✅ Conta criada! Verifique seu email para confirmar.'
        } else {
          successMessage = '✅ Conta criada e login automático realizado!'
          setTimeout(() => {
            window.location.reload()
          }, 1000)
        }
        
        console.log('✅ Usuário registrado:', data)
      }
      
    } catch (error) {
      errorMessage = '❌ Erro: ' + error.message
      console.error('❌ Erro completo:', error)
    } finally {
      loading = false
    }
  }

  function toggleMode() {
    isLogin = !isLogin
    errorMessage = ''
    successMessage = ''
  }
</script>

<div class="auth-container">
  <div class="auth-bg">
    <div class="bg-circle circle-1"></div>
    <div class="bg-circle circle-2"></div>
  </div>

  <div class="auth-card">
    {#if showLanding}
      <button class="back-btn" on:click={onBackToLanding}>
        <span>←</span> Voltar
      </button>
    {/if}

    <div class="auth-header">
      <div class="logo">
        <span class="logo-icon">⚡</span>
        <h1>DAXVengers</h1>
      </div>
      <h2>{isLogin ? 'Bem-vindo de volta!' : 'Junte-se aos Vingadores'}</h2>
      <p>{isLogin ? 'Entre para continuar sua jornada' : 'Crie sua conta e comece a dominar o DAX'}</p>
    </div>

    <form on:submit|preventDefault={handleSubmit}>
      
      {#if !isLogin}
        <div class="form-group">
          <label for="username">
            <span class="label-icon">👤</span>
            Nome de Herói
          </label>
          <input
            id="username"
            type="text"
            bind:value={username}
            placeholder="Seu nome de vingador"
            required={!isLogin}
          />
        </div>
      {/if}

      <div class="form-group">
        <label for="email">
          <span class="label-icon">📧</span>
          Email
        </label>
        <input
          id="email"
          type="email"
          bind:value={email}
          placeholder="seu@email.com"
          required
        />
      </div>

      <div class="form-group">
        <label for="password">
          <span class="label-icon">🔒</span>
          Senha
        </label>
        <input
          id="password"
          type="password"
          bind:value={password}
          placeholder="Mínimo 6 caracteres"
          required
          minlength="6"
        />
      </div>

      {#if errorMessage}
        <div class="message error">
          <span class="message-icon">❌</span>
          {errorMessage}
        </div>
      {/if}

      {#if successMessage}
        <div class="message success">
          <span class="message-icon">✅</span>
          {successMessage}
        </div>
      {/if}

      <button type="submit" class="submit-btn" disabled={loading}>
        {#if loading}
          <span class="spinner-small"></span>
          Processando...
        {:else}
          <span class="btn-icon">{isLogin ? '🚀' : '✨'}</span>
          {isLogin ? 'Entrar' : 'Criar Conta'}
        {/if}
      </button>
    </form>

    <div class="auth-footer">
      <button class="toggle-btn" on:click={toggleMode}>
        {isLogin ? 'Não tem conta? Criar uma!' : 'Já tem conta? Fazer login'}
      </button>
    </div>
  </div>
</div>

<style>
  .auth-container {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: var(--color-bg-darker);
    padding: 20px;
    position: relative;
    overflow: hidden;
  }

  .auth-bg {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    overflow: hidden;
  }

  .bg-circle {
    position: absolute;
    border-radius: 50%;
    filter: blur(100px);
    opacity: 0.15;
    animation: float-circle 15s ease-in-out infinite;
  }

  .circle-1 {
    width: 600px;
    height: 600px;
    background: var(--color-primary);
    top: -300px;
    right: -300px;
  }

  .circle-2 {
    width: 500px;
    height: 500px;
    background: var(--color-secondary);
    bottom: -250px;
    left: -250px;
    animation-delay: 7s;
  }

  @keyframes float-circle {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(30px, -30px) scale(1.1); }
  }

  .auth-card {
    background: var(--color-bg-card);
    border: 2px solid rgba(255, 107, 53, 0.2);
    border-radius: var(--border-radius-lg);
    padding: 50px 40px;
    width: 100%;
    max-width: 480px;
    box-shadow: var(--shadow-lg);
    position: relative;
    z-index: 1;
    backdrop-filter: blur(10px);
  }

  .back-btn {
    position: absolute;
    top: 20px;
    left: 20px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--color-text-secondary);
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .back-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--color-text-primary);
  }

  .auth-header {
    text-align: center;
    margin-bottom: 40px;
  }

  .logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin-bottom: 20px;
  }

  .logo-icon {
    font-size: 3rem;
    filter: drop-shadow(0 0 20px var(--color-primary));
    animation: pulse 3s ease-in-out infinite;
  }

  .logo h1 {
    font-size: 2.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
  }

  .auth-header h2 {
    font-size: 1.8rem;
    margin: 0 0 10px 0;
    color: var(--color-text-primary);
    font-weight: 700;
  }

  .auth-header p {
    color: var(--color-text-secondary);
    font-size: 1rem;
    margin: 0;
  }

  .form-group {
    margin-bottom: 25px;
  }

  label {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
    color: var(--color-text-primary);
    font-weight: 600;
    font-size: 0.95rem;
  }

  .label-icon {
    font-size: 1.2rem;
  }

  input {
    width: 100%;
    padding: 14px 18px;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius);
    font-size: 16px;
    color: var(--color-text-primary);
    transition: all 0.3s;
    box-sizing: border-box;
  }

  input::placeholder {
    color: var(--color-text-muted);
  }

  input:focus {
    outline: none;
    border-color: var(--color-primary);
    background: rgba(255, 255, 255, 0.08);
    box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
  }

  .message {
    padding: 14px 18px;
    border-radius: var(--border-radius);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 500;
    font-size: 0.95rem;
  }

  .message-icon {
    font-size: 1.2rem;
  }

  .message.error {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
  }

  .message.success {
    background: rgba(74, 222, 128, 0.1);
    color: #4ade80;
    border: 1px solid rgba(74, 222, 128, 0.3);
  }

  .submit-btn {
    width: 100%;
    padding: 16px;
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    color: white;
    border: none;
    border-radius: var(--border-radius);
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    box-shadow: 0 10px 30px rgba(255, 107, 53, 0.3);
  }

  .submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 15px 40px rgba(255, 107, 53, 0.5);
  }

  .submit-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .btn-icon {
    font-size: 1.3rem;
  }

  .spinner-small {
    width: 18px;
    height: 18px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .auth-footer {
    text-align: center;
    margin-top: 25px;
  }

  .toggle-btn {
    background: none;
    border: none;
    color: var(--color-primary);
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 600;
    padding: 8px;
    transition: all 0.3s;
  }

  .toggle-btn:hover {
    color: var(--color-secondary);
    text-decoration: underline;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
  }

  /* Responsive */
  @media (max-width: 480px) {
    .auth-card {
      padding: 40px 25px;
    }

    .logo h1 {
      font-size: 2rem;
    }

    .auth-header h2 {
      font-size: 1.5rem;
    }
  }
</style>