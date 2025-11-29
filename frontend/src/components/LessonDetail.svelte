<script>
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';
  import ExerciseCard from './ExerciseCard.svelte';
  
  const dispatch = createEventDispatcher();

  // Props
  export let lessonId;

  // State
  let lesson = null;
  let loading = true;
  let currentExerciseIndex = 0;
  let lessonCompleted = false;

  // Fetch lesson details
  onMount(async () => {
    try {
      const response = await fetch(`/api/lessons/${lessonId}`);
      lesson = await response.json();
      loading = false;
    } catch (error) {
      console.error('Erro ao carregar lição:', error);
      loading = false;
    }
  });

  // Handle exercise completion
  function handleExerciseComplete(event) {
    const earnedXP = event.detail.xp;
    
    // Move to next exercise or complete lesson
    if (currentExerciseIndex < lesson.exercises.length - 1) {
      setTimeout(() => {
        currentExerciseIndex++;
      }, 1500);
    } else {
      setTimeout(() => {
        completeLesson(earnedXP);
      }, 1500);
    }
  }

  // Complete lesson
  async function completeLesson(xp) {
    lessonCompleted = true;
    
    // Save progress to backend
    try {
      await fetch('/api/progress', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lessonId: lesson.id,
          xpEarned: xp,
          completed: true
        })
      });

      // Dispatch event to parent
      dispatch('lessonCompleted', {
        lessonId: lesson.id,
        xp: xp
      });
    } catch (error) {
      console.error('Erro ao salvar progresso:', error);
    }
  }

  // Go back
  function goBack() {
    dispatch('back');
  }
</script>

<div class="lesson-detail-container">
  {#if loading}
    <div class="loading">
      <div class="spinner"></div>
      <p>Carregando lição...</p>
    </div>
  {:else if lesson}
    <!-- Header -->
    <div class="lesson-header">
      <button class="back-btn" on:click={goBack}>
        ←
      </button>
      <h2 class="lesson-title-header">{lesson.title}</h2>
      <div style="width: 40px;"></div>
    </div>

    <!-- Lesson Introduction -->
    {#if currentExerciseIndex === 0 && !lessonCompleted}
      <div class="lesson-intro">
        <div class="lesson-icon">{lesson.icon}</div>
        <h1 class="lesson-name">{lesson.title}</h1>
        <p class="lesson-reward">Complete para ganhar {lesson.xp} XP!</p>
      </div>
    {/if}

    <!-- Theory Section -->
    <div class="theory-section">
      <h3>📚 {lesson.theoryTitle || 'O que você vai aprender'}</h3>
      <div class="theory-content">
        {@html lesson.theory}
      </div>
    </div>

    <!-- Exercises -->
    {#if !lessonCompleted}
      <div class="exercises-section">
        <div class="exercise-progress">
          <span>Exercício {currentExerciseIndex + 1} de {lesson.exercises.length}</span>
          <div class="progress-dots">
            {#each lesson.exercises as _, index}
              <span class="dot" class:active={index === currentExerciseIndex} class:completed={index < currentExerciseIndex}></span>
            {/each}
          </div>
        </div>

        <ExerciseCard 
          exercise={lesson.exercises[currentExerciseIndex]}
          lessonXP={lesson.xp}
          on:exerciseComplete={handleExerciseComplete}
        />
      </div>
    {:else}
      <!-- Completion Screen -->
      <div class="completion-screen">
        <div class="completion-animation">🎉</div>
        <h2>Lição Completa!</h2>
        <div class="xp-earned">+{lesson.xp} XP</div>
        <p class="completion-message">
          Parabéns, Vingador! Você dominou {lesson.title}!
        </p>
        <button class="btn-continue" on:click={goBack}>
          Continuar Jornada →
        </button>
      </div>
    {/if}
  {:else}
    <div class="error">
      <p>❌ Erro ao carregar lição</p>
      <button class="btn-back" on:click={goBack}>Voltar</button>
    </div>
  {/if}
</div>

<style>
  .lesson-detail-container {
    max-width: 600px;
    margin: 0 auto;
    min-height: 100vh;
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #2d1b3d 100%);
    color: #fff;
    padding-bottom: 40px;
  }

  /* Loading */
  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    color: rgba(255, 255, 255, 0.7);
  }

  .spinner {
    width: 50px;
    height: 50px;
    border: 4px solid rgba(255, 152, 0, 0.3);
    border-top: 4px solid #ff9800;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Header */
  .lesson-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px;
    background: rgba(10, 14, 39, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255, 87, 34, 0.2);
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .back-btn {
    background: rgba(255, 87, 34, 0.2);
    border: 1px solid rgba(255, 87, 34, 0.4);
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    font-size: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }

  .back-btn:hover {
    background: rgba(255, 87, 34, 0.3);
    transform: translateX(-2px);
  }

  .lesson-title-header {
    font-size: 18px;
    font-weight: bold;
  }

  /* Lesson Introduction */
  .lesson-intro {
    text-align: center;
    padding: 40px 20px;
    animation: fadeIn 0.5s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .lesson-icon {
    font-size: 80px;
    margin-bottom: 20px;
  }

  .lesson-name {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 12px;
  }

  .lesson-reward {
    font-size: 16px;
    color: #ffc107;
    font-weight: bold;
  }

  /* Theory Section */
  .theory-section {
    background: rgba(255, 87, 34, 0.1);
    border-left: 4px solid #ff5722;
    padding: 25px;
    margin: 20px;
    border-radius: 12px;
    animation: fadeIn 0.5s ease 0.2s both;
  }

  .theory-section h3 {
    color: #ff9800;
    font-size: 20px;
    margin-bottom: 15px;
  }

  .theory-content {
    line-height: 1.7;
    color: rgba(255, 255, 255, 0.9);
  }

  .theory-content :global(p) {
    margin-bottom: 15px;
  }

  .theory-content :global(strong) {
    color: #ffc107;
  }

  .theory-content :global(code) {
    background: rgba(0, 0, 0, 0.3);
    padding: 2px 8px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    color: #4caf50;
  }

  .theory-content :global(pre) {
    background: #1e1e1e;
    padding: 15px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 15px 0;
    border: 1px solid rgba(255, 152, 0, 0.3);
  }

  /* Exercises Section */
  .exercises-section {
    padding: 20px;
    animation: fadeIn 0.5s ease 0.4s both;
  }

  .exercise-progress {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
  }

  .progress-dots {
    display: flex;
    gap: 8px;
  }

  .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
  }

  .dot.active {
    background: #ff9800;
    transform: scale(1.3);
  }

  .dot.completed {
    background: #4caf50;
  }

  /* Completion Screen */
  .completion-screen {
    text-align: center;
    padding: 60px 20px;
    animation: fadeIn 0.5s ease;
  }

  .completion-animation {
    font-size: 100px;
    animation: bounce 1s ease infinite;
    margin-bottom: 20px;
  }

  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-20px); }
  }

  .completion-screen h2 {
    font-size: 32px;
    margin-bottom: 20px;
  }

  .xp-earned {
    display: inline-block;
    background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
    color: #000;
    padding: 15px 40px;
    border-radius: 25px;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
  }

  .completion-message {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 30px;
    line-height: 1.6;
  }

  .btn-continue {
    background: linear-gradient(135deg, #ff5722 0%, #ff9800 100%);
    color: white;
    border: none;
    padding: 15px 40px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(255, 87, 34, 0.4);
  }

  .btn-continue:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 87, 34, 0.6);
  }

  /* Error */
  .error {
    text-align: center;
    padding: 60px 20px;
  }

  .error p {
    font-size: 18px;
    margin-bottom: 20px;
  }

  .btn-back {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.3);
    padding: 12px 30px;
    border-radius: 10px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .btn-back:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  /* Responsive */
  @media (max-width: 600px) {
    .lesson-icon {
      font-size: 60px;
    }

    .lesson-name {
      font-size: 24px;
    }

    .completion-animation {
      font-size: 80px;
    }

    .xp-earned {
      font-size: 24px;
      padding: 12px 30px;
    }
  }
</style>