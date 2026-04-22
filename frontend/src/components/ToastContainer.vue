<template>
  <div class="toast-wrap">
    <TransitionGroup name="toast" tag="div" class="toast-list">
      <div
        v-for="t in store.toasts"
        :key="t.id"
        class="toast"
        :class="`toast-${t.type}`"
        @click="store.remove(t.id)"
      >
        <svg v-if="t.type === 'error'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
          <circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>
        </svg>
        <svg v-else-if="t.type === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
          <circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/>
        </svg>
        <span>{{ t.message }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { useToastStore } from '../stores/toastStore'
const store = useToastStore()
</script>

<style scoped>
.toast-wrap {
  position: fixed;
  bottom: calc(var(--nav-h, 0px) + 16px);
  left: 50%;
  transform: translateX(-50%);
  z-index: 200;
  width: 100%;
  max-width: 360px;
  padding: 0 16px;
  pointer-events: none;
}

.toast-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 14px;
  font-size: 13px;
  font-weight: 600;
  font-family: 'Manrope', sans-serif;
  cursor: pointer;
  pointer-events: all;
  backdrop-filter: blur(24px);
}

.toast svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.toast-error {
  background: rgba(224, 84, 84, .18);
  border: 1px solid rgba(224, 84, 84, .35);
  color: #f87171;
}

.toast-success {
  background: rgba(46, 204, 113, .15);
  border: 1px solid rgba(46, 204, 113, .3);
  color: var(--green);
}

.toast-info {
  background: rgba(99, 179, 237, .12);
  border: 1px solid rgba(99, 179, 237, .25);
  color: var(--blue);
}

.toast-enter-active { transition: all .25s ease; }
.toast-leave-active { transition: all .2s ease; }
.toast-enter-from { opacity: 0; transform: translateY(12px); }
.toast-leave-to   { opacity: 0; transform: translateY(6px); }
</style>
