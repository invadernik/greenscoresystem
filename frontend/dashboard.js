/**
 * GreenScore - User Dashboard JavaScript
 * Handles user-specific data loading and display
 */

const API_BASE_URL = 'http://localhost:8001';

// Category Icons
const CATEGORY_ICONS = {
    'Transport': '🚗',
    'Food': '🍔',
    'Shopping': '🛍️',
    'Utilities': '⚡',
    'Entertainment': '🎬',
    'Donations': '💝',
    'Other': '📦'
};

// State
let currentUser = null;
let allTransactions = [];
let currentFilter = 'all';

// ==================== Initialization ====================

document.addEventListener('DOMContentLoaded', () => {
    initializeDashboard();
    setupEventListeners();
});

async function initializeDashboard() {
    // Get user ID from URL or session
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('user');

    if (!userId) {
        // No user specified, redirect to home
        window.location.href = 'home.html';
        return;
    }

    try {
        // Load user data
        currentUser = await fetchAPI(`/users/${userId}`);
        updateUserHeader(currentUser);
        updateNavigation(currentUser);

        // Store in session for navbar
        sessionStorage.setItem('currentUser', JSON.stringify(currentUser));

        // Load all user-specific data
        await Promise.all([
            loadUserScore(userId),
            loadUserTransactions(userId),
            loadUserInsights(userId),
            loadUserIncentives(userId),
            loadUserImprovements(userId)
        ]);

        // Initialize charts
        initializeCharts();

    } catch (error) {
        console.error('Failed to load user data:', error);
        showError('Failed to load user data. Please try again.');
    }
}

function setupEventListeners() {
    // Category filter tabs
    document.querySelectorAll('.filter-tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.category;
            filterTransactions(currentFilter);
        });
    });
}

// ==================== API Calls ====================

async function fetchAPI(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    if (!response.ok) throw new Error(`API Error: ${response.status}`);
    return response.json();
}

// ==================== User Header ====================

function updateUserHeader(user) {
    const avatar = document.getElementById('userAvatar');
    const fullName = document.getElementById('userFullName');
    const email = document.getElementById('userEmailDisplay');

    avatar.textContent = user.first_name.charAt(0) + user.last_name.charAt(0);
    avatar.style.background = user.avatar_color;
    fullName.textContent = user.full_name;
    email.textContent = user.email;

    // Update page title
    document.title = `${user.full_name} - GreenScore Dashboard`;
}

function updateNavigation(user) {
    const navUserName = document.getElementById('navUserName');
    navUserName.textContent = user.first_name;
}

// ==================== Score ====================

async function loadUserScore(userId) {
    try {
        const data = await fetchAPI(`/users/${userId}/score`);
        updateScoreDisplay(data);
        updateESGDisplay(data.esg);
    } catch (error) {
        console.error('Failed to load score:', error);
    }
}

function updateScoreDisplay(data) {
    const { score, status, explanation, total_transactions, net_impact } = data;

    // Animate score number
    const scoreNumber = document.getElementById('scoreNumber');
    animateCounter(scoreNumber, score);

    // Update score ring
    const scoreRing = document.getElementById('scoreRing');
    const circumference = 2 * Math.PI * 85;
    const offset = circumference - (score / 100) * circumference;
    scoreRing.style.strokeDashoffset = offset;

    // Set ring color based on status
    const colors = { high: '#00D4AA', medium: '#FFD700', low: '#FF6B6B' };
    scoreRing.style.stroke = colors[status] || colors.medium;

    // Update badge
    const badge = document.getElementById('scoreBadge');
    badge.textContent = status.toUpperCase();
    badge.className = `badge ${status}`;

    // Update explanation
    document.getElementById('scoreExplanation').textContent = explanation;

    // Update stats
    document.getElementById('totalTransactions').textContent = total_transactions;
    document.getElementById('netImpact').textContent = net_impact >= 0 ? `+${net_impact}` : net_impact;

    // Update score card class
    document.getElementById('scoreCard').className = `card score-card score-${status}`;
}

function updateESGDisplay(esg) {
    document.getElementById('esgEnvironmental').textContent = esg.environmental;
    document.getElementById('esgSocial').textContent = esg.social;
    document.getElementById('esgGovernance').textContent = esg.governance;
}

function animateCounter(element, target) {
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.round(current);
    }, 30);
}

// ==================== Transactions ====================

async function loadUserTransactions(userId) {
    try {
        const data = await fetchAPI(`/users/${userId}/transactions`);
        allTransactions = data.transactions;
        renderTransactions(allTransactions);
    } catch (error) {
        console.error('Failed to load transactions:', error);
    }
}

function renderTransactions(transactions) {
    const container = document.getElementById('transactionsList');
    container.innerHTML = '';

    if (transactions.length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted); text-align: center; padding: 2rem;">No transactions found</p>';
        return;
    }

    transactions.forEach(txn => {
        const item = createTransactionElement(txn);
        container.appendChild(item);
    });
}

function createTransactionElement(txn) {
    const div = document.createElement('div');
    div.className = 'transaction-item';

    const impactClass = txn.eco_impact > 0 ? 'positive' : txn.eco_impact < 0 ? 'negative' : 'neutral';
    const impactSign = txn.eco_impact > 0 ? '+' : '';

    div.innerHTML = `
        <div class="transaction-icon">${CATEGORY_ICONS[txn.category] || '📦'}</div>
        <div class="transaction-details">
            <div class="transaction-description">${txn.description}</div>
            <div class="transaction-meta">
                <span>${txn.category}</span>
                <span>•</span>
                <span>${txn.date}</span>
            </div>
        </div>
        <div class="transaction-amount">
            <div class="amount">₹${formatAmount(txn.amount)}</div>
            <div class="transaction-impact ${impactClass}">
                ${impactSign}${txn.eco_impact} eco
            </div>
        </div>
    `;

    div.title = txn.reasoning;
    return div;
}

function filterTransactions(category) {
    const filtered = category === 'all'
        ? allTransactions
        : allTransactions.filter(t => t.category === category);
    renderTransactions(filtered);
}

function formatAmount(amount) {
    return new Intl.NumberFormat('en-IN').format(amount);
}

// ==================== Improvements ====================

async function loadUserImprovements(userId) {
    try {
        const data = await fetchAPI(`/users/${userId}/improvements`);
        renderImprovements(data);
    } catch (error) {
        console.error('Failed to load improvements:', error);
    }
}

function renderImprovements(data) {
    const card = document.getElementById('improvementsCard');
    const list = document.getElementById('improvementsList');
    const intro = document.getElementById('improvementsIntro');

    if (!data.improvement_areas || data.improvement_areas.length === 0) {
        // No improvements needed - show success state
        card.classList.add('hidden');
        card.style.display = 'none';
        return;
    }

    // Show the card
    card.classList.remove('hidden');
    card.style.display = 'block';
    intro.textContent = data.message;

    list.innerHTML = data.improvement_areas.map(item => `
        <div class="improvement-item priority-${item.priority}">
            <div class="improvement-icon">${item.icon}</div>
            <div class="improvement-content">
                <div class="improvement-category">${item.category}</div>
                <div class="improvement-issue">${item.issue}</div>
                ${item.examples.length > 0 ? `
                    <div class="improvement-examples">
                        Examples: ${item.examples.join(', ')}
                    </div>
                ` : ''}
                <div class="improvement-suggestion">
                    💡 ${item.suggestion}
                </div>
            </div>
            <div class="improvement-potential">
                <div class="potential-label">Potential</div>
                <div class="potential-value">${item.potential_improvement}</div>
            </div>
        </div>
    `).join('');
}

// ==================== Insights ====================

async function loadUserInsights(userId) {
    const id = userId || currentUser?.id;
    if (!id) return;

    try {
        const data = await fetchAPI(`/users/${id}/insights`);
        renderInsights(data);
    } catch (error) {
        console.error('Failed to load insights:', error);
    }
}

function renderInsights(data) {
    document.getElementById('insightsSummary').textContent = data.summary;

    const highlightsContainer = document.getElementById('highlightsList');
    highlightsContainer.innerHTML = '';

    if (data.highlights && data.highlights.length > 0) {
        data.highlights.forEach(highlight => {
            const div = document.createElement('div');
            div.className = 'highlight-item';
            div.innerHTML = `
                <span class="highlight-icon">${highlight.icon}</span>
                <div class="highlight-content">
                    <h4>${highlight.title}</h4>
                    <p>${highlight.description}</p>
                </div>
            `;
            highlightsContainer.appendChild(div);
        });
    }

    const recsContainer = document.getElementById('recommendationsList');
    recsContainer.innerHTML = '';

    if (data.recommendations && data.recommendations.length > 0) {
        data.recommendations.forEach(rec => {
            const div = document.createElement('div');
            div.className = `recommendation-item priority-${rec.priority}`;
            div.innerHTML = `
                <span class="recommendation-icon">${rec.icon}</span>
                <div class="recommendation-content">
                    <h4>${rec.title}</h4>
                    <p>${rec.action}</p>
                </div>
                <div class="recommendation-impact">${rec.potential_impact}</div>
            `;
            recsContainer.appendChild(div);
        });
    }
}

// ==================== Incentives ====================

async function loadUserIncentives(userId) {
    try {
        const data = await fetchAPI(`/users/${userId}/incentives`);
        renderIncentives(data);
        renderTier(data);
    } catch (error) {
        console.error('Failed to load incentives:', error);
    }
}

function renderIncentives(data) {
    const container = document.getElementById('incentivesGrid');
    container.innerHTML = '';

    if (data.incentives && data.incentives.length > 0) {
        data.incentives.forEach(inc => {
            const div = document.createElement('div');
            div.className = `incentive-item ${inc.eligible ? '' : 'locked'}`;

            let benefitText = '';
            const benefits = inc.benefits;
            if (benefits.rate) benefitText = benefits.rate;
            else if (benefits.rate_reduction) benefitText = `-${benefits.rate_reduction} APR`;
            else if (benefits.multiplier) benefitText = `${benefits.multiplier} Points`;
            else if (benefits.discount) benefitText = `${benefits.discount} Off`;
            else if (benefits.boost) benefitText = `${benefits.boost} Limit`;

            div.innerHTML = `
                <div class="incentive-header">
                    <span class="incentive-icon">${inc.icon}</span>
                    <span class="incentive-name">${inc.name}</span>
                </div>
                <p class="incentive-description">${inc.description}</p>
                <div class="incentive-value">${inc.eligible ? benefitText : '🔒 Locked'}</div>
            `;
            container.appendChild(div);
        });
    }

    if (data.estimated_monthly_value) {
        document.getElementById('monthlyValue').textContent = data.estimated_monthly_value;
    }

    if (data.disclaimer) {
        document.getElementById('disclaimer').textContent = data.disclaimer;
    }
}

function renderTier(data) {
    if (!data.current_tier) return;

    const tier = data.current_tier;

    document.getElementById('tierBadge').textContent = tier.badge;
    document.getElementById('tierName').textContent = tier.tier_name;
    document.getElementById('tierRange').textContent = `Score: ${tier.min_score} - ${tier.max_score}`;

    if (data.next_tier) {
        const nextTier = data.next_tier;
        const progressBar = document.getElementById('tierProgress');
        const nextTierText = document.getElementById('nextTierText');

        if (nextTier.exists) {
            const currentScore = data.green_score || 0;
            const currentMin = tier.min_score;
            const nextMin = nextTier.min_score_required;
            const progress = ((currentScore - currentMin) / (nextMin - currentMin)) * 100;

            progressBar.style.width = `${Math.min(progress, 100)}%`;
            nextTierText.textContent = nextTier.message;
        } else {
            progressBar.style.width = '100%';
            nextTierText.textContent = nextTier.message;
        }
    }
}

// ==================== Charts ====================

let esgChart = null;
let categoryChart = null;

function initializeCharts() {
    createESGChart();
    createCategoryChart();
}

function createESGChart() {
    const ctx = document.getElementById('esgChart');
    if (!ctx) return;

    const esgE = parseInt(document.getElementById('esgEnvironmental').textContent) || 50;
    const esgS = parseInt(document.getElementById('esgSocial').textContent) || 50;
    const esgG = parseInt(document.getElementById('esgGovernance').textContent) || 50;

    if (esgChart) esgChart.destroy();

    esgChart = new Chart(ctx.getContext('2d'), {
        type: 'radar',
        data: {
            labels: ['Environmental', 'Social', 'Governance'],
            datasets: [{
                label: 'ESG Score',
                data: [esgE, esgS, esgG],
                backgroundColor: 'rgba(0, 212, 170, 0.2)',
                borderColor: '#00D4AA',
                borderWidth: 2,
                pointBackgroundColor: ['#00D4AA', '#00B4D8', '#9D4EDD'],
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { stepSize: 25, color: '#64748B', backdropColor: 'transparent' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                    pointLabels: { color: '#94A3B8', font: { size: 11 } }
                }
            },
            plugins: { legend: { display: false } }
        }
    });
}

function createCategoryChart() {
    const ctx = document.getElementById('categoryChart');
    if (!ctx || allTransactions.length === 0) return;

    const categoryData = {};
    allTransactions.forEach(txn => {
        const cat = txn.category;
        if (!categoryData[cat]) categoryData[cat] = { count: 0, totalImpact: 0 };
        categoryData[cat].count++;
        categoryData[cat].totalImpact += txn.eco_impact;
    });

    const labels = Object.keys(categoryData);
    const impacts = labels.map(cat => categoryData[cat].totalImpact);
    const colors = impacts.map(val => val >= 0 ? '#00D4AA' : '#FF6B6B');

    if (categoryChart) categoryChart.destroy();

    categoryChart = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total Eco Impact',
                data: impacts,
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 1,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            scales: {
                x: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94A3B8' } },
                y: { grid: { display: false }, ticks: { color: '#94A3B8' } }
            },
            plugins: { legend: { display: false } }
        }
    });
}

// ==================== Error Handling ====================

function showError(message) {
    const container = document.querySelector('.dashboard');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'card';
    errorDiv.style.gridColumn = 'span 12';
    errorDiv.style.textAlign = 'center';
    errorDiv.style.padding = '2rem';
    errorDiv.innerHTML = `
        <h2 style="color: #FF6B6B; margin-bottom: 1rem;">⚠️ Error</h2>
        <p style="color: #94A3B8;">${message}</p>
        <a href="home.html" style="color: var(--green-primary); display: inline-block; margin-top: 1rem;">← Back to Home</a>
    `;
    container.insertBefore(errorDiv, container.firstChild);
}
