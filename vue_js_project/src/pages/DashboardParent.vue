<template>
  <DefaultLayout>
    <h1 class="text-2xl font-bold mb-4">Parent Dashboard</h1>
    <p>View announcements for your children’s classes.</p>

    <!-- Announcements List -->
    <div class="mt-8">
      <h2 class="text-xl font-bold mb-2">Announcements</h2>
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
          :title="ann.title"
          :body="ann.body"
          :createdBy="ann.created_by"
          :createdAt="ann.created_at"
        />
      </div>
    </div>

    <!-- Children List -->
    <div class="mt-8">
      <h2 class="text-xl font-bold mb-2">My Children</h2>
      <div v-if="loadingChildren">
        <p class="italic">Loading children...</p>
      </div>
      <div v-else>
        <div v-if="children.length === 0">
          <p class="italic">No children registered yet.</p>
        </div>
        <ChildCard
          v-for="child in children"
          :key="child.id"
          :firstName="child.first_name"
          :lastName="child.last_name"
          :className="child.class_.name" 
          :createdAt="child.created_at"
        />
      </div>
    </div>

    <!-- Add Child Component -->
    <AddChild @childAdded="handleChildAdded" />
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import AnnouncementCard from '../components/AnnouncementCard.vue'
import ChildCard from '../components/ChildCard.vue'
import AddChild from '../components/AddChild.vue'
import { useStore } from 'vuex'
import { useToast } from 'vue-toastification'

const store = useStore()
const toast = useToast()

// Announcements
const announcements = ref([])
const loadingAnnouncements = ref(false)

// Children
const children = ref([])
const loadingChildren = ref(false)

// Fetch announcements on mount
const fetchAnnouncements = async () => {
  loadingAnnouncements.value = true
  try {
    const res = await axios.get('/announcements/for_parent', {
      headers: {
        Authorization: `Bearer ${store.state.token}`
      }
    })
    announcements.value = res.data
  } catch (err) {
    console.error('Error fetching parent announcements:', err)
    toast.error('Failed to load announcements.')
  } finally {
    loadingAnnouncements.value = false
  }
}

// Fetch children on mount
const fetchChildren = async () => {
  loadingChildren.value = true
  try {
    const res = await axios.get('/children/my', {
      headers: {
        Authorization: `Bearer ${store.state.token}`
      }
    })
    children.value = res.data
  } catch (err) {
    console.error('Error fetching children:', err)
    toast.error('Failed to load children.')
  } finally {
    loadingChildren.value = false
  }
}

// On component mount
onMounted(() => {
  fetchAnnouncements()
  fetchChildren()
})

// If a child is added, re-fetch announcements (if you want) and children
const handleChildAdded = () => {
  toast.success('Child added successfully!')
  fetchAnnouncements()
  fetchChildren()
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
