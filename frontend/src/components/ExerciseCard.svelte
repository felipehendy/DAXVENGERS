<script>
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();

  // Props
  export let exercise;
  export let lessonXP = 50;

  // State
  let selectedOption = -1;
  let userCode = '';
  let showFeedback = false;
  let isCorrect = false;
  let feedbackMessage = '';
  let hintIndex = 0;
  let showHint = false;
  let submitted = false;

  // Select option (for multiple choice)
  function selectOption(index) {
    if (submitted) return;
    selectedOption = index;
  }

  // Check answer
  function checkAnswer() {
    if (submitted) return;
    submitted = true;

    if (exercise.type === 'multiple_choice') {
      isCorrect = selectedOption === exercise.correct;
      feedbackMessage = isCorrect ? exercise.explanation : `❌ Tente novamente! ${exercise.explanation}`;
    } else if (exercise.type === 'code') {
      const normalizedUser = userCode.trim().replace(/\s+/g, '').toUpperCase();
      const normalizedSolution = exercise.solution.replace(/\s+/g, '').toUpperCase();
      
      isCorrect = normalizedUser === normalizedSolution || normalizedUser.includes(normalizedSolution);
      feedbackMessage = isCorrect 
        ? '✅ Código perfeito! Você dominou essa função! 🎉'
        : '❌ Quase lá! Confira a sintaxe e tente novamente.';
    }

    showFeedback = true;

    if (isCorrect) {
      setTimeout(() => {
        dispatch('exerciseComplete', { xp: lessonXP });
      }, 2000);
    } else {
      setTimeout(() => {
        showFeedback = false;
        submitted = false;
        if (exercise.type === 'multiple_choice') {
          selectedOption = -1;
        }
      }, 3000);
    }
  }

  // Show next hint
  function revealHint() {
    if (hintIndex < exercise.hints.length) {
      showHint = true;
      hintIndex++;
    }
  }

  // Get button text
  function getButtonText() {
    if (exercise.type === 'multiple_choice') {
      return selectedOption === -1 ? 'Selecione uma opção' : 'Verificar Resposta';
    }
    return 'Verificar Código';
  }

  // Check if can submit
  function canSubmit() {
    if (submitted) return false;
    if (exercise.type === 'multiple_choice') return selectedOption !== -1;
    if (exercise.type === 'code') return userCode.trim().length > 0;
    return false;
  }
</script>

<div class="exercise-card">
  <!-- Question -->
  <div class="question-section">
    <h4 class="question-icon">
      {#if exercise.type === 'multiple_choice'}
        ❓
      {:else if exercise.type === 'code'}
        💻
      {:else}
        🎯
      {/if}
    </h4>
    <p class="question-text">{exercise.question}</p>
  </div>

  <!-- Multiple Choice -->
  {#if exercise.type === 'multiple_choice'}
    <div class="options-container">
      {#each exercise.options as option, index}
        <button
          class="option"
          class:selected={selectedOption === index && !submitted}
          class:correct={submitted && isCorrect && selectedOption === index}
          class:wrong={submitted && !isCorrect && selectedOption === index}
          on:click={() => selectOption(index)}
          disabled={submitted}
        >
          <span class="option-letter">{String.fromCharCode(65 + index)}</span>
          <span class="option-text">{option}</span>
        </button>
      {/each}
    </div>
  {/if}

  <!-- Code Exercise -->
  {#if exercise.type === 'code'}
    <div class="code-section">
      <textarea
        class="code-input"
        bind:value={userCode}
        placeholder="Digite seu código DAX aqui..."
        disabled={submitted && isCorrect}
      ></textarea>

      <!-- Hints -->
      {#if exercise.hints && exercise.hints.length > 0}
        <button class="hint-btn" on:click={revealHint} disabled={hintIndex >= exercise.hints.length}>
          💡 {hintIndex >= exercise.hints.length ? 'Todas as dicas usadas' : 'Preciso de uma Dica'}
        </button>

        {#if showHint && hintIndex > 0}
          <div class="hint-box">
            <strong>💡 Dica {hintIndex}:</strong> {exercise.hints[hintIndex - 1]}
          </div>
        {/if}
      {/if}
    </div>
  {/if}

  <!-- Feedback -->
  {#if showFeedback}
    <div class="feedback" class:correct={isCorrect} class:wrong={!isCorrect}>
      <p class="feedback-text">{feedbackMessage}</p>
      {#if isCorrect}
        <div class="xp-badge">+{lessonXP} XP</div>
      {/if}
    </div>
  {/if}

  <!-- Submit Button -->
  <button
    class="btn-submit"
    on:click={checkAnswer}
    disabled={!canSubmit()}
  >
    {getButtonText()}
  </button>
</div>

<style>
  .exercise-card {
    background: rgba(26, 31, 58, 0.8);
    border: 2px solid rgba(255, 152, 0, 0.3);
    border-radius: 15px;
    padding: 25px;
    animation: fadeIn 0.5s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* Question */
  .question-section {
    margin-bottom: 25px;
  }

  .question-icon {
    font-size: 32px;
    margin-bottom: 12px;
  }

  .question-text {
    font-size: 16px;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.95);
  }

  /* Options (Multiple Choice) */
  .options-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 20px;
  }

  .option {
    display: flex;
    align-items: center;
    gap: 15px;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.2);
    padding: 15px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
    width: 100%;
  }

  .option:hover:not(:disabled) {
    border-color: #ff9800;
    background: rgba(255, 152, 0, 0.1);
    transform: translateX(3px);
  }

  .option.selected {
    border-color: #ff9800;
    background: rgba(255, 152, 0, 0.2);
  }

  .option.correct {
    border-color: #4caf50;
    background: rgba(76, 175, 80, 0.2);
  }

  .option.wrong {
    border-color: #f44336;
    background: rgba(244, 67, 54, 0.2);
  }

  .option:disabled {
    cursor: not-allowed;
  }

  .option-letter {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 32px;
    height: 32px;
    background: rgba(255, 152, 0, 0.3);
    border-radius: 50%;
    font-weight: bold;
    font-size: 14px;
  }

  .option.correct .option-letter {
    background: rgba(76, 175, 80, 0.5);
  }

  .option.wrong .option-letter {
    background: rgba(244, 67, 54, 0.5);
  }

  .option-text {
    flex: 1;
    font-size: 15px;
  }

  /* Code Section */
  .code-section {
    margin-bottom: 20px;
  }

  .code-input {
    width: 100%;
    background: #1e1e1e;
    color: #d4d4d4;
    border: 2px solid rgba(255, 152, 0, 0.3);
    padding: 15px;
    border-radius: 10px;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    min-height: 120px;
    resize: vertical;
    margin-bottom: 15px;
  }

  .code-input:focus {
    outline: none;
    border-color: #ff9800;
    box-shadow: 0 0 10px rgba(255, 152, 0, 0.3);
  }

  .code-input:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  /* Hints */
  .hint-btn {
    background: rgba(255, 193, 7, 0.2);
    border: 2px solid rgba(255, 193, 7, 0.4);
    color: #ffc107;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    transition: all 0.3s ease;
    width: 100%;
    margin-bottom: 15px;
  }

  .hint-btn:hover:not(:disabled) {
    background: rgba(255, 193, 7, 0.3);
    transform: translateY(-2px);
  }

  .hint-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .hint-box {
    background: rgba(255, 193, 7, 0.1);
    border-left: 4px solid #ffc107;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    animation: slideIn 0.3s ease;
    font-size: 14px;
    line-height: 1.6;
  }

  @keyframes slideIn {
    from { opacity: 0; transform: translateX(-10px); }
    to { opacity: 1; transform: translateX(0); }
  }

  /* Feedback */
  .feedback {
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    animation: slideIn 0.3s ease;
  }

  .feedback.correct {
    background: rgba(76, 175, 80, 0.2);
    border: 2px solid #4caf50;
  }

  .feedback.wrong {
    background: rgba(244, 67, 54, 0.2);
    border: 2px solid #f44336;
  }

  .feedback-text {
    margin-bottom: 10px;
    line-height: 1.6;
  }

  .xp-badge {
    display: inline-block;
    background: linear-gradient(135deg, #ffd700 0%, #ff9800 100%);
    color: #000;
    padding: 8px 20px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 16px;
    box-shadow: 0 2px 10px rgba(255, 215, 0, 0.4);
  }

  /* Submit Button */
  .btn-submit {
    width: 100%;
    background: linear-gradient(135deg, #ff5722 0%, #ff9800 100%);
    color: white;
    border: none;
    padding: 16px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(255, 87, 34, 0.4);
  }

  .btn-submit:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 87, 34, 0.6);
  }

  .btn-submit:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  .btn-submit:active:not(:disabled) {
    transform: scale(0.98);
  }

  /* Responsive */
  @media (max-width: 600px) {
    .exercise-card {
      padding: 20px;
    }

    .question-icon {
      font-size: 28px;
    }

    .question-text {
      font-size: 15px;
    }

    .option {
      padding: 12px;
    }

    .code-input {
      font-size: 13px;
      min-height: 100px;
    }
  }
</style>