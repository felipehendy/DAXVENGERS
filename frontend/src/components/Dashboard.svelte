<script>
  import { user, logout } from '../stores/userStore.js'
  
  // Dados mock (depois vamos buscar do backend)
  let userStats = {
    xp: 0,
    level: 1,
    coins: 0,
    streak: 0,
    nextLevelXp: 500
  }
  
  $: xpProgress = (userStats.xp / userStats.nextLevelXp) * 100
  
  async function handleLogout() {
    await logout()
  }
  
  function startJourney() {
    alert('🚀 Jornada DAX será implementada em breve!')
  }
</script>

<div class="dashboard">
  <!-- Header -->
  <header class="header">
    <div class="header-content">
      <div class="logo">
        <span class="logo-icon">⚡</span>
        <h1>DAXVengers</h1>
      </div>
      
      <nav class="nav">
        <button class="nav-item active">
          <span class="icon">🏠</span>
          <span>Início</span>
        </button>
        <button class="nav-item">
          <span class="icon">🗺️</span>
          <span>Jornada</span>
        </button>
        <button class="nav-item">
          <span class="icon">🏆</span>
          <span>Ranking</span>
        </button>
        <button class="nav-item">
          <span class="icon">👤</span>
          <span>Perfil</span>
        </button>
      </nav>
      
      <button class="logout-btn" on:click={handleLogout}>
        <span class="icon">🚪</span>
        Sair
      </button>
    </div>
  </header>

  <!-- Main Content -->
  <main class="main-content">
    <div class="container">
      
      <!-- Welcome Section -->
      <section class="welcome-section">
        <div class="welcome-card">
          <div class="welcome-text">
            <h2>Bem-vindo de volta, <span class="highlight">{$user?.user_metadata?.username || 'Herói'}</span>! 🎉</h2>
            <p>Continue sua jornada para dominar o DAX e se tornar um verdadeiro vingador de dados!</p>
          </div>
          <button class="cta-button" on:click={startJourney}>
            <span class="icon">🚀</span>
            Continuar Jornada
          </button>
        </div>
      </section>

      <!-- Stats Grid -->
      <section class="stats-section">
        <div class="stats-grid">
          
          <!-- XP Card -->
          <div class="stat-card xp-card">
            <div class="stat-header">
              <div class="stat-icon">⭐</div>
              <div class="stat-label">Experiência</div>
            </div>
            <div class="stat-value">{userStats.xp} XP</div>
            <div class="progress-bar">
              <div class="progress-fill" style="width: {xpProgress}%"></div>
            </div>
            <div class="stat-footer">
              Faltam {userStats.nextLevelXp - userStats.xp} XP para o nível {userStats.level + 1}
            </div>
          </div>

          <!-- Level Card -->
          <div class="stat-card level-card">
            <div class="stat-header">
              <div class="stat-icon">🏆</div>
              <div class="stat-label">Nível</div>
            </div>
            <div class="stat-value level-badge">
              {userStats.level}
            </div>
            <div class="stat-footer">
              Iniciante DAX
            </div>
          </div>

          <!-- Coins Card -->
          <div class="stat-card coins-card">
            <div class="stat-header">
              <div class="stat-icon">💎</div>
              <div class="stat-label">Power Coins</div>
            </div>
            <div class="stat-value">{userStats.coins}</div>
            <div class="stat-footer">
              <button class="mini-btn">Ir para Loja</button>
            </div>
          </div>

          <!-- Streak Card -->
          <div class="stat-card streak-card">
            <div class="stat-header">
              <div class="stat-icon">🔥</div>
              <div class="stat-label">Sequência</div>
            </div>
            <div class="stat-value">{userStats.streak} dias</div>
            <div class="stat-footer">
              {#if userStats.streak === 0}
                Complete uma missão hoje!
              {:else}
                Continue assim! 💪
              {/if}
            </div>
          </div>

        </div>
      </section>

      <!-- Quick Actions -->
      <section class="actions-section">
        <h3>⚡ Ações Rápidas</h3>
        <div class="actions-grid">
          <button class="action-card">
            <div class="action-icon">📚</div>
            <div class="action-title">Lição Diária</div>
            <div class="action-subtitle">+50 XP</div>
          </button>
          
          <button class="action-card">
            <div class="action-icon">⚔️</div>
            <div class="action-title">Desafio Rápido</div>
            <div class="action-subtitle">+100 XP</div>
          </button>
          
          <button class="action-card">
            <div class="action-icon">🎯</div>
            <div class="action-title">Praticar</div>
            <div class="action-subtitle">Revise conceitos</div>
          </button>
          
          <button class="action-card">
            <div class="action-icon">👥</div>
            <div class="action-title">Ranking</div>
            <div class="action-subtitle">Veja sua posição</div>
          </button>
        </div>
      </section>

    </div>
  </main>
</div>

<style>
  .dashboard {
    min-height: 100vh;
    background: var(--color-bg-dark);
  }

  /* Header */
  .header {
    background: var(--color-bg-card);
    border-bottom: 2px solid rgba(255, 107, 53, 0.2);
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: var(--shadow-md);
  }

  .header-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px 40px;
    display: flex;
    align-items: center;
    gap: 30px;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .logo-icon {
    font-size: 2rem;
    filter: drop-shadow(0 0 10px var(--color-primary));
  }

  .logo h1 {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
  }

  .nav {
    display: flex;
    gap: 10px;
    flex: 1;
    margin-left: 40px;
  }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background: transparent;
    border: none;
    border-radius: var(--border-radius);
    color: var(--color-text-secondary);
    cursor: pointer;
    transition: all 0.3s;
    font-size: 15px;
    font-weight: 500;
  }

  .nav-item:hover {
    background: rgba(255, 107, 53, 0.1);
    color: var(--color-text-primary);
  }

  .nav-item.active {
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    color: white;
    box-shadow: var(--shadow-glow);
  }

  .nav-item .icon {
    font-size: 1.2rem;
  }

  .logout-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background: rgba(239, 68, 68, 0.1);
    border: 2px solid rgba(239, 68, 68, 0.3);
    border-radius: var(--border-radius);
    color: #ef4444;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s;
  }

  .logout-btn:hover {
    background: #ef4444;
    color: white;
    border-color: #ef4444;
  }

  /* Main Content */
  .main-content {
    padding: 40px 20px;
  }

  .container {
    max-width: 1400px;
    margin: 0 auto;
  }

  /* Welcome Section */
  .welcome-section {
    margin-bottom: 40px;
  }

  .welcome-card {
    background: linear-gradient(135deg, var(--color-bg-card) 0%, var(--color-bg-darker) 100%);
    border: 2px solid rgba(255, 107, 53, 0.2);
    border-radius: var(--border-radius-lg);
    padding: 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
  }

  .welcome-card::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(255, 107, 53, 0.1) 0%, transparent 70%);
    animation: pulse 3s ease-in-out infinite;
  }

  .welcome-text h2 {
    font-size: 2rem;
    margin: 0 0 10px 0;
    font-weight: 700;
  }

  .highlight {
    color: var(--color-primary);
    text-shadow: 0 0 20px rgba(255, 107, 53, 0.5);
  }

  .welcome-text p {
    color: var(--color-text-secondary);
    font-size: 1.1rem;
    margin: 0;
  }

  .cta-button {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 16px 32px;
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    border: none;
    border-radius: var(--border-radius);
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    box-shadow: var(--shadow-glow);
    transition: all 0.3s;
    z-index: 1;
  }

  .cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(255, 107, 53, 0.5);
  }

  .cta-button .icon {
    font-size: 1.5rem;
  }

  /* Stats Section */
  .stats-section {
    margin-bottom: 40px;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
  }

  .stat-card {
    background: var(--color-bg-card);
    border: 2px solid rgba(255, 255, 255, 0.05);
    border-radius: var(--border-radius-lg);
    padding: 25px;
    box-shadow: var(--shadow-md);
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
  }

  .stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
  }

  .stat-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255, 107, 53, 0.3);
    box-shadow: var(--shadow-lg);
  }

  .stat-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 15px;
  }

  .stat-icon {
    font-size: 2rem;
    filter: drop-shadow(0 0 10px rgba(255, 107, 53, 0.5));
  }

  .stat-label {
    font-size: 0.9rem;
    color: var(--color-text-secondary);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .stat-value {
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--color-text-primary);
    margin-bottom: 15px;
  }

  .level-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--color-level), var(--color-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .progress-bar {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 10px;
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--color-xp), var(--color-primary));
    border-radius: 10px;
    transition: width 0.5s ease;
    box-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
  }

  .stat-footer {
    font-size: 0.85rem;
    color: var(--color-text-muted);
  }

  .mini-btn {
    background: rgba(255, 107, 53, 0.1);
    border: 1px solid rgba(255, 107, 53, 0.3);
    color: var(--color-primary);
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all 0.3s;
  }

  .mini-btn:hover {
    background: var(--color-primary);
    color: white;
  }

  /* Actions Section */
  .actions-section {
    margin-bottom: 40px;
  }

  .actions-section h3 {
    font-size: 1.5rem;
    margin-bottom: 20px;
    color: var(--color-text-primary);
  }

  .actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
  }

  .action-card {
    background: var(--color-bg-card);
    border: 2px solid rgba(255, 255, 255, 0.05);
    border-radius: var(--border-radius-lg);
    padding: 30px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: var(--shadow-sm);
  }

  .action-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255, 107, 53, 0.5);
    box-shadow: var(--shadow-glow);
    background: var(--color-bg-card-hover);
  }

  .action-icon {
    font-size: 3rem;
    margin-bottom: 15px;
    filter: drop-shadow(0 0 10px rgba(255, 107, 53, 0.3));
  }

  .action-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--color-text-primary);
    margin-bottom: 5px;
  }

  .action-subtitle {
    font-size: 0.9rem;
    color: var(--color-text-secondary);
  }

  /* Responsive */
  @media (max-width: 1024px) {
    .nav {
      display: none;
    }
  }

  @media (max-width: 768px) {
    .header-content {
      padding: 15px 20px;
    }

    .welcome-card {
      flex-direction: column;
      text-align: center;
      gap: 20px;
    }

    .stats-grid {
      grid-template-columns: 1fr;
    }

    .actions-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>