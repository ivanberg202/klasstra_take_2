<!-- filename: vue_js_project/src/components/AddChild.vue -->
<template>
    <div class="mt-8 p-4 border rounded bg-white dark:bg-gray-800">
      <h2 class="text-xl font-bold mb-4">Add a Child</h2>
      <form @submit.prevent="handleSubmit">
        <div class="mb-2">
          <input
            v-model="firstName"
            placeholder="Child's First Name"
            class="w-full p-2 border rounded mb-2 bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
            required
          />
        </div>
        <div class="mb-2">
          <input
            v-model="lastName"
            placeholder="Child's Last Name"
            class="w-full p-2 border rounded mb-2 bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
            required
          />
        </div>
        <div class="mb-4">
          <select
            v-model="selectedClassId"
            class="w-full p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
            required
          >
            <option disabled value="">Select a class</option>
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">
              {{ cls.name }}
            </option>
          </select>
        </div>
        <button
          type="submit"
          :disabled="isSubmitting"
          class="bg-primary text-white px-4 py-2 rounded w-full disabled:opacity-50"
        >
          {{ isSubmitting ? 'Adding...' : 'Add Child' }}
        </button>
      </form>
  
      <!-- Display Success or Error Messages -->
      <div v-if="successMessage" class="mt-4 text-green-500">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="mt-4 text-red-500">
        {{ errorMessage }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { useStore } from 'vuex'
  import { useToast } from 'vue-toastification'
  
  const emit = defineEmits(['childAdded'])
  
  const store = useStore()
  const toast = useToast()
  
  const firstName = ref('')
  const lastName = ref('')
  const selectedClassId = ref('')
  const classes = ref([])
  
  const isSubmitting = ref(false)
  const successMessage = ref('')
  const errorMessage = ref('')
  
  // Fetch classes when component is mounted
  const fetchClasses = async () => {
    try {
      const res = await axios.get('/classes', {
        headers: {
          Authorization: `Bearer ${store.state.token}`
        }
      })
      classes.value = res.data
    } catch (err) {
      console.error('Error fetching classes:', err)
      errorMessage.value = 'Failed to load classes. Please try again later.'
      toast.error('Failed to load classes.')
    }
  }
  
  onMounted(() => {
    fetchClasses()
  })
  
  const handleSubmit = async () => {
    // Reset messages
    successMessage.value = ''
    errorMessage.value = ''
  
    // Simple front-end validation
    if (!firstName.value || !lastName.value || !selectedClassId.value) {
      errorMessage.value = 'All fields are required.'
      toast.error('All fields are required.')
      return
    }
  
    isSubmitting.value = true
  
    try {
      // Fetch the logged-in parent data
      const me = await axios.get('/users/me', {
        headers: { Authorization: `Bearer ${store.state.token}` }
      })
  
      // Send a POST request to add the child
      const res = await axios.post(
        '/children',
        {
          parent_id: me.data.id,
          first_name: firstName.value,
          last_name: lastName.value,
          class_id: selectedClassId.value
        },
        {
          headers: { Authorization: `Bearer ${store.state.token}` }
        }
      )
  
      // Clear form
      firstName.value = ''
      lastName.value = ''
      selectedClassId.value = ''
  
      successMessage.value = 'Child added successfully!'
      toast.success('Child added successfully!')
  
      emit('childAdded', res.data) // Notify parent component if needed
    } catch (err) {
      console.error('Error adding child:', err)
      if (err.response && err.response.data && err.response.data.detail) {
        errorMessage.value = err.response.data.detail
        toast.error(err.response.data.detail)
      } else {
        errorMessage.value = 'Failed to add child. Please try again.'
        toast.error('Failed to add child. Please try again.')
      }
    } finally {
      isSubmitting.value = false
    }
  }
  </script>
  
  <style scoped>
  /* Add any component-specific styles here */
  </style>
  