/**
 * GreenScore - Home Page JavaScript
 * Handles user listing, search, and navigation
 */

const API_BASE_URL = 'http://localhost:8001';

// State
let allUsers = [];
let filteredUsers = [];

// ==================== Initialization ====================

document.addEventListener('DOMContentLoaded', () => {
    loadUsers();
    setupSearchListeners();
    checkCurrentUser();
});

// ==================== API Calls ====================

async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) throw new Error(`API Error: ${response.status}`);
        return response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ==================== Load Users ====================

async function loadUsers() {
    const loadingState = document.getElementById('loadingState');
    const usersGrid = document.getElementById('usersGrid');
    const userCount = document.getElementById('userCount');

    try {
        const data = await fetchAPI('/users');
        allUsers = data.users;
        filteredUsers = allUsers;

        loadingState.style.display = 'none';
        renderUsers(filteredUsers);
        userCount.textContent = `${data.total} users available`;

    } catch (error) {
        console.error('Failed to load users:', error);
        loadingState.innerHTML = `
            <p style="color: var(--red-warning);">⚠️ Failed to connect to server</p>
            <p style="font-size: 0.85rem; margin-top: 0.5rem;">
                Run: <code style="background: #1e293b; padding: 0.25rem 0.5rem; border-radius: 4px;">
                    cd backend && python -m uvicorn main:app --reload
                </code>
            </p>
        `;
    }
}

// ==================== Render Users ====================

function renderUsers(users) {
    const grid = document.getElementById('usersGrid');
    const noResults = document.getElementById('noResults');

    if (users.length === 0) {
        grid.innerHTML = '';
        noResults.style.display = 'block';
        return;
    }

    noResults.style.display = 'none';

    grid.innerHTML = users.map(user => `
        <a href="dashboard.html?user=${user.id}" class="user-card" data-user-id="${user.id}">
            <div class="user-card-header">
                <div class="user-avatar" style="background: ${user.avatar_color}">
                    ${user.first_name.charAt(0)}${user.last_name.charAt(0)}
                </div>
                <div class="user-info">
                    <div class="user-name">${user.full_name}</div>
                    <div class="user-email">${user.email}</div>
                </div>
            </div>
            <div class="user-card-body">
                <div class="user-score">
                    <span class="score-badge ${user.score_status}">${user.green_score}</span>
                    <span style="color: var(--text-muted); font-size: 0.8rem;">GreenScore</span>
                </div>
                <div class="user-transactions">
                    ${user.total_transactions} txns
                </div>
            </div>
        </a>
    `).join('');

    // Add click handlers to store user in session
    document.querySelectorAll('.user-card').forEach(card => {
        card.addEventListener('click', (e) => {
            const userId = card.dataset.userId;
            const user = users.find(u => u.id === userId);
            if (user) {
                sessionStorage.setItem('currentUser', JSON.stringify(user));
            }
        });
    });
}

// ==================== Search ====================

function setupSearchListeners() {
    const searchInput = document.getElementById('searchInput');
    const searchClear = document.getElementById('searchClear');

    // Debounce search
    let debounceTimeout;
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();

        // Show/hide clear button
        searchClear.style.display = query ? 'block' : 'none';

        // Debounce the search
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            searchUsers(query);
        }, 200);
    });

    // Clear button
    searchClear.addEventListener('click', () => {
        searchInput.value = '';
        searchClear.style.display = 'none';
        filteredUsers = allUsers;
        renderUsers(filteredUsers);
        document.getElementById('userCount').textContent = `${allUsers.length} users available`;
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === '/' && document.activeElement !== searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
        if (e.key === 'Escape' && document.activeElement === searchInput) {
            searchInput.blur();
        }
    });
}

function searchUsers(query) {
    const userCount = document.getElementById('userCount');

    if (!query) {
        filteredUsers = allUsers;
        renderUsers(filteredUsers);
        userCount.textContent = `${allUsers.length} users available`;
        return;
    }

    const queryLower = query.toLowerCase();
    filteredUsers = allUsers.filter(user =>
        user.full_name.toLowerCase().includes(queryLower) ||
        user.email.toLowerCase().includes(queryLower) ||
        user.id.toLowerCase().includes(queryLower)
    );

    renderUsers(filteredUsers);
    userCount.textContent = `${filteredUsers.length} of ${allUsers.length} users`;
}

// ==================== Current User ====================

function checkCurrentUser() {
    const currentUser = sessionStorage.getItem('currentUser');
    if (currentUser) {
        const user = JSON.parse(currentUser);
        const navUserLink = document.getElementById('navUserLink');
        const navUserName = document.getElementById('navUserName');

        navUserLink.style.display = 'flex';
        navUserLink.href = `dashboard.html?user=${user.id}`;
        navUserName.textContent = user.first_name;
    }
}
