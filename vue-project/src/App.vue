<template>
  <header>
    <div class="wrapper">
      <AppNavbar/>

    </div>
  </header>

  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import AppNavbar from './components/Common/AppNavbar.vue';


</script>

<style>

</style>