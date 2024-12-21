<!-- filename: vue_js_project/src/pages/DashboardParent.vue -->
<template>
  <DefaultLayout>
    <h1 class="text-2xl font-bold mb-4">Parent Dashboard</h1>
    <p>View announcements for your children’s classes.</p>

    <!-- Add Child Form -->
    <div class="mt-8 p-4 border rounded bg-white dark:bg-gray-800">
      <h2 class="text-xl font-bold mb-4">Add a Child</h2>
      <div class="mb-2">
        <input v-model="firstName" placeholder="Child's First Name" class="w-full p-2 border rounded mb-2" />
        <input v-model="lastName" placeholder="Child's Last Name" class="w-full p-2 border rounded mb-2" />
        
        <select v-model="selectedClassId" class="w-full p-2 border rounded mb-4">
          <option disabled value="">Select a class</option>
          <option v-for="cls in classes" :key="cls.id" :value="cls.id">
            {{ cls.name }}
          </option>
        </select>
        
        <button @click="addChild" class="bg-primary text-white px-4 py-2 rounded">
          Add Child
        </button>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import DefaultLayout from '../layouts/DefaultLayout.vue';
import { useStore } from 'vuex';

const store = useStore();
const firstName = ref('');
const lastName = ref('');
const selectedClassId = ref('');
const classes = ref([]);

onMounted(async () => {
  try {
    console.log("Fetching classes...");
    const res = await axios.get('/classes');
    console.log("Classes fetched:", res.data);
    classes.value = res.data;
  } catch (err) {
    console.error("Error fetching classes:", err);
  }
});

async function addChild() {
  try {
    console.log("Attempting to fetch current user...");
    console.log("Authorization token:", store.state.token);

    const me = await axios.get('/users/me', {
      headers: { Authorization: `Bearer ${store.state.token}` }
    });

    console.log("Current user data:", me.data);

    console.log("Adding child with details:", {
      parent_id: me.data.id,
      first_name: firstName.value,
      last_name: lastName.value,
      class_id: selectedClassId.value
    });

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
    );

    console.log("Child added successfully:", res.data);

    // Clear form
    firstName.value = '';
    lastName.value = '';
    selectedClassId.value = '';
  } catch (err) {
    console.error("Error adding child:", err);
  }
}
</script>
