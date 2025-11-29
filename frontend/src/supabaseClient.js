import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://nkutkbbprklquhkimhwu.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rdXRrYmJwcmtscXVoa2ltaHd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQzMDUyNjAsImV4cCI6MjA3OTg4MTI2MH0.muSz7gIUrNCBUi2OkyYN5Tmh6Lrs6c28HHMRCHgLecg'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)