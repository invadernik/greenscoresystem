/**
 * GreenScore - Frontend Application
 * Handles API communication and dynamic UI updates
 * Includes offline fallback with mock data
 */

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

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

// ==================== FALLBACK MOCK DATA ====================
// Used when backend is not available

const MOCK_TRANSACTIONS = [
    { id: "TXN001", description: "Metro Rail Monthly Pass", amount: 1500, category: "Transport", date: "2026-01-10", eco_impact: 5, reasoning: "Public transport reduces carbon emissions" },
    { id: "TXN002", description: "Electric Vehicle Charging", amount: 450, category: "Transport", date: "2026-01-09", eco_impact: 4, reasoning: "EV supports clean energy transition" },
    { id: "TXN003", description: "Organic Grocery Shopping", amount: 2300, category: "Food", date: "2026-01-08", eco_impact: 3, reasoning: "Organic farming supports soil health" },
    { id: "TXN004", description: "Fast Fashion Purchase", amount: 4500, category: "Shopping", date: "2026-01-07", eco_impact: -4, reasoning: "Fast fashion contributes to textile waste" },
    { id: "TXN005", description: "Solar Panel Installation EMI", amount: 8500, category: "Utilities", date: "2026-01-06", eco_impact: 5, reasoning: "Solar reduces fossil fuel dependency" },
    { id: "TXN006", description: "Flight Ticket - Domestic", amount: 7500, category: "Transport", date: "2026-01-05", eco_impact: -5, reasoning: "Air travel has high carbon emissions" },
    { id: "TXN007", description: "Plant-Based Restaurant", amount: 850, category: "Food", date: "2026-01-04", eco_impact: 4, reasoning: "Plant-based meals have lower footprint" },
    { id: "TXN008", description: "Ride Share - Carpool", amount: 250, category: "Transport", date: "2026-01-03", eco_impact: 3, reasoning: "Carpooling reduces per-person emissions" },
    { id: "TXN009", description: "Electricity Bill Payment", amount: 3200, category: "Utilities", date: "2026-01-02", eco_impact: 0, reasoning: "Standard utility payment" },
    { id: "TXN010", description: "Petrol Fuel Purchase", amount: 5000, category: "Transport", date: "2026-01-01", eco_impact: -4, reasoning: "Fossil fuel contributes to emissions" },
    { id: "TXN011", description: "Thrift Store Shopping", amount: 1200, category: "Shopping", date: "2025-12-30", eco_impact: 4, reasoning: "Second-hand reduces manufacturing demand" },
    { id: "TXN012", description: "Digital Subscription - Netflix", amount: 649, category: "Entertainment", date: "2025-12-29", eco_impact: 1, reasoning: "Digital has lower footprint than physical" },
    { id: "TXN013", description: "Charity Donation - Tree Plantation", amount: 2000, category: "Donations", date: "2025-12-28", eco_impact: 5, reasoning: "Direct contribution to carbon sequestration" },
    { id: "TXN014", description: "Plastic Bottled Water - Bulk", amount: 800, category: "Food", date: "2025-12-27", eco_impact: -3, reasoning: "Single-use plastic causes pollution" },
    { id: "TXN015", description: "Bicycle Purchase", amount: 12000, category: "Transport", date: "2025-12-26", eco_impact: 5, reasoning: "Zero-emission transportation" },
    { id: "TXN016", description: "UPI Payment - Local Vendor", amount: 150, category: "Food", date: "2025-12-25", eco_impact: 2, reasoning: "Digital payments and local sourcing" }
];

// State
let allTransactions = [];
let currentFilter = 'all';
let isOfflineMode = false;

// ==================== Initialization ====================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});

async function initializeApp() {
    try {
        // Try to load from API first
        const scoreData = await fetchAPI('/score');

        // If we get here, API is working
        updateScoreDisplay(scoreData);
        updateESGDisplay(scoreData.esg);

        const txnData = await fetchAPI('/transactions');
        allTransactions = txnData.transactions;
        renderTransactions(allTransactions);

        const insightsData = await fetchAPI('/insights');
        renderInsights(insightsData);

        const incentivesData = await fetchAPI('/incentives');
        renderIncentives(incentivesData);
        renderTier(incentivesData);

        // Initialize charts after data is loaded
        initializeCharts();

    } catch (error) {
        console.warn('Backend not available, using offline mode:', error.message);
        isOfflineMode = true;
        showOfflineNotice();
        loadOfflineData();
    }
}

function loadOfflineData() {
    // Use mock data when backend is unavailable
    allTransactions = MOCK_TRANSACTIONS;

    // Calculate score from mock data
    const totalImpact = allTransactions.reduce((sum, t) => sum + t.eco_impact, 0);
    const score = Math.max(0, Math.min(100, 50 + totalImpact * 2));
    const status = score >= 71 ? 'high' : score >= 41 ? 'medium' : 'low';

    // Update score display
    updateScoreDisplay({
        score: score,
        status: status,
        explanation: "🔌 Demo Mode: Showing sample data. Start backend for live data.",
        total_transactions: allTransactions.length,
        net_impact: totalImpact
    });

    // Update ESG display
    updateESGDisplay({
        environmental: 68,
        social: 55,
        governance: 60
    });

    // Render transactions
    renderTransactions(allTransactions);

    // Render mock insights
    renderInsights({
        summary: "📊 Demo Mode: This is sample data showing how GreenScore analyzes your spending patterns.",
        highlights: [
            { icon: "🌟", title: "Top Choice: Metro Pass", description: "Public transport is excellent for sustainability!" },
            { icon: "🏆", title: "Great Progress", description: "Multiple eco-friendly transactions detected" }
        ],
        recommendations: [
            { priority: "medium", icon: "🚇", title: "Keep Using Public Transport", action: "Your metro usage is great! Consider extending to other trips.", potential_impact: "+5 points" },
            { priority: "high", icon: "✈️", title: "Reduce Air Travel", action: "Consider trains for shorter distances when possible.", potential_impact: "+10 points" },
            { priority: "low", icon: "🛒", title: "Shop Sustainably", action: "Great job with thrift shopping! Keep it up.", potential_impact: "Maintain score" }
        ]
    });

    // Render mock incentives
    const tier = { tier_id: "silver", tier_name: "Silver Green", badge: "🥈", min_score: 50, max_score: 69 };
    document.getElementById('tierBadge').textContent = tier.badge;
    document.getElementById('tierName').textContent = tier.tier_name;
    document.getElementById('tierRange').textContent = `Score: ${tier.min_score} - ${tier.max_score}`;
    document.getElementById('tierProgress').style.width = '60%';
    document.getElementById('nextTierText').textContent = "Earn 4 more points to unlock Gold Green!";
    document.getElementById('monthlyValue').textContent = "₹500 - ₹1,500";

    renderIncentives({
        current_tier: tier,
        estimated_monthly_value: "₹500 - ₹1,500",
        incentives: [
            { id: "cashback", name: "Green Cashback", description: "Cashback on eco purchases", icon: "💰", eligible: true, benefits: { rate: "1.5%" } },
            { id: "green_loan", name: "Green Loan Benefits", description: "Reduced interest rates", icon: "🏦", eligible: true, benefits: { rate_reduction: "0.75%" } },
            { id: "rewards", name: "Green Rewards", description: "Bonus reward points", icon: "🎁", eligible: true, benefits: { multiplier: "1.5x" } },
            { id: "insurance", name: "Insurance Discount", description: "Premium discounts", icon: "🛡️", eligible: true, benefits: { discount: "5%" } }
        ],
        disclaimer: "⚠️ DEMO MODE: Backend not connected. These are simulated incentives for demonstration."
    });

    // Initialize charts with mock data
    initializeCharts();
}

function showOfflineNotice() {
    const notice = document.createElement('div');
    notice.id = 'offlineNotice';
    notice.innerHTML = `
        <span>⚠️ <strong>Demo Mode</strong> - Backend not connected</span>
        <span style="opacity: 0.9;">Start server: <code>cd backend && python main.py</code></span>
    `;
    notice.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #9D4EDD 0%, #7B2CBF 100%);
        color: white;
        padding: 12px 20px;
        text-align: center;
        z-index: 1000;
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        font-size: 0.9rem;
        box-shadow: 0 4px 20px rgba(157, 78, 221, 0.4);
    `;

    // Style the code element
    const style = document.createElement('style');
    style.textContent = `
        #offlineNotice code {
            background: rgba(255,255,255,0.2);
            padding: 2px 8px;
            border-radius: 4px;
            font-family: monospace;
        }
    `;
    document.head.appendChild(style);

    document.body.prepend(notice);

    // Add padding to container
    document.querySelector('.container').style.paddingTop = '70px';
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
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000); // 3 second timeout

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        return response.json();
    } catch (error) {
        clearTimeout(timeoutId);
        throw error;
    }
}

// ==================== Score ====================

async function loadScore() {
    try {
        const data = await fetchAPI('/score');
        updateScoreDisplay(data);
        updateESGDisplay(data.esg);
    } catch (error) {
        console.error('Failed to load score:', error);
        throw error;
    }
}

function updateScoreDisplay(data) {
    const { score, status, explanation, total_transactions, net_impact } = data;

    // Update score number with animation
    const scoreNumber = document.getElementById('scoreNumber');
    animateCounter(scoreNumber, score);

    // Update score ring
    const scoreRing = document.getElementById('scoreRing');
    const circumference = 2 * Math.PI * 85;
    const offset = circumference - (score / 100) * circumference;
    scoreRing.style.strokeDashoffset = offset;

    // Set ring color based on status
    const colors = {
        high: '#00D4AA',
        medium: '#FFD700',
        low: '#FF6B6B'
    };
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

    // Update score card class for styling
    const scoreCard = document.getElementById('scoreCard');
    scoreCard.className = `card score-card score-${status}`;
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

async function loadTransactions() {
    try {
        const data = await fetchAPI('/transactions');
        allTransactions = data.transactions;
        renderTransactions(allTransactions);
    } catch (error) {
        console.error('Failed to load transactions:', error);
        throw error;
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

    // Add tooltip with reasoning
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

// ==================== Insights ====================

async function loadInsights() {
    try {
        const data = await fetchAPI('/insights');
        renderInsights(data);
    } catch (error) {
        console.error('Failed to load insights:', error);
        throw error;
    }
}

function renderInsights(data) {
    // Summary
    document.getElementById('insightsSummary').textContent = data.summary;

    // Highlights
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

    // Recommendations
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

async function loadIncentives() {
    try {
        const data = await fetchAPI('/incentives');
        renderIncentives(data);
        renderTier(data);
    } catch (error) {
        console.error('Failed to load incentives:', error);
        throw error;
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

    // Monthly value
    if (data.estimated_monthly_value) {
        document.getElementById('monthlyValue').textContent = data.estimated_monthly_value;
    }

    // Disclaimer
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

    // Next tier progress
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

    // Destroy existing chart if any
    if (esgChart) {
        esgChart.destroy();
    }

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
                    ticks: {
                        stepSize: 25,
                        color: '#64748B',
                        backdropColor: 'transparent'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    angleLines: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    pointLabels: {
                        color: '#94A3B8',
                        font: { size: 11 }
                    }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function createCategoryChart() {
    const ctx = document.getElementById('categoryChart');
    if (!ctx || allTransactions.length === 0) return;

    // Aggregate data by category
    const categoryData = {};
    allTransactions.forEach(txn => {
        const cat = txn.category;
        if (!categoryData[cat]) {
            categoryData[cat] = { count: 0, totalImpact: 0 };
        }
        categoryData[cat].count++;
        categoryData[cat].totalImpact += txn.eco_impact;
    });

    const labels = Object.keys(categoryData);
    const impacts = labels.map(cat => categoryData[cat].totalImpact);
    const colors = impacts.map(val => val >= 0 ? '#00D4AA' : '#FF6B6B');

    // Destroy existing chart if any
    if (categoryChart) {
        categoryChart.destroy();
    }

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
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: { color: '#94A3B8' }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#94A3B8' }
                }
            },
            plugins: {
                legend: { display: false }
            }
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
        <h2 style="color: #FF6B6B; margin-bottom: 1rem;">⚠️ Connection Error</h2>
        <p style="color: #94A3B8;">${message}</p>
        <p style="color: #64748B; margin-top: 1rem; font-size: 0.9rem;">
            Run: <code style="background: #1e293b; padding: 0.25rem 0.5rem; border-radius: 4px;">
                cd backend && python main.py
            </code>
        </p>
    `;
    container.insertBefore(errorDiv, container.firstChild);
}

// ==================== Exports for Testing ====================

if (typeof module !== 'undefined') {
    module.exports = {
        fetchAPI,
        formatAmount,
        filterTransactions
    };
}
