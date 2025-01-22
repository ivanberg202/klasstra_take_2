<!-- filename: src/pages/DashboardTeacher.vue -->
<template>
  <DefaultLayout>
    <div class="flex flex-col space-y-6">
      <!-- Assigned Classes Section -->
      <section>
        <h1 class="text-2xl font-bold mb-4">My Classes</h1>
        <div v-if="loadingClasses">
          <p class="italic">Loading classes...</p>
        </div>
        <div v-else>
          <div v-if="classes.length === 0">
            <p class="italic">No classes assigned.</p>
          </div>
          <ul class="list-disc list-inside">
            <li v-for="cls in classes" :key="cls.id" class="text-lg">
              {{ cls.name }}
            </li>
          </ul>
        </div>
      </section>

      <!-- Create Announcement Section (AI-Driven) -->
      <section>
        <h1 class="text-2xl font-bold mb-4">Create Announcement</h1>
        <AIAnnouncementForm @announcementCreated="handleAnnouncementCreated" />
      </section>

      <!-- Announcements List Section -->
      <section>
        <h1 class="text-2xl font-bold mb-4">Announcements</h1>
        <div v-if="loadingAnnouncements">
          <p class="italic">Loading announcements...</p>
        </div>
        <div v-else>
          <div v-if="announcements.length === 0">
            <p class="italic">No announcements yet.</p>
          </div>
          <AnnouncementCard
            v-for="ann in announcements"
            :key="ann.id"
            :announcement="ann"
            @edited="fetchAnnouncements"
            @deleted="fetchAnnouncements"
          />
        </div>
      </section>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../plugins/axios.js'
import { useStore } from 'vuex'
import { useToast } from 'vue-toastification'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import AIAnnouncementForm from '../components/AIAnnouncementForm.vue'
import AnnouncementCard from '../components/AnnouncementCard.vue'

const store = useStore()
const toast = useToast()

// State variables
const classes = ref([])
const loadingClasses = ref(false)

const announcements = ref([])
const loadingAnnouncements = ref(false)

// Fetch assigned classes
const fetchClasses = async () => {
  loadingClasses.value = true
  try {
    const res = await axios.get('/teacher/my-classes', {
      headers: {
        Authorization: `Bearer ${store.state.token}`,
      },
    })
    classes.value = res.data
  } catch (err) {
    console.error('Error fetching classes:', err)
    toast.error('Failed to load classes.')
  } finally {
    loadingClasses.value = false
  }
}

// Fetch announcements
const fetchAnnouncements = async () => {
  loadingAnnouncements.value = true
  try {
    const res = await axios.get('/teacher/my-announcements', {
      headers: {
        Authorization: `Bearer ${store.state.token}`,
      },
    })
    announcements.value = res.data
  } catch (err) {
    console.error('Error fetching announcements:', err)
    toast.error('Failed to load announcements.')
  } finally {
    loadingAnnouncements.value = false
  }
}

// Handle new announcement creation
const handleAnnouncementCreated = () => {
  fetchAnnouncements()
  toast.success('Announcement created successfully!')
}

// On component mount
onMounted(() => {
  fetchClasses()
  fetchAnnouncements()
})
</script>

<style scoped>
/* Add any specific styles here */
</style>
