// Hydrate Astro island only after user interaction or custom locale event
export default (load, _options, el) => {
  let done = false;
  let hydrated = false;
  let pendingBtn = null;

  const events = ['pointerdown', 'touchstart', 'keydown', 'scroll', 'hr:hydrate'];
  const cleanup = () => {
    for (const ev of events) {
      window.removeEventListener(ev, trigger, { capture: true });
    }
    el.removeEventListener('pointerenter', trigger);
    el.removeEventListener('focusin', trigger);
    el.removeEventListener('click', onEarlyClick, { capture: true });
  };

  const trigger = async () => {
    if (done) return;
    done = true;
    cleanup();
    const hydrate = await load();
    await hydrate();
    hydrated = true;
    if (pendingBtn && el.contains(pendingBtn)) {
      const target = pendingBtn;
      pendingBtn = null;
      queueMicrotask(() => target.click());
    }
  };

  const onEarlyClick = (ev) => {
    if (hydrated) return;
    const btn = ev.target instanceof Element ? ev.target.closest('button') : null;
    if (btn) {
      ev.preventDefault();
      ev.stopPropagation();
      pendingBtn = btn;
      trigger();
    }
  };

  for (const ev of events) {
    window.addEventListener(ev, trigger, { capture: true, passive: true, once: true });
  }
  el.addEventListener('pointerenter', trigger, { passive: true, once: true });
  el.addEventListener('focusin', trigger, { passive: true, once: true });
  el.addEventListener('click', onEarlyClick, { capture: true });
};
