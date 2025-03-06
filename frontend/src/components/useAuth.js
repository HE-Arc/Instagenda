import { ref } from 'vue'

const user = ref(null)

export function useAuth() {
  return { user }
}
