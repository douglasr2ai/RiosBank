<template>
  <div class="mock mock-aprovacao">
    <div class="timer-row">
      <span class="timer mono">07s</span>
      <span class="timer-label">Aprovação coletiva</span>
    </div>

    <div class="tx">
      <span class="tx-line"><strong>Marina</strong> quer pagar</span>
      <span class="tx-value mono">R$ 1.200</span>
      <span class="tx-line">para <strong>Douglas</strong></span>
      <span class="tx-desc">Aluguel — Av. Paulista</span>
    </div>

    <div class="vote-row">
      <button class="vote reject">Reprovar</button>
      <button class="vote approve">Aprovar</button>
    </div>

    <div class="status-row">
      <span class="dot up" /> 2 aprovações
      <span class="sep">·</span>
      <span class="dot dn" /> 0 reprovações
      <span class="sep">·</span>
      <span class="dot pending" /> 1 sem voto
    </div>

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
  display: flex; flex-direction: column; gap: 14px;
}
.timer-row {
  display: flex; flex-direction: column; align-items: center; gap: 2px;
}
.timer {
  font-size: 32px; font-weight: 800;
  color: var(--amber);
}
.timer-label {
  font-size: 11px;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: .12em;
  color: var(--text-2);
  text-transform: uppercase;
}
.tx {
  background: rgba(255,255,255,.04);
  border-radius: 12px;
  padding: 12px;
  display: flex; flex-direction: column; align-items: center; gap: 2px;
}
.tx-line { font-size: 13px; color: var(--text-2); }
.tx-line strong { color: var(--text); font-weight: 700; }
.tx-value { font-size: 24px; font-weight: 800; color: var(--green); margin: 2px 0; }
.tx-desc { font-size: 11px; color: var(--text-2); margin-top: 4px; }
.vote-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.vote {
  border-radius: 12px;
  padding: 12px;
  font-size: 13px;
  font-weight: 700;
  font-family: 'Manrope', sans-serif;
  border: 0;
  cursor: default;
}
.vote.reject {
  background: rgba(224,84,84,.12);
  color: var(--danger);
  border: 1px solid rgba(224,84,84,.3);
}
.vote.approve {
  background: linear-gradient(135deg, var(--green), var(--green-d));
  color: #fff;
}
.status-row {
  display: flex; align-items: center; justify-content: center;
  gap: 6px; font-size: 11px; color: var(--text-2);
}
.dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; }
.dot.up { background: var(--green); }
.dot.dn { background: var(--danger); }
.dot.pending { background: var(--text-2); opacity: .6; }
.sep { opacity: .4; }
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
