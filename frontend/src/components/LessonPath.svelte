<script>
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();

  // Props
  export let missionId = 'dax-basics';
  export let userProgress = { completedLessons: [], currentLesson: 1, totalXP: 0 };

  // State
  let lessons = [];
  let loading = true;

  // Fetch lessons from API
  onMount(async () => {
    try {
      const response = await fetch(`/api/missions/${missionId}/lessons`);
      lessons = await response.json();
      loading = false;
    } catch (error) {
      console.error('Erro ao carregar lições:', error);
      loading = false;
    }
  });

  // Check if lesson is unlocked
  function isUnlocked(lessonId) {
    if (lessonId === 1) return true;
    return userProgress.completedLessons.includes(lessonId - 1);
  }

  // Check if lesson is completed
  function isCompleted(lessonId) {
    return userProgress.completedLessons.includes(lessonId);
  }

  // Check if lesson is current
  function isCurrent(lessonId) {
    return lessonId === userProgress.currentLesson;
  }

  // Handle lesson click
  function handleLessonClick(lesson) {
    if (isUnlocked(lesson.id)) {
      dispatch('lessonSelected', lesson);
    }
  }

  // Get lesson status class
  function getLessonClass(lesson) {
    if (isCompleted(lesson.id)) return 'completed';
    if (isCurrent(lesson.id)) return 'current';
    if (isUnlocked(lesson.id)) return 'unlocked';
    return 'locked';
  }
</script>

<div class="lesson-path-container">
  <!-- Header -->
  <div class="path-header">
    <h2 class="mission-title">🦾 Missão: Funções Básicas DAX</h2>
    <p class="mission-progress">
      {userProgress.completedLessons.length}/{lessons.length} lições completas
    </p>
  </div>

  {#if loading}
    <div class="loading">
      <div class="spinner"></div>
      <p>Carregando missão...</p>
    </div>
  {:else}
    <!-- Lesson Path -->
    <div class="path-scroll">
      <div class="path-line"></div>
      
      {#each lessons as lesson, index}
        <div class="lesson-node" class:offset-left={index % 3 === 1} class:offset-right={index % 3 === 2}>
          <!-- Lesson Circle -->
          <button
            class="lesson-circle {getLessonClass(lesson)}"
            on:click={() => handleLessonClick(lesson)}
            disabled={!isUnlocked(lesson.id)}
            class:boss={lesson.type === 'boss'}
          >
            {#if isCompleted(lesson.id)}
              <span class="icon">✓</span>
            {:else if isUnlocked(lesson.id)}
              <span class="icon">{lesson.icon}</span>
            {:else}
              <span class="icon">🔒</span>
            {/if}
          </button>

          <!-- Lesson Info -->
          <div class="lesson-info">
            <h3 class="lesson-title">{lesson.title}</h3>
            <p class="lesson-xp">+{lesson.xp} XP</p>
            {#if lesson.type === 'boss'}
              <span class="boss-badge">BOSS CHALLENGE</span>
            {/if}
          </div>
        </div>

        <!-- Checkpoint every 3 lessons -->
        {#if (index + 1) % 3 === 0 && index < lessons.length - 1}
          <div class="checkpoint">
            <div class="checkpoint-icon">⚡</div>
            <h3>Checkpoint {Math.floor((index + 1) / 3)}</h3>
            <p>Ótimo progresso, Vingador!</p>
          </div>
        {/if}
      {/each}
    </div>
  {/if}
</div>

<style>
  .lesson-path-container {
    max-width: 480px;
    margin: 0 auto;
    padding: 20px;
    padding-bottom: 100px;
  }

  /* Header */
  .path-header {
    text-align: center;
    margin-bottom: 40px;
  }

  .mission-title {
    font-size: 24px;
    font-weight: bold;
    color: #fff;
    margin-bottom: 8px;
  }

  .mission-progress {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
  }

  /* Loading */
  .loading {
    text-align: center;
    padding: 60px 20px;
    color: rgba(255, 255, 255, 0.7);
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 152, 0, 0.3);
    border-top: 3px solid #ff9800;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Path */
  .path-scroll {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 50px;
  }

  .path-line {
    position: absolute;
    width: 3px;
    height: 100%;
    background: linear-gradient(180deg, 
      rgba(255, 87, 34, 0.5) 0%, 
      rgba(255, 87, 34, 0.2) 50%,
      rgba(255, 87, 34, 0.1) 100%);
    left: 50%;
    transform: translateX(-50%);
    z-index: 0;
  }

  /* Lesson Node */
  .lesson-node {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    animation: fadeIn 0.5s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .lesson-node.offset-left {
    align-self: flex-start;
    margin-left: 20%;
  }

  .lesson-node.offset-right {
    align-self: flex-end;
    margin-right: 20%;
  }

  /* Lesson Circle */
  .lesson-circle {
    width: 90px;
    height: 90px;
    border-radius: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
  }

  .lesson-circle .icon {
    font-size: 40px;
  }

  .lesson-circle.completed {
    background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
    border: 3px solid #81c784;
    box-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
  }

  .lesson-circle.current {
    background: linear-gradient(135deg, #ff5722 0%, #ff9800 100%);
    border: 3px solid #ffc107;
    box-shadow: 0 0 30px rgba(255, 87, 34, 0.8);
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { box-shadow: 0 0 20px rgba(255, 87, 34, 0.5); }
    50% { box-shadow: 0 0 40px rgba(255, 152, 0, 1); }
  }

  .lesson-circle.unlocked {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: 3px solid #a78bfa;
    box-shadow: 0 0 15px rgba(167, 139, 250, 0.4);
  }

  .lesson-circle.locked {
    background: rgba(45, 53, 97, 0.6);
    border: 3px solid rgba(255, 255, 255, 0.2);
    cursor: not-allowed;
    opacity: 0.6;
  }

  .lesson-circle.boss {
    width: 110px;
    height: 110px;
    border-radius: 28px;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border: 4px solid #ffd700;
    box-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
  }

  .lesson-circle.boss .icon {
    font-size: 50px;
  }

  .lesson-circle:not(.locked):active {
    transform: scale(0.95);
  }

  .lesson-circle:not(.locked):hover {
    transform: translateY(-3px);
    filter: brightness(1.1);
  }

  /* Lesson Info */
  .lesson-info {
    text-align: center;
    margin-top: 12px;
    max-width: 200px;
  }

  .lesson-title {
    font-size: 14px;
    font-weight: bold;
    color: #fff;
    margin-bottom: 4px;
  }

  .lesson-xp {
    font-size: 12px;
    color: #ffc107;
  }

  .boss-badge {
    display: inline-block;
    background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
    color: #000;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 10px;
    font-weight: bold;
    margin-top: 8px;
  }

  /* Checkpoint */
  .checkpoint {
    background: linear-gradient(135deg, rgba(255, 152, 0, 0.2) 0%, rgba(255, 87, 34, 0.2) 100%);
    border: 2px solid rgba(255, 152, 0, 0.5);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    width: 90%;
    margin: 20px 0;
    animation: fadeIn 0.5s ease;
  }

  .checkpoint-icon {
    font-size: 32px;
    margin-bottom: 10px;
  }

  .checkpoint h3 {
    font-size: 16px;
    color: #fff;
    margin-bottom: 5px;
  }

  .checkpoint p {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
  }

  /* Responsive */
  @media (max-width: 480px) {
    .lesson-circle {
      width: 80px;
      height: 80px;
    }

    .lesson-circle .icon {
      font-size: 35px;
    }

    .lesson-circle.boss {
      width: 100px;
      height: 100px;
    }
  }
</style>