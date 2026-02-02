const matchmakingForm = document.querySelector('#matchmaking-form');
const badgeGrid = document.querySelector('#badge-grid');
const rosterGrid = document.querySelector('#brother-roster-grid');
const resultsGrid = document.querySelector('#match-results');
const resultsNote = document.querySelector('#match-results-note');

let badgeIndex = {};
let brotherData = [];

const stopWords = new Set([
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'she', 'that',
    'the', 'their', 'they', 'this', 'to', 'was', 'we', 'with', 'you', 'your',
    'our', 'us', 'i', 'my', 'me', 'them', 'they', 'who', 'what', 'when',
    'where', 'why', 'how'
]);

const tokenize = (text) => {
    if (!text) {
        return [];
    }
    return text
        .toLowerCase()
        .replace(/[^a-z0-9\s]/g, ' ')
        .split(/\s+/)
        .filter((word) => word.length > 2 && !stopWords.has(word));
};

const vectorize = (tokens) => {
    const counts = {};
    tokens.forEach((token) => {
        counts[token] = (counts[token] || 0) + 1;
    });
    return counts;
};

const cosineSimilarity = (vecA, vecB) => {
    const keys = new Set([...Object.keys(vecA), ...Object.keys(vecB)]);
    let dot = 0;
    let normA = 0;
    let normB = 0;

    keys.forEach((key) => {
        const a = vecA[key] || 0;
        const b = vecB[key] || 0;
        dot += a * b;
        normA += a * a;
        normB += b * b;
    });

    if (normA === 0 || normB === 0) {
        return 0;
    }

    return dot / (Math.sqrt(normA) * Math.sqrt(normB));
};

const buildProfileText = (profile, badges) => {
    const badgeNames = (profile.badges || [])
        .map((badgeId) => badges[badgeId]?.name || '')
        .join(' ');
    return [profile.description, profile.major, profile.year, badgeNames]
        .filter(Boolean)
        .join(' ');
};

const renderBadgeCheckboxes = (badges) => {
    badgeGrid.innerHTML = '';

    badges.forEach((badge) => {
        const label = document.createElement('label');
        label.className = 'badge-checkbox-item-vertical';
        label.innerHTML = `
            <input type="checkbox" name="badges" value="${badge.id}" aria-label="${badge.name}">
            <div class="badge-content-vertical">
                <img class="badge-icon-large-form" src="${badge.icon}" alt="${badge.name} badge">
                <div class="badge-name-vertical">${badge.name}</div>
            </div>
        `;

        const checkbox = label.querySelector('input');
        checkbox.addEventListener('change', () => {
            label.classList.toggle('checked', checkbox.checked);
        });

        badgeGrid.appendChild(label);
    });
};

const createBadgePill = (badge, sizeClass) => {
    if (!badge) {
        return '';
    }
    return `
        <span class="${sizeClass} ${badge.pillar}">
            <img class="${sizeClass.includes('card') ? 'badge-pill-icon-card' : 'badge-pill-icon'}" src="${badge.icon}" alt="${badge.name} badge">
            <span class="${sizeClass.includes('card') ? 'badge-pill-name-card' : 'badge-pill-name'}">${badge.name}</span>
        </span>
    `;
};

const renderBrotherRoster = (brothers) => {
    rosterGrid.innerHTML = '';

    brothers.forEach((brother) => {
        const card = document.createElement('div');
        card.className = 'col-12 col-md-6 col-lg-4';

        const badgesHtml = (brother.badges || [])
            .map((badgeId) => createBadgePill(badgeIndex[badgeId], 'badge-pill'))
            .join('');

        card.innerHTML = `
            <div class="card h-100">
                <div class="card-body text-center p-4">
                    <div class="exec-photo mx-auto mb-3">
                        <img src="${brother.photo}" alt="${brother.name} headshot">
                    </div>
                    <h5 class="fw-bold mb-1">${brother.name}</h5>
                    <p class="text-muted mb-2">${brother.year} · ${brother.major}</p>
                    <p class="mb-3">${brother.description}</p>
                    <div class="badges-display">${badgesHtml}</div>
                </div>
            </div>
        `;

        rosterGrid.appendChild(card);
    });
};

const renderMatches = (matches, pnmName) => {
    resultsGrid.innerHTML = '';

    if (matches.length === 0) {
        resultsGrid.innerHTML = `
            <div class="match-empty">
                <h5 class="fw-bold mb-2">No matches yet</h5>
                <p class="text-muted mb-0">Complete the form to see your best-fit brothers.</p>
            </div>
        `;
        return;
    }

    matches.forEach((match) => {
        const brother = match.brother;
        const score = Math.round(match.score * 100);
        const badgesHtml = (brother.badges || [])
            .map((badgeId) => createBadgePill(badgeIndex[badgeId], 'badge-pill-card'))
            .join('');
        const calendarLink = generateCalendarLink(pnmName, brother.name);

        const card = document.createElement('div');
        card.className = 'col-12 col-md-6 col-lg-4';
        card.innerHTML = `
            <div class="card h-100 match-card">
                <div class="card-body text-center p-4">
                    <div class="match-score mb-2">${score}% match</div>
                    <div class="exec-photo mx-auto mb-3">
                        <img src="${brother.photo}" alt="${brother.name} headshot">
                    </div>
                    <h5 class="fw-bold mb-1">${brother.name}</h5>
                    <p class="text-muted mb-2">${brother.year} · ${brother.major}</p>
                    <p class="mb-3">${brother.description}</p>
                    <div class="badges-display-prominent-card">${badgesHtml}</div>
                    <a class="btn btn-primary w-100 mt-3" href="${calendarLink}" target="_blank" rel="noopener">
                        Schedule a coffee chat
                    </a>
                </div>
            </div>
        `;

        resultsGrid.appendChild(card);
    });
};

const generateCalendarLink = (pnmName, brotherName) => {
    const title = encodeURIComponent(`Coffee Chat: ${pnmName} & ${brotherName}`);
    const details = encodeURIComponent(
        `Coffee chat between ${pnmName} (PNM) and ${brotherName} (Brother).`
    );
    return `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&details=${details}`;
};

const buildMatches = (pnmProfile) => {
    const pnmText = buildProfileText(pnmProfile, badgeIndex);
    const pnmVector = vectorize(tokenize(pnmText));

    const scored = brotherData.map((brother) => {
        const brotherText = buildProfileText(brother, badgeIndex);
        const brotherVector = vectorize(tokenize(brotherText));
        return {
            brother,
            score: cosineSimilarity(pnmVector, brotherVector)
        };
    });

    return scored
        .sort((a, b) => b.score - a.score)
        .slice(0, 3);
};

const loadMatchmakingData = () => {
    fetch('data/matchmaking.json')
        .then((response) => {
            if (!response.ok) {
                throw new Error('Failed to load matchmaking data.');
            }
            return response.json();
        })
        .then((data) => {
            badgeIndex = data.badges.reduce((acc, badge) => {
                acc[badge.id] = badge;
                return acc;
            }, {});
            brotherData = data.brothers;

            renderBadgeCheckboxes(data.badges);
            renderBrotherRoster(brotherData);
        })
        .catch(() => {
            if (resultsNote) {
                resultsNote.textContent = 'Unable to load matchmaking data right now.';
                resultsNote.classList.remove('d-none');
            }
        });
};

if (matchmakingForm) {
    loadMatchmakingData();

    matchmakingForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(matchmakingForm);
        const selectedBadges = formData.getAll('badges');
        const pnmName = formData.get('pnmName') || 'PNM';

        const profile = {
            name: pnmName,
            year: formData.get('pnmYear') || '',
            major: formData.get('pnmMajor') || '',
            description: formData.get('pnmDescription') || '',
            badges: selectedBadges
        };

        const matches = buildMatches(profile);
        renderMatches(matches, pnmName);
    });

    renderMatches([], 'PNM');
}
