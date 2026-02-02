const execGrid = document.querySelector('#exec-board-grid');
const execError = document.querySelector('#exec-board-error');

if (execGrid) {
    fetch('exec-board.json')
        .then((response) => {
            if (!response.ok) {
                throw new Error('Failed to load exec board data.');
            }
            return response.json();
        })
        .then((members) => {
            execGrid.innerHTML = '';

            members.forEach((member) => {
                const card = document.createElement('div');
                card.className = 'col-12 col-md-6 col-lg-4';
                card.innerHTML = `
                    <div class="card h-100">
                        <div class="card-body text-center p-4">
                            <div class="exec-photo mx-auto mb-3">
                                <img src="${member.photo}" alt="${member.name} headshot">
                            </div>
                            <h5 class="fw-bold mb-1">${member.name}</h5>
                            <span class="badge badge-gold mb-2">${member.position}</span>
                            <p class="text-muted mb-2">${member.major}</p>
                            <p class="mb-0">${member.bio}</p>
                        </div>
                    </div>
                `;
                execGrid.appendChild(card);
            });
        })
        .catch(() => {
            if (execError) {
                execError.classList.remove('d-none');
            }
        });
}
