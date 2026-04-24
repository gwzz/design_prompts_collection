const copyButton = document.querySelector('[data-copy-target]');

if (copyButton) {
  copyButton.addEventListener('click', async () => {
    const target = document.getElementById(copyButton.dataset.copyTarget);
    if (!target) return;

    try {
      await navigator.clipboard.writeText(target.textContent);
      const originalLabel = copyButton.textContent;
      const successLabel = document.body.dataset.copySuccess || 'Copied';
      copyButton.textContent = successLabel;
      copyButton.classList.add('copied');
      window.setTimeout(() => {
        copyButton.textContent = originalLabel;
        copyButton.classList.remove('copied');
      }, 1800);
    } catch (error) {
      const failedLabel = document.body.dataset.copyFailed || 'Copy failed';
      copyButton.textContent = failedLabel;
    }
  });
}
