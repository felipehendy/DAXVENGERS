import { writable } from 'svelte/store'
import { supabase } from '../supabaseClient.js'

export const user = writable(null)
export const loading = writable(true)

// Verificar se há usuário logado ao carregar a página
export async function checkUser() {
  loading.set(true)
  
  try {
    const { data: { session } } = await supabase.auth.getSession()
    
    if (session) {
      user.set(session.user)
      console.log('✅ Usuário logado:', session.user)
    } else {
      user.set(null)
    }
  } catch (error) {
    console.error('Erro ao verificar usuário:', error)
    user.set(null)
  } finally {
    loading.set(false)
  }
}

// Escutar mudanças na autenticação
supabase.auth.onAuthStateChange((event, session) => {
  console.log('Auth event:', event)
  
  if (session) {
    user.set(session.user)
  } else {
    user.set(null)
  }
})

// Função de logout
export async function logout() {
  await supabase.auth.signOut()
  user.set(null)
}