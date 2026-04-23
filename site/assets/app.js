const state = { mode: 'all', font: 'all', category: 'all' };

function setActive(group, button) {
  group.querySelectorAll('[data-selectable]').forEach((item) => item.classList.remove('active'));
  button.classList.add('active');
}

function filterCards() {
  const search = document.getElementById('searchInput').value.trim().toLowerCase();
  let visible = 0;

  document.querySelectorAll('.style-card').forEach((card) => {
    const matchesMode = state.mode === 'all' || card.dataset.mode === state.mode;
    const matchesFont = state.font === 'all' || card.dataset.font === state.font;
    const matchesCategory = state.category === 'all' || card.dataset.category === state.category;
    const matchesSearch =
      !search ||
      card.dataset.name.includes(search) ||
      card.dataset.mode.includes(search) ||
      card.dataset.font.includes(search) ||
      card.dataset.categorySearch.includes(search);

    const isVisible = matchesMode && matchesFont && matchesCategory && matchesSearch;
    card.hidden = !isVisible;
    if (isVisible) visible += 1;
  });

  document.getElementById('resultCount').textContent = `${visible} styles`;
  document.getElementById('noResults').hidden = visible !== 0;
}

document.querySelectorAll('[data-filter]').forEach((button) => {
  button.addEventListener('click', () => {
    const group = button.closest('[data-filter-group]');
    setActive(group, button);
    state[button.dataset.filter] = button.dataset.value;
    filterCards();
  });
});

document.getElementById('searchInput').addEventListener('input', filterCards);
filterCards();
