<template>
  <div class="mock mock-lobby">
    <div class="mock-header">
      <span class="mock-title">Sala: Reis do Tabuleiro</span>
      <span class="mock-code">A4K9B2</span>
    </div>

    <div class="invite-row">
      <span class="invite-label">Link de convite</span>
      <span class="invite-value mono">riosbank.r2pulse.com/join/…</span>
    </div>

    <div class="players-list">
      <div class="player-row">
        <div class="avatar host">D</div>
        <span class="name">Douglas <span class="tag-host">host</span></span>
        <span class="status online">● online</span>
      </div>
      <div class="player-row">
        <div class="avatar">M</div>
        <span class="name">Marina</span>
        <span class="status online">● online</span>
      </div>
      <div class="player-row">
        <div class="avatar">R</div>
        <span class="name">Rafael</span>
        <span class="status">● offline</span>
      </div>
    </div>

    <button class="start-btn" v-if="showStart" disabled>Iniciar partida</button>
    <template v-if="annotations">
      <span
        v-for="a in annotations"
        :key="a.label"
        class="annotation"
        :style="a.position"
      >{{ a.label }}</span>
    </template>
  </div>
</template>

<script setup>
defineProps({
  annotations: { type: Array, default: null },
  showStart: { type: Boolean, default: true },
})
</script>

<style scoped>
.mock {
  position: relative;
  background: var(--glass-bg);
  border: 1px solid var(--glass-br);
  border-radius: 18px;
  padding: 18px;
  font-family: 'Manrope', sans-serif;
  color: var(--text);
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.mock-header { display: flex; justify-content: space-between; align-items: center; }
.mock-title { font-size: 14px; font-weight: 700; }
.mock-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--green);
  background: var(--green-dim);
  padding: 3px 8px;
  border-radius: 6px;
}
.invite-row {
  background: rgba(255,255,255,.04);
  border-radius: 10px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.invite-label { font-size: 10px; color: var(--text-2); text-transform: uppercase; letter-spacing: .1em; }
.invite-value { font-size: 12px; color: var(--text); }
.players-list { display: flex; flex-direction: column; gap: 6px; }
.player-row {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255,255,255,.03);
  padding: 8px 10px;
  border-radius: 10px;
}
.avatar {
  width: 28px; height: 28px; border-radius: 50%;
  background: rgba(255,255,255,.06);
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700;
}
.avatar.host { background: var(--green-dim); color: var(--green); }
.name { flex: 1; font-size: 13px; font-weight: 600; }
.tag-host {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  background: var(--green-dim);
  color: var(--green);
  padding: 1px 6px;
  border-radius: 4px;
  margin-left: 4px;
}
.status { font-size: 10px; color: var(--text-2); }
.status.online { color: var(--green); }
.start-btn {
  background: linear-gradient(135deg, var(--green), var(--green-d));
  color: #fff;
  border: 0;
  border-radius: 12px;
  padding: 12px;
  font-size: 13px;
  font-weight: 700;
  font-family: 'Manrope', sans-serif;
  cursor: not-allowed;
  opacity: .9;
}
.annotation {
  position: absolute;
  background: var(--green);
  color: #06140E;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  pointer-events: none;
  white-space: nowrap;
}
.mono { font-family: 'JetBrains Mono', monospace; }
</style>
