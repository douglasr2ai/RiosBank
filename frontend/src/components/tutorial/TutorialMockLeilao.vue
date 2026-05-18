<template>
  <div class="mock mock-leilao">
    <div class="hdr">
      <span class="hdr-pre">LEILÃO</span>
      <span class="hdr-prop">Av. Paulista</span>
      <span class="hdr-base">Lance mínimo: R$ 200</span>
    </div>

    <div class="lance-row">
      <span class="lance-label">LANCE ATUAL</span>
      <span class="lance-value mono">R$ 1.800</span>
      <span class="lance-lider">Líder: <strong>Marina</strong></span>
    </div>

    <div class="timer mono">42s</div>

    <div class="incrementos">
      <button class="inc">+ R$ 100</button>
      <button class="inc">+ R$ 500</button>
      <button class="inc">+ R$ 1.000</button>
    </div>

    <div class="last-bids">
      <div class="bid"><span>Marina</span><span class="mono">1.800</span></div>
      <div class="bid"><span>Douglas</span><span class="mono">1.300</span></div>
      <div class="bid"><span>Rafael</span><span class="mono">800</span></div>
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
defineProps({ annotations: { type: Array, default: null } })
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
  display: flex; flex-direction: column; gap: 12px;
  align-items: center;
}
.hdr { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.hdr-pre {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  letter-spacing: .14em;
  color: var(--amber);
}
.hdr-prop { font-size: 16px; font-weight: 800; }
.hdr-base { font-size: 11px; color: var(--text-2); }
.lance-row { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.lance-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  letter-spacing: .14em;
  color: var(--text-2);
}
.lance-value { font-size: 28px; font-weight: 800; color: var(--green); }
.lance-lider { font-size: 11px; color: var(--text-2); }
.lance-lider strong { color: var(--text); font-weight: 700; }
.timer {
  font-size: 22px; font-weight: 800; color: var(--amber);
  background: rgba(246,173,85,.08);
  padding: 6px 18px;
  border-radius: 999px;
}
.incrementos { display: flex; gap: 6px; }
.inc {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.1);
  color: var(--text);
  font-size: 11px;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  border-radius: 10px;
  padding: 8px 12px;
  cursor: default;
}
.last-bids {
  width: 100%;
  display: flex; flex-direction: column; gap: 4px;
  margin-top: 4px;
}
.bid {
  display: flex; justify-content: space-between;
  font-size: 11px; color: var(--text-2);
  padding: 4px 8px;
  background: rgba(255,255,255,.03);
  border-radius: 6px;
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
