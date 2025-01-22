<!-- filename: src/components/EditAnnouncementModal.vue -->
<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 p-6 rounded shadow-lg w-11/12 max-w-md">
      <h2 class="text-xl font-bold mb-4">Edit Announcement</h2>
      <form @submit.prevent="submitEdit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium">Title</label>
          <input
            v-model="editTitle"
            type="text"
            required
            class="w-full p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
          />
        </div>
        <div>
          <label class="block text-sm font-medium">Body</label>
          <textarea
            v-model="editBody"
            required
            class="w-full p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
          ></textarea>
        </div>
        <div class="flex space-x-4">
          <button
            type="submit"
            :disabled="isSubmitting"
            class="bg-primary text-white px-4 py-2 rounded w-full disabled:opacity-50"
          >
            {{ isSubmitting ? 'Saving...' : 'Save Changes' }}
          </button>
          <button
            type="button"
            @click="$emit('close')"
            class="bg-gray-300 dark:bg-gray-600 text-black dark:text-white px-4 py-2 rounded w-full"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from '../plugins/axios.js'
import { useStore } from 'vuex';
import { useToast } from 'vue-toastification';

const props = defineProps({
  announcement: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['close', 'edited']);

const store = useStore();
const toast = useToast();

// Form state
const editTitle = ref(props.announcement.title);
const editBody = ref(props.announcement.body);
const isSubmitting = ref(false);

// Submit edited announcement
const submitEdit = async () => {
  isSubmitting.value = true;
  try {
    const payload = {
      title: editTitle.value,
      body: editBody.value,
    };

    await axios.patch(`/teacher/announcements/${props.announcement.id}`, payload, {
      headers: { Authorization: `Bearer ${store.state.token}` },
    });

    toast.success('Announcement updated successfully!');
    emit('edited');
  } catch (err) {
    console.error('Error updating announcement:', err);
    toast.error('Failed to update announcement.');
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
/* Modal styles can be enhanced as needed */
</style>
