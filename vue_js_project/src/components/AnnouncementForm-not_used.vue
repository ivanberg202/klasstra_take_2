<!-- filename: src/components/AnnouncementForm.vue -->
<template>
    <form @submit.prevent="submitAnnouncement" class="space-y-4">
      
      <!-- TITLE -->
      <div>
        <label class="block text-sm font-medium">Title</label>
        <input
          v-model="title"
          type="text"
          placeholder="Announcement Title"
          required
          class="w-full p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
        />
      </div>
  
      <!-- BODY -->
      <div>
        <label class="block text-sm font-medium">Body</label>
        <textarea
          v-model="body"
          rows="4"
          placeholder="Type your announcement here..."
          required
          class="w-full p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
        ></textarea>
      </div>
  
      <!-- RECIPIENTS CHECKBOXES -->
      <div>
        <label class="block text-sm font-medium">Recipients</label>
        <div class="flex space-x-4">
          <div class="flex items-center">
            <input
              type="checkbox"
              id="classes"
              v-model="recipientOptions.classes"
              class="mr-2"
            />
            <label for="classes">Classes</label>
          </div>
          <div class="flex items-center">
            <input
              type="checkbox"
              id="parents"
              v-model="recipientOptions.parents"
              class="mr-2"
            />
            <label for="parents">Parents</label>
          </div>
        </div>
      </div>
  
      <!-- CLASSES DROPDOWN -->
      <div v-if="recipientOptions.classes">
        <label class="block text-sm font-medium">Select Classes</label>
        <select
          v-model="selectedClasses"
          multiple
          class="w-full p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
        >
          <option v-for="cls in classes" :key="cls.id" :value="cls.id">
            {{ cls.name }}
          </option>
        </select>
      </div>
  
      <!-- PARENTS DROPDOWN -->
      <div v-if="recipientOptions.parents">
        <label class="block text-sm font-medium">Select Parents</label>
        <select
          v-model="selectedParents"
          multiple
          class="w-full p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
        >
          <option v-for="parent in parents" :key="parent.id" :value="parent.id">
            {{ parent.first_name }} {{ parent.last_name }}
          </option>
        </select>
      </div>
  
      <!-- ATTACHMENT FILE INPUT (OPTIONAL) -->
      <div>
        <label class="block text-sm font-medium">Attach File (optional)</label>
        <input
          type="file"
          @change="handleFileUpload"
          class="w-full p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
        />
      </div>
  
      <!-- SUBMIT BUTTON -->
      <div>
        <button
          type="submit"
          :disabled="isSubmitting"
          class="bg-primary text-white px-4 py-2 rounded w-full disabled:opacity-50"
        >
          {{ isSubmitting ? 'Publishing...' : 'Publish Announcement' }}
        </button>
      </div>
    </form>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from '../plugins/axios.js';
  import { useStore } from 'vuex';
  import { useToast } from 'vue-toastification';
  
  const emit = defineEmits(['announcementCreated']);
  
  // Form state
  const title = ref('');
  const body = ref('');
  const recipientOptions = ref({
    classes: false,
    parents: false,
  });
  const selectedClasses = ref([]);
  const selectedParents = ref([]);
  const attachmentFile = ref(null);
  const isSubmitting = ref(false);
  
  // Recipient data
  const classes = ref([]);
  const parents = ref([]);
  
  const store = useStore();
  const toast = useToast();
  
  // Fetch classes & parents (depends on user role)
  const fetchRecipients = async () => {
    try {
      // 1) Fetch classes assigned to the teacher
      const classesRes = await axios.get('/teacher/my-classes', {
        headers: {
          Authorization: `Bearer ${store.state.token}`,
        },
      });
      classes.value = classesRes.data;
  
      // 2) Fetch parents (differ by role)
      let parentsRes;
      const userRole = store.getters.getUserRole;
      if (userRole === 'admin') {
        // Admin fetches all parents
        parentsRes = await axios.get('/parents', {
          headers: {
            Authorization: `Bearer ${store.state.token}`,
          },
        });
      } else if (userRole === 'teacher' || userRole === 'class_rep') {
        // Teachers/class_rep fetch parents for their classes
        parentsRes = await axios.get('/announcements/teacher/parents', {
          headers: {
            Authorization: `Bearer ${store.state.token}`,
          },
        });
      } else {
        // Other roles not supported here
        parentsRes = { data: [] };
      }
  
      parents.value = parentsRes.data;
    } catch (err) {
      console.error('Error fetching recipients:', err);
      toast.error('Failed to load recipients.');
    }
  };
  
  // Handle file selection
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      attachmentFile.value = file;
    }
  };
  
  // Submit announcement
  const submitAnnouncement = async () => {
    isSubmitting.value = true;
    try {
      let attachmentUrl = null;
  
      // If there's a file, upload it first
      if (attachmentFile.value) {
        const formData = new FormData();
        formData.append('file', attachmentFile.value);
  
        const uploadRes = await axios.post('/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${store.state.token}`,
          },
        });
        attachmentUrl = uploadRes.data.url; // Adjust based on your backend response
      }
  
      // Check that at least one recipient group is selected
      const classesRecipients = recipientOptions.value.classes
        ? selectedClasses.value
        : [];
      const parentsRecipients = recipientOptions.value.parents
        ? selectedParents.value
        : [];
  
      if (classesRecipients.length === 0 && parentsRecipients.length === 0) {
        toast.error('Please select at least one recipient.');
        isSubmitting.value = false;
        return;
      }
  
      // Post a single request to /teacher/announcements
      const response = await axios.post(
        '/teacher/announcements',
        {
          title: title.value,
          body: body.value,
          attachment_url: attachmentUrl,
          classes: classesRecipients,  // array of class IDs
          parents: parentsRecipients,  // array of parent IDs
        },
        {
          headers: {
            Authorization: `Bearer ${store.state.token}`,
          },
        }
      );
  
      // Clear form
      title.value = '';
      body.value = '';
      recipientOptions.value = { classes: false, parents: false };
      selectedClasses.value = [];
      selectedParents.value = [];
      attachmentFile.value = null;
  
      // Notify parent component
      emit('announcementCreated');
  
      toast.success('Announcement published successfully!');
    } catch (err) {
      console.error('Error publishing announcement:', err);
      if (err.response && err.response.data && err.response.data.detail) {
        toast.error(`Failed to publish announcement: ${err.response.data.detail}`);
      } else {
        toast.error('Failed to publish announcement.');
      }
    } finally {
      isSubmitting.value = false;
    }
  };
  
  // Fetch recipients on mount
  onMounted(() => {
    fetchRecipients();
  });
  </script>
  
  <style scoped>
  /* Add any specific styling here */
  </style>
  