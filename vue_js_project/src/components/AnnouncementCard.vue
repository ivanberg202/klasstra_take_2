<!-- filename: src/components/AnnouncementCard.vue -->
<template>
  <div class="border rounded p-4 shadow mb-4 bg-white dark:bg-gray-800 dark:text-white">
    <!-- Title -->
    <h2 class="font-bold text-lg">{{ announcement.title }}</h2>
    
    <!-- Recipient Display -->
    <div v-if="hasRecipient" class="mt-1">
      <small class="text-gray-600 dark:text-gray-300">
        Recipient:
        <span v-if="recipientDisplay">
          {{ recipientDisplay }}
        </span>
        <span v-else>
          (ID: {{ announcement.recipient_id }})
        </span>
      </small>
    </div>
    
    <!-- Collapsible Message Body Toggle -->
    <div class="mt-2">
      <button @click="toggleExpanded" class="text-blue-500 hover:underline">
        {{ expanded ? "Hide Message" : "Show Message" }}
      </button>
    </div>
    
    <!-- Expanded message body -->
    <div v-if="expanded" class="mt-2">
      <p class="whitespace-pre-line">{{ announcement.body }}</p>
    </div>
    
    <!-- Attachment Link -->
    <div v-if="announcement.attachment_url" class="mt-2">
      <a :href="announcement.attachment_url" target="_blank" class="text-blue-500 underline">View Attachment</a>
    </div>
    
    <!-- Creator and Date -->
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
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import axios from '../plugins/axios.js';
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
const expanded = ref(false);
const recipientDetail = ref(null);
const loadingRecipient = ref(false);

// Toggle the message body expansion/collapse
const toggleExpanded = () => {
  expanded.value = !expanded.value;
};

// Check if the announcement has recipient info
const hasRecipient = computed(() => {
  return props.announcement.recipient_type && props.announcement.recipient_id;
});

// Compute a user-friendly recipient display based on recipient details
const recipientDisplay = computed(() => {
  if (!recipientDetail.value) return "";
  if (props.announcement.recipient_type === "class") {
    // Assuming a class object has a "name" field
    return `Class: ${recipientDetail.value.name}`;
  } else if (props.announcement.recipient_type === "parent") {
    // Assuming a parent object has "first_name" and "last_name"
    return `Parent: ${recipientDetail.value.first_name} ${recipientDetail.value.last_name}`;
  }
  return "";
});

// Fetch recipient details based on recipient_type and recipient_id.
const fetchRecipientDetail = async () => {
  if (!hasRecipient.value) return;
  loadingRecipient.value = true;
  try {
    if (props.announcement.recipient_type === "class") {
      // Get teacher's classes and filter the one with matching ID.
      const res = await axios.get('/teacher/my-classes', {
        headers: { Authorization: `Bearer ${store.state.token}` },
      });
      const cls = res.data.find(item => item.id === props.announcement.recipient_id);
      if (cls) {
        recipientDetail.value = cls;
      }
    } else if (props.announcement.recipient_type === "parent") {
      // Get teacher's parents and filter for matching parent.
      const res = await axios.get('/announcements/teacher/parents', {
        headers: { Authorization: `Bearer ${store.state.token}` },
      });
      const par = res.data.find(item => item.id === props.announcement.recipient_id);
      if (par) {
        recipientDetail.value = par;
      }
    }
  } catch (err) {
    console.error('Error fetching recipient detail:', err);
    toast.error('Failed to load recipient details.');
  } finally {
    loadingRecipient.value = false;
  }
};

// Fetch recipient details when component is mounted or if announcement changes.
onMounted(fetchRecipientDetail);
watch(() => props.announcement, () => {
  recipientDetail.value = null;
  fetchRecipientDetail();
});

// Check if the logged-in user is the creator
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
/* Component-specific styling can be added here */
</style>
