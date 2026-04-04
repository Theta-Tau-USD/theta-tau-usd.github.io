fetch('../faq/faq.json')
  .then(res => res.json())
  .then(items => {
    const accordion = document.getElementById('faq-accordion');
    accordion.innerHTML = items.map((item, i) => `
      <div class="accordion-item">
        <h2 class="accordion-header">
          <button class="accordion-button collapsed" type="button"
            data-bs-toggle="collapse" data-bs-target="#faq-${i}">
            ${item.question}
          </button>
        </h2>
        <div id="faq-${i}" class="accordion-collapse collapse"
          data-bs-parent="#faq-accordion">
          <div class="accordion-body">
            ${item.answer}
          </div>
        </div>
      </div>
    `).join('');
  })
  .catch(() => {
    document.getElementById('faq-error').classList.remove('d-none');
    document.getElementById('faq-accordion').innerHTML = '';
  });
