import { ref } from 'vue'

const user = ref(null)

export function useAuth() {
  return { user }
}

const errorMessage = ref("")
export function useErrorMessage() {
  return { errorMessage }
}

const message = ref("")
export function userMessage() {
  return { message }
}
