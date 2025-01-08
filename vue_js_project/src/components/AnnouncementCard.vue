<!-- filename: src/components/AnnouncementCard.vue -->
<template>
  <div class="border rounded p-4 shadow mb-4 bg-white dark:bg-gray-800 dark:text-white">
    <h2 class="font-bold text-lg">{{ announcement.title }}</h2>
    <p class="mt-2">{{ announcement.body }}</p>
    <div v-if="announcement.attachment_url" class="mt-2">
      <a :href="announcement.attachment_url" target="_blank" class="text-blue-500 underline">View Attachment</a>
    </div>
    <small class="text-gray-500 dark:text-gray-400 mt-2 block">
      By: {{ announcement.created_by.first_name }} {{ announcement.created_by.last_name }} • {{ formattedDate }}
    </small>
    
    <!-- Edit & Delete Buttons -->
    <div v-if="isCreator" class="mt-2 flex space-x-2">
      <button @click="openEditModal" class="text-yellow-500 hover:underline">Edit</button>
      <button @click="deleteAnnouncement" class="text-red-500 hover:underline">Delete</button>
    </div>

    <!-- Edit Modal -->
    <EditAnnouncementModal
      v-if="showEditModal"
      :announcement="announcement"
      @close="showEditModal = false"
      @edited="onEdited"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import axios from '../plugins/axios.js'
import { useToast } from 'vue-toastification';
import EditAnnouncementModal from '../components/EditAnnouncementModal.vue';

const props = defineProps({
  announcement: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['edited', 'deleted']);

const store = useStore();
const toast = useToast();

const showEditModal = ref(false);

// Check if the logged-in teacher is the creator
const isCreator = computed(() => {
  return store.getters.getUserId === props.announcement.created_by.id;
});

// Format date
const formattedDate = computed(() => {
  const date = new Date(props.announcement.created_at);
  return date.toLocaleString();
});

// Open edit modal
const openEditModal = () => {
  showEditModal.value = true;
};

// Delete announcement
const deleteAnnouncement = async () => {
  if (!confirm('Are you sure you want to delete this announcement?')) return;

  try {
    await axios.delete(`/teacher/announcements/${props.announcement.id}`, {
      headers: { Authorization: `Bearer ${store.state.token}` },
    });
    toast.success('Announcement deleted successfully!');
    emit('deleted');
  } catch (err) {
    console.error('Error deleting announcement:', err);
    toast.error('Failed to delete announcement.');
  }
};

// Handle edited announcement
const onEdited = () => {
  showEditModal.value = false;
  emit('edited');
};
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
