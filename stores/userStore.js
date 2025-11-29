/**
 * Store Svelte para gerenciar estado global do usuário
 */

import { writable, derived } from 'svelte/store';
import { progressAPI } from '../lib/api';

// ============================================
// STORES BÁSICAS
// ============================================

/**
 * Informações do usuário
 */
export const user = writable({
  id: null,
  username: null,
  email: null,
  isAuthenticated: false,
});

/**
 * Progresso atual do usuário
 */
export const progress = writable({
  currentMission: 'dax-basics',
  completedLessons: [],
  currentLesson: 1,
  totalXP: 0,
  streakDays: 1,
  lastActivity: null,
});

/**
 * Lição atualmente sendo visualizada
 */
export const currentLesson = writable(null);

/**
 * Missão atualmente selecionada
 */
export const currentMission = writable(null);

/**
 * Loading states
 */
export const loading = writable({
  missions: false,
  lessons: false,
  progress: false,
});

/**
 * Erros
 */
export const errors = writable({
  missions: null,
  lessons: null,
  progress: null,
});

// ============================================
// DERIVED STORES (COMPUTADAS)
// ============================================

/**
 * Calcula nível do usuário baseado no XP
 */
export const userLevel = derived(progress, ($progress) => {
  const xp = $progress.totalXP;
  return Math.floor(xp / 100) + 1;
});

/**
 * Calcula XP necessário para próximo nível
 */
export const xpToNextLevel = derived(progress, ($progress) => {
  const currentLevel = Math.floor($progress.totalXP / 100) + 1;
  const nextLevelXP = currentLevel * 100;
  return nextLevelXP - $progress.totalXP;
});

/**
 * Porcentagem de progresso para próximo nível
 */
export const levelProgress = derived(progress, ($progress) => {
  const xp = $progress.totalXP;
  const currentLevelBase = Math.floor(xp / 100) * 100;
  const xpInCurrentLevel = xp - currentLevelBase;
  return (xpInCurrentLevel / 100) * 100;
});

/**
 * Verifica se usuário tem acesso premium
 */
export const isPremium = derived(user, ($user) => {
  // TODO: Implementar lógica real de verificação de premium
  return $user.isPremium || false;
});

// ============================================
// ACTIONS (FUNÇÕES)
// ============================================

/**
 * Inicializa o usuário (simula login)
 * TODO: Integrar com Supabase auth
 */
export function initUser(userId = 'demo-user') {
  user.set({
    id: userId,
    username: 'DAXVenger',
    email: 'user@daxvengers.com',
    isAuthenticated: true,
  });
  
  // Carrega progresso
  loadUserProgress(userId);
}

/**
 * Carrega progresso do usuário do backend
 */
export async function loadUserProgress(userId, missionId = 'dax-basics') {
  loading.update(l => ({ ...l, progress: true }));
  errors.update(e => ({ ...e, progress: null }));
  
  try {
    const data = await progressAPI.get(userId, missionId);
    progress.set(data);
    loading.update(l => ({ ...l, progress: false }));
  } catch (error) {
    console.error('Erro ao carregar progresso:', error);
    errors.update(e => ({ ...e, progress: error.message }));
    loading.update(l => ({ ...l, progress: false }));
  }
}

/**
 * Salva progresso ao completar uma lição
 */
export async function completeLesson(lessonId, xpEarned) {
  const userId = getUserId();
  
  try {
    const response = await progressAPI.save({
      user_id: userId,
      lesson_id: lessonId,
      xp_earned: xpEarned,
      completed: true,
    });
    
    // Atualiza store local
    progress.update(p => ({
      ...p,
      completedLessons: [...p.completedLessons, lessonId],
      currentLesson: lessonId + 1,
      totalXP: p.totalXP + xpEarned,
      lastActivity: new Date().toISOString(),
    }));
    
    return response;
  } catch (error) {
    console.error('Erro ao salvar progresso:', error);
    throw error;
  }
}

/**
 * Adiciona XP ao usuário
 */
export function addXP(amount) {
  progress.update(p => ({
    ...p,
    totalXP: p.totalXP + amount,
  }));
}

/**
 * Atualiza streak de dias
 */
export function updateStreak() {
  const lastActivity = new Date(getProgress().lastActivity);
  const today = new Date();
  const diffDays = Math.floor((today - lastActivity) / (1000 * 60 * 60 * 24));
  
  progress.update(p => {
    if (diffDays === 0) {
      // Mesmo dia, mantém streak
      return p;
    } else if (diffDays === 1) {
      // Dia consecutivo, aumenta streak
      return { ...p, streakDays: p.streakDays + 1 };
    } else {
      // Perdeu o streak
      return { ...p, streakDays: 1 };
    }
  });
}

/**
 * Reseta progresso (para testes)
 */
export async function resetProgress(missionId = 'dax-basics') {
  const userId = getUserId();
  
  try {
    await progressAPI.reset(userId, missionId);
    
    progress.set({
      currentMission: missionId,
      completedLessons: [],
      currentLesson: 1,
      totalXP: 0,
      streakDays: 1,
      lastActivity: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Erro ao resetar progresso:', error);
    throw error;
  }
}

// ============================================
// HELPERS (GETTERS)
// ============================================

/**
 * Pega ID do usuário atual
 */
function getUserId() {
  let userId;
  user.subscribe(u => userId = u.id)();
  return userId || 'demo-user';
}

/**
 * Pega progresso atual
 */
function getProgress() {
  let currentProgress;
  progress.subscribe(p => currentProgress = p)();
  return currentProgress;
}

/**
 * Verifica se uma lição está completa
 */
export function isLessonCompleted(lessonId) {
  const currentProgress = getProgress();
  return currentProgress.completedLessons.includes(lessonId);
}

/**
 * Verifica se uma lição está desbloqueada
 */
export function isLessonUnlocked(lessonId) {
  if (lessonId === 1) return true;
  return isLessonCompleted(lessonId - 1);
}

// ============================================
// PERSISTÊNCIA LOCAL (localStorage)
// ============================================

/**
 * Salva progresso no localStorage
 */
export function saveToLocalStorage() {
  const currentProgress = getProgress();
  const currentUser = getUserId();
  
  localStorage.setItem('daxvengers_progress', JSON.stringify(currentProgress));
  localStorage.setItem('daxvengers_user', currentUser);
}

/**
 * Carrega progresso do localStorage
 */
export function loadFromLocalStorage() {
  try {
    const savedProgress = localStorage.getItem('daxvengers_progress');
    const savedUser = localStorage.getItem('daxvengers_user');
    
    if (savedProgress) {
      progress.set(JSON.parse(savedProgress));
    }
    
    if (savedUser) {
      initUser(savedUser);
    }
  } catch (error) {
    console.error('Erro ao carregar do localStorage:', error);
  }
}

// Auto-save no localStorage quando progresso muda
progress.subscribe(saveToLocalStorage);