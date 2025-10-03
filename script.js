// Backend API URL
const API_URL = 'http://127.0.0.1:5050/api';

// Current user ID (for demo purposes)
const CURRENT_USER_ID = 1;

// Fetch configuration for API calls
const fetchConfig = {
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
};

// Show success message
function showSuccess(message) {
    const successMsg = document.createElement('div');
    successMsg.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-full font-bold z-50';
    successMsg.textContent = message;
    document.body.appendChild(successMsg);
    setTimeout(() => {
        successMsg.remove();
    }, 3000);
}

// Show error message
function showError(message) {
    const errorMsg = document.createElement('div');
    errorMsg.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-full font-bold z-50';
    errorMsg.textContent = message;
    document.body.appendChild(errorMsg);
    setTimeout(() => {
        errorMsg.remove();
    }, 5000);
}

// Page Navigation
async function showPage(pageId) {
    try {
        console.log('Showing page:', pageId);
        // Hide all pages
        const pages = document.querySelectorAll('.page');
        pages.forEach(page => page.classList.add('hidden'));
        
        // Show selected page
        const selectedPage = document.getElementById(pageId);
        if (!selectedPage) {
            throw new Error(`Page "${pageId}" not found`);
        }
        selectedPage.classList.remove('hidden');
        
        // Update navigation active state
        const navButtons = document.querySelectorAll('nav button');
        navButtons.forEach(btn => {
            btn.classList.remove('text-green-600', 'font-bold');
            if (btn.getAttribute('onclick')?.includes(pageId)) {
                btn.classList.add('text-green-600', 'font-bold');
            }
        });

        // Load data based on the page
        if (pageId === 'dashboard') {
            await loadUserData();
        } else if (pageId === 'challenges') {
            await loadChallenges();
        } else if (pageId === 'leaderboard') {
            await loadLeaderboard();
        }
    } catch (error) {
        console.error('Error showing page:', error);
        showError('Failed to load page content');
    }
}

// Simulate progress animations
function animateProgress() {
    const progressBars = document.querySelectorAll('.progress-fill');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });
}

// Load user data from backend
async function loadUserData() {
    try {
        console.log('Fetching user data...');
        const response = await fetch(`${API_URL}/user/${CURRENT_USER_ID}`, fetchConfig);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const userData = await response.json();
        
        // Update user info in the dashboard
        document.querySelector('.points-display').textContent = `⭐ ${userData.points} pts`;
        const levelDisplay = document.querySelector('.level-display');
        if (levelDisplay) levelDisplay.textContent = `Level ${userData.level}`;
        const challengesCompleted = document.querySelector('.challenges-completed');
        if (challengesCompleted) challengesCompleted.textContent = userData.challenges_completed;
        
        animateProgress();
    } catch (error) {
        console.error('Error loading user data:', error);
        showError('Failed to load user data');
    }
}

// Load challenges from backend
async function loadChallenges() {
    try {
        console.log('Fetching challenges...');
        const response = await fetch(`${API_URL}/challenges`, fetchConfig);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const challenges = await response.json();
        
        const challengesContainer = document.querySelector('#challenges .grid');
        if (challengesContainer) {
            challengesContainer.innerHTML = challenges.map(challenge => `
                <div class="bg-white p-6 rounded-xl shadow-md card-hover">
                    <h3 class="text-xl font-bold mb-2">${challenge.title}</h3>
                    <p class="text-gray-600 mb-4">${challenge.description}</p>
                    <div class="flex justify-between items-center">
                        <span class="text-yellow-500 font-bold">⭐ ${challenge.points_reward} pts</span>
                        <button 
                            data-challenge-id="${challenge.id}"
                            class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-full">
                            Mark as Complete
                        </button>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading challenges:', error);
        showError('Failed to load challenges');
    }
}

// Load leaderboard data
async function loadLeaderboard() {
    try {
        console.log('Fetching leaderboard...');
        const response = await fetch(`${API_URL}/leaderboard`, fetchConfig);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const users = await response.json();
        
        const leaderboardContainer = document.querySelector('#leaderboard .leaderboard-list');
        if (leaderboardContainer) {
            leaderboardContainer.innerHTML = users.map((user, index) => `
                <div class="flex items-center justify-between p-4 ${index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}">
                    <div class="flex items-center space-x-4">
                        <span class="font-bold ${index < 3 ? 'text-yellow-500' : 'text-gray-500'}">#${index + 1}</span>
                        <span class="font-medium">${user.name}</span>
                    </div>
                    <div class="flex items-center space-x-4">
                        <span class="text-gray-600">Level ${user.level}</span>
                        <span class="font-bold text-yellow-500">⭐ ${user.points}</span>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading leaderboard:', error);
        showError('Failed to load leaderboard');
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded, initializing...');
    // Load initial user data and show landing page
    loadUserData().then(() => {
        showPage('landing');
    }).catch(error => {
        console.error('Error during initialization:', error);
        showError('Failed to initialize application');
    });
});