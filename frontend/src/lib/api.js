/**
 * Cliente da API DAXVengers
 * Centraliza todas as chamadas HTTP para o backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Helper para fazer requisições HTTP
 */
async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erro na requisição');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

// ============================================
// API DE MISSÕES
// ============================================

export const missionsAPI = {
  /**
   * Lista todas as missões disponíveis
   */
  getAll: async () => {
    return await request('/api/missions');
  },

  /**
   * Pega uma missão específica
   * @param {string} missionId - ID da missão
   */
  getById: async (missionId) => {
    return await request(`/api/missions/${missionId}`);
  },

  /**
   * Lista todas as lições de uma missão
   * @param {string} missionId - ID da missão
   */
  getLessons: async (missionId) => {
    return await request(`/api/missions/${missionId}/lessons`);
  },
};

// ============================================
// API DE LIÇÕES
// ============================================

export const lessonsAPI = {
  /**
   * Pega uma lição específica com todo o conteúdo
   * @param {number} lessonId - ID da lição
   */
  getById: async (lessonId) => {
    return await request(`/api/lessons/${lessonId}`);
  },

  /**
   * Pega a próxima lição da sequência
   * @param {number} lessonId - ID da lição atual
   * @param {string} missionId - ID da missão
   */
  getNext: async (lessonId, missionId) => {
    return await request(`/api/lessons/${lessonId}/next?mission_id=${missionId}`);
  },
};

// ============================================
// API DE PROGRESSO
// ============================================

export const progressAPI = {
  /**
   * Pega o progresso do usuário em uma missão
   * @param {string} userId - ID do usuário
   * @param {string} missionId - ID da missão
   */
  get: async (userId, missionId = 'dax-basics') => {
    return await request(`/api/progress/${userId}?mission_id=${missionId}`);
  },

  /**
   * Salva progresso ao completar uma lição
   * @param {Object} data - Dados do progresso
   */
  save: async (data) => {
    return await request('/api/progress', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Reseta o progresso do usuário em uma missão
   * @param {string} userId - ID do usuário
   * @param {string} missionId - ID da missão
   */
  reset: async (userId, missionId = 'dax-basics') => {
    return await request(`/api/progress/reset/${userId}?mission_id=${missionId}`, {
      method: 'POST',
    });
  },
};

// ============================================
// API DE LEADERBOARD
// ============================================

export const leaderboardAPI = {
  /**
   * Pega o ranking dos top jogadores
   * @param {number} limit - Número de jogadores
   */
  getTop: async (limit = 10) => {
    return await request(`/api/leaderboard?limit=${limit}`);
  },
};

// ============================================
// API DE HEALTH CHECK
// ============================================

export const healthAPI = {
  /**
   * Verifica se a API está online
   */
  check: async () => {
    return await request('/api/health');
  },
};

// ============================================
// EXPORT DEFAULT COM TODAS AS APIs
// ============================================

export default {
  missions: missionsAPI,
  lessons: lessonsAPI,
  progress: progressAPI,
  leaderboard: leaderboardAPI,
  health: healthAPI,
};