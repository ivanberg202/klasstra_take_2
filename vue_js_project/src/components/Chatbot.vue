<!-- filename: vue_js_project/src/components/Chatbot.vue -->
<template>
    <div>
      <!-- Floating chat button -->
      <button
        class="fixed bottom-4 right-4 bg-blue-500 text-white p-4 rounded-full shadow-lg z-50"
        @click="toggleChatWindow"
      >
        <i class="fas fa-comment-alt"></i>
      </button>
  
      <!-- Chat window -->
      <div
        v-if="showChatWindow"
        class="fixed bottom-20 right-4 w-96 rounded-lg shadow-lg z-50 border"
        :class="darkMode ? 'bg-gray-900 text-white border-gray-700' : 'bg-white text-black border-gray-300'"
      >
        <div class="flex flex-col h-96">
          <!-- Chat messages -->
          <div class="flex-1 overflow-y-auto p-4">
            <div
              v-for="(message, index) in messages"
              :key="index"
              :class="message.sender === 'user' ? 'text-right' : 'text-left'"
            >
              <p
                :class="message.sender === 'user' ? userMessageClass : aiMessageClass"
                class="inline-block p-2 rounded-lg mb-2"
              >
                {{ message.text }}
              </p>
            </div>
          </div>
  
          <!-- Chat input -->
          <div class="flex p-2 border-t" :class="darkMode ? 'border-gray-700' : 'border-gray-300'">
            <input
              v-model="userMessage"
              class="flex-1 p-2 rounded-lg"
              :class="darkMode ? 'bg-gray-800 text-white placeholder-gray-400' : 'bg-gray-100 text-black placeholder-gray-500'"
              type="text"
              placeholder="Type your message..."
            />
            <button
              @click="sendMessage"
              class="ml-2 px-4 py-2 rounded-lg"
              :class="darkMode ? 'bg-blue-600 text-white' : 'bg-blue-500 text-white'"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import { useStore } from 'vuex';
  import axios from '../plugins/axios.js';
  
  // Vuex Store for dark mode
  const store = useStore();
  const darkMode = computed(() => store.state.darkMode);
  
  const showChatWindow = ref(false);
  const userMessage = ref('');
  const messages = ref([]);
  
  // Classes for user and AI messages
  const userMessageClass = 'bg-blue-500 text-white';
  const aiMessageClass = computed(() =>
    darkMode.value ? 'bg-gray-700 text-white' : 'bg-gray-200 text-black'
  );
  
  const toggleChatWindow = () => {
    showChatWindow.value = !showChatWindow.value;
  };
  
  const sendMessage = async () => {
    if (userMessage.value.trim() === '') return;
  
    messages.value.push({ sender: 'user', text: userMessage.value });
    const currentMessage = userMessage.value;
    userMessage.value = '';
  
    try {
      const res = await axios.post('/ai/chat', {
        message: currentMessage,
      });
      messages.value.push({ sender: 'ai', text: res.data.response });
    } catch (err) {
      console.error('Error sending message:', err);
      messages.value.push({ sender: 'ai', text: 'An error occurred. Please try again.' });
    }
  };
  </script>
  
  <style scoped>
  /* Add smooth transition for background color and text color changes */
  div {
    transition: background-color 0.3s ease, color 0.3s ease;
  }
  </style>
  