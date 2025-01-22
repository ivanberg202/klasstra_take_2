<!-- filename: src/components/AIAnnouncementForm.vue -->
<template>
    <div class="max-w-2xl my-6 p-4 border rounded bg-white dark:bg-gray-800 text-left">
      <h1 class="text-xl font-bold mb-4 text-gray-900 dark:text-gray-100">AI Assistant</h1>
  
      <!-- 1) Recipient Selection -->
      <div class="mb-4">
        <label class="block font-semibold">Select Recipients</label>
        <div class="flex space-x-4 mt-2">
          <label class="flex items-center space-x-2">
            <input type="checkbox" v-model="recipientOptions.classes" /> 
            <span>Classes</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="checkbox" v-model="recipientOptions.parents" />
            <span>Parents</span>
          </label>
        </div>
      </div>
  
      <div v-if="recipientOptions.classes" class="mb-4">
        <label class="block text-sm font-medium">Choose Classes</label>
        <select v-model="selectedClasses" multiple class="w-full p-2 border rounded dark:bg-gray-700 dark:text-white">
          <option v-for="cls in classes" :key="cls.id" :value="cls.id">
            {{ cls.name }}
          </option>
        </select>
      </div>
  
      <div v-if="recipientOptions.parents" class="mb-4">
        <label class="block text-sm font-medium">Choose Parents</label>
        <select v-model="selectedParents" multiple class="w-full p-2 border rounded dark:bg-gray-700 dark:text-white">
          <option v-for="p in parents" :key="p.id" :value="p.id">
            {{ p.first_name }} {{ p.last_name }}
          </option>
        </select>
      </div>
  
      <!-- 2) AI Input -->
      <form @submit.prevent="handleGenerate" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Your Text</label>
          <textarea
            v-model="inputText"
            rows="5"
            class="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
            placeholder="Unstructured text here..."
          ></textarea>
        </div>
        <button
          type="submit"
          :disabled="loadingGenerate"
          class="bg-primary text-white px-4 py-2 rounded w-full disabled:opacity-50"
        >
          {{ loadingGenerate ? "Generating..." : "Generate AI Text" }}
        </button>
      </form>
  
      <!-- 3) AI Output + Final Submit -->
      <div v-if="responseText" class="mt-4">
        <label class="font-bold mb-2 block">AI-Generated Announcement</label>
        <textarea
          v-model="responseText"
          rows="12"
          class="w-full p-2 border rounded bg-gray-100 dark:bg-gray-900 dark:text-white"
          style="white-space: pre-wrap; resize: vertical;"
        ></textarea>
  
        <button
          @click="submitAnnouncement"
          :disabled="loadingSubmit"
          class="mt-4 bg-secondary text-white px-4 py-2 rounded w-full disabled:opacity-50"
        >
          {{ loadingSubmit ? "Submitting..." : "Submit the announcement" }}
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from '../plugins/axios.js'
  import { useStore } from 'vuex'
  import { useToast } from 'vue-toastification'
  
  const store = useStore()
  const toast = useToast()
  const emit = defineEmits(['announcementCreated'])
  
  // Recipients
  const classes = ref([])
  const parents = ref([])
  const recipientOptions = ref({ classes: false, parents: false })
  const selectedClasses = ref([])
  const selectedParents = ref([])
  
  // AI Input/Output
  const inputText = ref('')
  const responseText = ref('')
  const loadingGenerate = ref(false)
  const loadingSubmit = ref(false)
  
  /* 1) Fetch Classes & Parents on mount */
  onMounted(async () => {
    try {
      // Classes: /teacher/my-classes
      const clsRes = await axios.get('/teacher/my-classes', {
        headers: { Authorization: `Bearer ${store.state.token}` },
      })
      classes.value = clsRes.data
  
      // Parents: /announcements/teacher/parents
      const parRes = await axios.get('/announcements/teacher/parents', {
        headers: { Authorization: `Bearer ${store.state.token}` },
      })
      parents.value = parRes.data
    } catch (err) {
      console.error('Error loading recipients:', err)
      toast.error('Failed to load recipients.')
    }
  })
  
  /* 2) Generate AI Text */
  async function handleGenerate() {
    if (!inputText.value.trim()) {
      toast.error('Please enter some text to transform.')
      return
    }
    loadingGenerate.value = true
    responseText.value = ''
    try {
      const res = await axios.post('/ai/generate',
        { input_text: inputText.value },
        { headers: { Authorization: `Bearer ${store.state.token}` } }
      )
      responseText.value = res.data.output_text
    } catch (err) {
      console.error('AI generation failed:', err)
      toast.error('AI request failed.')
    } finally {
      loadingGenerate.value = false
    }
  }
  
  /* 3) Submit Announcement (POST /teacher/announcements) */
  async function submitAnnouncement() {
    if (!responseText.value.trim()) {
      toast.error('No AI text to submit.')
      return
    }
    if (!recipientOptions.value.classes && !recipientOptions.value.parents) {
      toast.error('Please select at least one recipient group.')
      return
    }
    loadingSubmit.value = true
    try {
      // Extract the subject from the response text.
      // Expected format on first line: "Topic: French | German | English"
      let title = ''
      let body = ''
      const lines = responseText.value.split("\n")
      if (lines[0].trim().startsWith("Topic:")) {
        title = lines[0].trim().substring("Topic:".length).trim()
        body = lines.slice(1).join("\n").trim()
      } else {
        // Fallback if no valid topic line found
        title = "AI-Generated Announcement"
        body = responseText.value
      }
      await axios.post('/teacher/announcements',
        {
          title: title,
          body: body,
          attachment_url: null,
          classes: recipientOptions.value.classes ? selectedClasses.value : [],
          parents: recipientOptions.value.parents ? selectedParents.value : [],
        },
        { headers: { Authorization: `Bearer ${store.state.token}` } }
      )
      toast.success('Announcement submitted successfully!')
      emit('announcementCreated')
    } catch (err) {
      console.error('Error submitting announcement:', err)
      toast.error('Failed to submit announcement.')
    } finally {
      loadingSubmit.value = false
    }
  }
  </script>
  
  <style scoped>
  /* Minimal local styling */
  </style>
  