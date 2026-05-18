<template>
  <div class="mock mock-host">
    <div class="hdr">
      <span class="hdr-title">Painel do Host</span>
      <span class="hdr-tag">você é host</span>
    </div>

    <div class="section-list">
      <div class="row">
        <div class="row-info">
          <span class="row-title">Estornar transação</span>
          <span class="row-sub">Última: Marina → Douglas · R$ 1.200</span>
        </div>
        <button class="btn ghost">Estornar</button>
      </div>

      <div class="row">
        <div class="row-info">
          <span class="row-title">Ajustar saldo</span>
          <span class="row-sub">Em caso de erro real</span>
        </div>
        <button class="btn ghost">Ajustar</button>
      </div>

      <div class="row">
        <div class="row-info">
          <span class="row-title">Expulsar jogador</span>
          <span class="row-sub">Remove da partida</span>
        </div>
        <button class="btn ghost danger">Expulsar</button>
      </div>

      <div class="row">
        <div class="row-info">
          <span class="row-title">Encerrar partida</span>
          <span class="row-sub">Gera o histórico final</span>
        </div>
        <button class="btn primary">Encerrar</button>
      </div>
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
  display: flex; flex-direction: column; gap: 14px;
}
.hdr { display: flex; justify-content: space-between; align-items: center; }
.hdr-title { font-size: 14px; font-weight: 700; }
.hdr-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  background: var(--green-dim);
  color: var(--green);
  padding: 2px 8px;
  border-radius: 6px;
}
.section-list { display: flex; flex-direction: column; gap: 8px; }
.row {
  display: flex; align-items: center; gap: 10px;
  background: rgba(255,255,255,.03);
  padding: 10px;
  border-radius: 10px;
}
.row-info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.row-title { font-size: 13px; font-weight: 700; }
.row-sub { font-size: 11px; color: var(--text-2); }
.btn {
  font-size: 11px; font-weight: 700; font-family: 'Manrope', sans-serif;
  border-radius: 8px;
  padding: 7px 12px;
  border: 1px solid rgba(255,255,255,.12);
  background: rgba(255,255,255,.06);
  color: var(--text);
  cursor: default;
}
.btn.ghost.danger { color: var(--danger); border-color: rgba(224,84,84,.3); }
.btn.primary {
  background: linear-gradient(135deg, var(--green), var(--green-d));
  border-color: transparent;
  color: #fff;
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
</style>
