<template>
  <div class="player-pill" :class="{ 'pp-host': isHost, 'pp-falido': isFalido }">
    <div class="avatar">{{ nome[0]?.toUpperCase() }}</div>
    <span class="pp-nome">{{ nome }}</span>
    <span v-if="isHost" class="host-badge">host</span>
    <span v-if="isFalido" class="falido-badge">falido</span>
  </div>
</template>

<script setup>
defineProps({
  nome: { type: String, required: true },
  isHost: { type: Boolean, default: false },
  isFalido: { type: Boolean, default: false },
})
</script>

<style scoped>
.player-pill {
  display: flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,.05);
  border: 1px solid rgba(255,255,255,.09);
  border-radius: 999px; padding: 6px 12px 6px 6px;
}

.avatar {
  width: 28px; height: 28px; border-radius: 50%;
  background: var(--green-dim);
  border: 1px solid rgba(46,204,113,.2);
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; color: var(--green);
}

.pp-nome { font-size: 13px; font-weight: 600; }

.host-badge, .falido-badge {
  font-size: 9px; font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: .05em; text-transform: uppercase;
  border-radius: 999px; padding: 2px 7px;
}
.host-badge { background: var(--green-dim); color: var(--green); }
.falido-badge { background: rgba(224,84,84,.1); color: var(--danger); }

.pp-falido .avatar { background: rgba(224,84,84,.1); border-color: rgba(224,84,84,.2); color: var(--danger); }
.pp-host { border-color: rgba(46,204,113,.2); }
</style>
