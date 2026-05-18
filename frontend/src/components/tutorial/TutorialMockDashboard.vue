<template>
  <div class="mock mock-dashboard">
    <div class="balance">
      <span class="balance-label">SEU SALDO</span>
      <span class="balance-value mono">R$ 12.400</span>
    </div>

    <div class="players">
      <div class="p-row me">
        <div class="dot" />
        <span class="p-name">Douglas (você)</span>
        <span class="p-bal mono">12.400</span>
      </div>
      <div class="p-row">
        <div class="dot" style="background:#63B3ED" />
        <span class="p-name">Marina</span>
        <span class="p-bal mono">8.200</span>
      </div>
      <div class="p-row">
        <div class="dot" style="background:#F6AD55" />
        <span class="p-name">Rafael</span>
        <span class="p-bal mono">5.900</span>
      </div>
    </div>

    <div class="actions">
      <button class="act primary">Transferir</button>
      <button class="act">Pagar aluguel</button>
      <button class="act">Comprar imóvel</button>
      <button class="act">Negociar</button>
    </div>

    <div class="nav">
      <span class="nav-item active">Saldo</span>
      <span class="nav-item">Imóveis</span>
      <span class="nav-item">Feed</span>
      <span class="nav-item">Ranking</span>
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
.balance {
  background: var(--green-dim);
  border: 1px solid rgba(46,204,113,.25);
  border-radius: 14px;
  padding: 14px;
  display: flex; flex-direction: column; gap: 4px;
  align-items: center;
}
.balance-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: var(--green);
  letter-spacing: .14em;
}
.balance-value { font-size: 26px; font-weight: 800; color: var(--green); }
.players { display: flex; flex-direction: column; gap: 4px; }
.p-row {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 8px;
  background: rgba(255,255,255,.03);
  border-radius: 8px;
}
.p-row.me { background: rgba(46,204,113,.06); }
.dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); }
.p-name { flex: 1; font-size: 12px; font-weight: 600; }
.p-bal { font-size: 12px; color: var(--text-2); }
.actions { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
.act {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.1);
  color: var(--text);
  font-size: 12px; font-weight: 700; font-family: 'Manrope', sans-serif;
  border-radius: 10px;
  padding: 10px 8px;
  cursor: default;
}
.act.primary {
  background: linear-gradient(135deg, var(--green), var(--green-d));
  border-color: transparent;
  color: #fff;
}
.nav {
  display: flex; justify-content: space-around;
  border-top: 1px solid rgba(255,255,255,.07);
  padding-top: 10px;
  margin-top: 2px;
}
.nav-item {
  font-size: 11px;
  color: var(--text-2);
  font-weight: 600;
}
.nav-item.active { color: var(--green); }
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
