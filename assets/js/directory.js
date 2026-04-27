const directoryGrid = document.querySelector('#directory-grid');
const directoryError = document.querySelector('#directory-error');
const directorySort = document.querySelector('#directory-sort');
const directoryCount = document.querySelector('#directory-count');
const fallbackPhoto = '../assets/img/shared/profile-placeholder.svg';

const state = {
    members: []
};

const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    '\'': '&#39;'
}[char]));

const renderSocialLinks = (member) => {
    const links = [];

    if (member.linkedin) {
        links.push(`
            <a class="btn btn-primary member-action-btn" href="${escapeHtml(member.linkedin)}" target="_blank" rel="noopener noreferrer" aria-label="Open ${escapeHtml(member.name)} LinkedIn profile">
                <i class="bi bi-linkedin" aria-hidden="true"></i>
            </a>
        `);
    }

    if (member.github) {
        links.push(`
            <a class="btn btn-secondary member-action-btn" href="${escapeHtml(member.github)}" target="_blank" rel="noopener noreferrer" aria-label="Open ${escapeHtml(member.name)} GitHub profile">
                <i class="bi bi-github" aria-hidden="true"></i>
            </a>
        `);
    }

    if (!links.length) {
        return '<p class="mb-0 text-muted">No social profiles listed.</p>';
    }

    return `<div class="member-actions">${links.join('')}</div>`;
};

const populateSeasonOptions = () => {
    const seasons = [...new Map(
        state.members
            .sort((left, right) => right.inductionSortKey - left.inductionSortKey || left.name.localeCompare(right.name))
            .map((member) => [member.inductionSeason, member.inductionSortKey])
    ).entries()];

    directorySort.innerHTML = `
        <option value="all">All seasons</option>
        ${seasons.map(([season]) => `<option value="${escapeHtml(season)}">${escapeHtml(season)}</option>`).join('')}
    `;
};

const renderMembers = (selectedSeason = 'all') => {
    if (!directoryGrid) {
        return;
    }

    const members = [...state.members].sort((left, right) => {
        const seasonComparison = right.inductionSortKey - left.inductionSortKey;
        if (seasonComparison !== 0) {
            return seasonComparison;
        }

        return left.name.localeCompare(right.name);
    });
    const filteredMembers = selectedSeason === 'all'
        ? members
        : members.filter((member) => member.inductionSeason === selectedSeason);

    directoryCount.textContent = String(filteredMembers.length);

    if (!filteredMembers.length) {
        directoryGrid.innerHTML = `
            <div class="col-12">
                <div class="card empty-state text-center">
                    <div class="card-body">
                        <p class="mb-0 text-muted">No members were found for that induction season.</p>
                    </div>
                </div>
            </div>
        `;
        return;
    }

    directoryGrid.innerHTML = filteredMembers.map((member) => `
        <div class="col-12 col-md-6 col-xl-4">
            <article class="card directory-card h-100">
                <div class="card-body">
                    <div class="member-photo">
                        <img src="${escapeHtml(member.photo)}" alt="${escapeHtml(member.name)} headshot" loading="lazy" onerror="this.onerror=null;this.src='${fallbackPhoto}';">
                    </div>
                    <div>
                        <span class="badge badge-gold mb-2">${escapeHtml(member.inductionSeason)}</span>
                        <h3 class="h4 fw-bold mb-1">${escapeHtml(member.name)}</h3>
                        <p class="text-muted mb-0">Class of ${escapeHtml(member.graduationYear)}</p>
                    </div>
                    <div class="member-meta">
                        <div class="member-meta-item member-meta-item-major">
                            <p class="small-caps text-muted mb-1">Major</p>
                            <p class="member-major-text">${escapeHtml(member.major)}</p>
                        </div>
                        <div class="member-meta-item">
                            <p class="small-caps text-muted mb-1">Email</p>
                            <a class="member-email-link" href="mailto:${escapeHtml(member.email)}">${escapeHtml(member.email)}</a>
                        </div>
                        <div class="member-meta-item">
                            <p class="small-caps text-muted mb-1">Profiles</p>
                            ${renderSocialLinks(member)}
                        </div>
                    </div>
                </div>
            </article>
        </div>
    `).join('');
};

if (directoryGrid && directorySort && directoryCount) {
    fetch('./members.json')
        .then((response) => {
            if (!response.ok) {
                throw new Error('Failed to load directory data.');
            }

            return response.json();
        })
        .then((members) => {
            state.members = members;
            populateSeasonOptions();
            renderMembers(directorySort.value);
        })
        .catch(() => {
            directoryError?.classList.remove('d-none');
            directoryGrid.innerHTML = '';
        });

    directorySort.addEventListener('change', (event) => {
        renderMembers(event.target.value);
    });
}
