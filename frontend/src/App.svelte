<script>
  import { onMount } from 'svelte'
  import LandingPage from './components/LandingPage.svelte'
  import Login from './components/Login.svelte'
  import Dashboard from './components/Dashboard.svelte'
  import { user, loading, checkUser } from './stores/userStore.js'
  import './styles/theme.css'
  
  let showLanding = true
  let showLogin = false
  
  onMount(() => {
    checkUser()
  })

  function handleShowLogin() {
    showLanding = false
    showLogin = true
  }

  function handleShowRegister() {
    showLanding = false
    showLogin = true
  }

  function handleBackToLanding() {
    showLanding = true
    showLogin = false
  }
</script>

<main>
  {#if $loading}
    <div class="loading-screen">
      <div class="spinner-container">
        <div class="spinner"></div>
        <div class="spinner-glow"></div>
      </div>
      <h2>⚡ DAXVengers</h2>
      <p>Carregando seu poder...</p>
    </div>
  {:else if $user}
    <Dashboard />
  {:else if showLogin}
    <Login showLanding={true} onBackToLanding={handleBackToLanding} />
  {:else}
    <LandingPage onLogin={handleShowLogin} onRegister={handleShowRegister} />
  {/if}
</main>

<style>
  main {
    min-height: 100vh;
    background: var(--color-bg-dark);
  }

  .loading-screen {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, var(--color-bg-darker) 0%, var(--color-bg-dark) 100%);
    color: var(--color-text-primary);
  }

  .spinner-container {
    position: relative;
    width: 80px;
    height: 80px;
    margin-bottom: 30px;
  }

  .spinner {
    position: absolute;
    width: 80px;
    height: 80px;
    border: 4px solid rgba(255, 107, 53, 0.2);
    border-top-color: var(--color-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    z-index: 2;
  }

  .spinner-glow {
    position: absolute;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 107, 53, 0.3) 0%, transparent 70%);
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  @keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.2); opacity: 0.8; }
  }

  .loading-screen h2 {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
  }

  .loading-screen p {
    font-size: 1.2rem;
    color: var(--color-text-secondary);
    font-weight: 500;
  }
</style>