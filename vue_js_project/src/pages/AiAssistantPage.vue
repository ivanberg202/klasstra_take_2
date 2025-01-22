<template>
  <DefaultLayout>
    <div class="max-w-2xl mx-auto my-8 p-4 border rounded bg-white dark:bg-gray-800">
      <h1 class="text-xl font-bold mb-4 text-gray-900 dark:text-gray-100">AI Assistant</h1>
      <p class="text-gray-700 dark:text-gray-300 mb-4">
        Drop a few unstructured lines about what you want to announce. You will get an AI-improved 
        message in French, German, and English to review, edit, and send.
      </p>
      
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Your Text</label>
          <textarea
            v-model="inputText"
            rows="5"
            class="w-full p-2 border rounded dark:bg-gray-700 dark:text-white dark:border-gray-600"
            placeholder="Paste your announcement or lesson text here..."
          ></textarea>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="bg-primary text-white px-4 py-2 rounded disabled:opacity-50 w-full"
        >
          {{ loading ? "Generating..." : "Generate" }}
        </button>
      </form>

      <div v-if="responseText" class="mt-6">
        <h2 class="font-bold mb-2">AI Response</h2>
        <textarea
          v-model="responseText"
          rows="20"
          class="w-full p-2 border rounded bg-gray-100 dark:bg-gray-900 dark:text-white dark:border-gray-600"
          style="white-space: pre-wrap; resize: vertical;"
        ></textarea>
        <button
          @click="handleEditSubmit"
          class="mt-4 bg-secondary text-white px-4 py-2 rounded w-full"
        >
          Submit Edited Text
        </button>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '../plugins/axios.js';
import DefaultLayout from '../layouts/DefaultLayout.vue';
import { useStore } from 'vuex';
import { useToast } from 'vue-toastification';

const store = useStore();
const toast = useToast();

const inputText = ref('');
const responseText = ref('');
const loading = ref(false);

onMounted(() => {
  console.log('AI Assistant Store Token:', store.state.token);
});

async function handleSubmit() {
  console.log('Form submitted with the following data:');
  console.log('Input Text:', inputText.value);
  console.log('Token in Store:', store.state.token);

  if (!inputText.value.trim()) {
    toast.error('Please enter some text to transform.');
    return;
  }

  loading.value = true;
  responseText.value = '';

  try {
    const res = await axios.post(
      '/ai/generate',
      { input_text: inputText.value },
      {
        headers: {
          Authorization: `Bearer ${store.state.token}`,
        },
      }
    );
    console.log('API Response:', res.data);
    responseText.value = res.data.output_text;
  } catch (err) {
    console.error('Error during API call:', err);
    toast.error('AI request failed.');
  } finally {
    loading.value = false;
  }
}

async function handleEditSubmit() {
  console.log('Submitting edited text:', responseText.value);

  try {
    const res = await axios.post(
      '/ai/submit-edited',
      { edited_text: responseText.value },
      {
        headers: {
          Authorization: `Bearer ${store.state.token}`,
        },
      }
    );
    console.log('Edited Text Submission Response:', res.data);
    toast.success('Edited text submitted successfully!');
  } catch (err) {
    console.error('Error during submission:', err);
    toast.error('Failed to submit edited text.');
  }
}
</script>

<style scoped>
/* Optional local styling */
</style>
