// Hydrate Astro island on first keyboard, screen-reader click, pointer, or scroll interaction
export default (load, _options, el) => {
  let done = false;
  let hydrated = false;
  let pendingDescriptor = null;

  const events = ['pointerdown', 'touchstart', 'keydown', 'scroll', 'hr:hydrate'];
  const cleanupTriggers = () => {
    for (const ev of events) {
      window.removeEventListener(ev, trigger, { capture: true });
    }
    el.removeEventListener('pointerenter', trigger);
    el.removeEventListener('focusin', trigger);
  };

  const replayButton = () => {
    if (!pendingDescriptor) return;
    const { node, btnIndex, dataCity, ariaLabel } = pendingDescriptor;
    pendingDescriptor = null;
    let target = node && el.contains(node) ? node : null;
    if (!target && dataCity) {
      target = el.querySelector(`button[data-city="${dataCity}"]`);
    }
    if (!target && ariaLabel) {
      target = el.querySelector(`button[aria-label="${CSS.escape(ariaLabel)}"]`);
    }
    if (!target && btnIndex >= 0) {
      target = el.querySelectorAll('button')[btnIndex] || null;
    }
    if (target instanceof HTMLElement) {
      requestAnimationFrame(() => {
        target.focus({ preventScroll: true });
        target.click();
      });
    }
  };

  const trigger = async () => {
    if (done) return;
    done = true;
    cleanupTriggers();
    const hydrate = await load();
    await hydrate();
    hydrated = true;
    el.removeEventListener('click', onEarlyClick, { capture: true });
    replayButton();
  };

  const onEarlyClick = (ev) => {
    if (hydrated) return;
    const btn = ev.target instanceof Element ? ev.target.closest('button') : null;
    if (btn) {
      ev.preventDefault();
      ev.stopPropagation();
      const allBtns = [...el.querySelectorAll('button')];
      pendingDescriptor = {
        node: btn,
        btnIndex: allBtns.indexOf(btn),
        dataCity: btn.getAttribute('data-city'),
        ariaLabel: btn.getAttribute('aria-label')
      };
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
