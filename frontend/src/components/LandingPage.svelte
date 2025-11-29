<script>
  export let onLogin = () => {}
  export let onRegister = () => {}
</script>

<div class="landing">
  <!-- Hero Section -->
  <section class="hero">
    <div class="hero-content">
      <div class="hero-badge">
        <span class="badge-icon">⚡</span>
        <span>Versão Beta</span>
      </div>
      
      <h1 class="hero-title">
        <span class="gradient-text">DAXVengers</span>
      </h1>
      
      <p class="hero-subtitle">
        Domine Power BI e DAX como um super-herói. Aprenda, pratique e conquiste badges épicos.
      </p>
      
      <div class="hero-buttons">
        <button class="btn-primary" on:click={onRegister}>
          <span class="btn-icon">🚀</span>
          Começar Jornada
        </button>
        <button class="btn-secondary" on:click={onLogin}>
          Ver Demo
        </button>
      </div>

      <!-- Stats -->
      <div class="stats">
        <div class="stat-item">
          <div class="stat-value">50+</div>
          <div class="stat-label">Missões DAX</div>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <div class="stat-value">15</div>
          <div class="stat-label">Badges Épicos</div>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <div class="stat-value">1K+</div>
          <div class="stat-label">Vingadores</div>
        </div>
      </div>
    </div>

    <!-- Animated Background -->
    <div class="hero-bg">
      <div class="bg-circle circle-1"></div>
      <div class="bg-circle circle-2"></div>
      <div class="bg-circle circle-3"></div>
    </div>
  </section>
</div>

<style>
  .landing {
    min-height: 100vh;
    background: var(--color-bg-darker);
    position: relative;
    overflow: hidden;
  }

  .hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    position: relative;
    z-index: 1;
  }

  .hero-content {
    max-width: 800px;
    text-align: center;
    position: relative;
    z-index: 2;
  }

  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 107, 53, 0.1);
    border: 1px solid rgba(255, 107, 53, 0.3);
    border-radius: 50px;
    padding: 8px 20px;
    margin-bottom: 30px;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--color-primary);
    animation: float 3s ease-in-out infinite;
  }

  .badge-icon {
    font-size: 1.2rem;
    animation: pulse 2s ease-in-out infinite;
  }

  .hero-title {
    font-size: clamp(3rem, 10vw, 6rem);
    font-weight: 900;
    margin: 0 0 20px 0;
    line-height: 1.1;
    letter-spacing: -2px;
  }

  .gradient-text {
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 50%, var(--color-accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 60px rgba(255, 107, 53, 0.3);
    animation: gradient-shift 5s ease infinite;
    background-size: 200% 200%;
  }

  @keyframes gradient-shift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
  }

  .hero-subtitle {
    font-size: clamp(1.1rem, 3vw, 1.5rem);
    color: var(--color-text-secondary);
    margin: 0 0 40px 0;
    line-height: 1.6;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  .hero-buttons {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 60px;
  }

  .btn-primary, .btn-secondary {
    padding: 16px 40px;
    border-radius: 12px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s;
    border: none;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .btn-primary {
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    color: white;
    box-shadow: 0 10px 30px rgba(255, 107, 53, 0.4);
  }

  .btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(255, 107, 53, 0.6);
  }

  .btn-secondary {
    background: transparent;
    color: var(--color-text-primary);
    border: 2px solid rgba(255, 255, 255, 0.2);
  }

  .btn-secondary:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.4);
    transform: translateY(-3px);
  }

  .btn-icon {
    font-size: 1.5rem;
  }

  /* Stats */
  .stats {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 40px;
    flex-wrap: wrap;
  }

  .stat-item {
    text-align: center;
  }

  .stat-value {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 5px;
  }

  .stat-label {
    font-size: 0.9rem;
    color: var(--color-text-muted);
    font-weight: 600;
  }

  .stat-divider {
    width: 2px;
    height: 40px;
    background: rgba(255, 255, 255, 0.1);
  }

  /* Animated Background */
  .hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    overflow: hidden;
    z-index: 0;
  }

  .bg-circle {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.2;
    animation: float-circle 20s ease-in-out infinite;
  }

  .circle-1 {
    width: 500px;
    height: 500px;
    background: var(--color-primary);
    top: -250px;
    left: -250px;
    animation-delay: 0s;
  }

  .circle-2 {
    width: 400px;
    height: 400px;
    background: var(--color-secondary);
    bottom: -200px;
    right: -200px;
    animation-delay: 5s;
  }

  .circle-3 {
    width: 300px;
    height: 300px;
    background: var(--color-accent);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation-delay: 10s;
  }

  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
  }

  @keyframes float-circle {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(50px, -50px) scale(1.1); }
    66% { transform: translate(-50px, 50px) scale(0.9); }
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }

  /* Responsive */
  @media (max-width: 768px) {
    .hero-buttons {
      flex-direction: column;
      width: 100%;
    }

    .btn-primary, .btn-secondary {
      width: 100%;
      justify-content: center;
    }

    .stats {
      gap: 20px;
    }

    .stat-divider {
      display: none;
    }
  }
</style>