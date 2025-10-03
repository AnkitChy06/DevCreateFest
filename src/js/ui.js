// UI Helper functions and global components
const UIHelpers = {
    showMessage(message, type = 'success') {
        const alertClass = type === 'success' ? 'bg-green-500' : 'bg-red-500';
        const alert = document.createElement('div');
        alert.className = `fixed top-4 right-4 ${alertClass} text-white px-6 py-3 rounded-lg font-bold z-50 animate-fade-in-down`;
        alert.textContent = message;

        document.body.appendChild(alert);
        setTimeout(() => {
            alert.classList.add('animate-fade-out-up');
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    },

    showSuccess(message) {
        this.showMessage(message, 'success');
    },

    showError(message) {
        this.showMessage(message, 'error');
    },

    createLoader() {
        return `
            <div class="flex items-center justify-center p-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
            </div>
        `;
    },

    formatDate(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    formatTime(date) {
        return new Date(date).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    initializeNavigation() {
        document.addEventListener('DOMContentLoaded', () => {
            const navLinks = document.querySelectorAll('[data-page]');
            navLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const pageId = link.dataset.page;
                    this.navigateToPage(pageId);
                });
            });

            // Initialize notifications badge
            this.updateNotificationsBadge();
            // Start polling for notifications
            this.startNotificationPolling();
        });
    },

    async navigateToPage(pageId) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.add('hidden');
        });

        // Show selected page
        const selectedPage = document.getElementById(pageId);
        if (!selectedPage) return;

        selectedPage.classList.remove('hidden');

        // Initialize page content
        switch (pageId) {
            case 'eco-dashboard':
                await EcoUI.renderDashboard('eco-content');
                break;
            case 'learning':
                await LearningUI.renderDashboard('learning-content');
                break;
            case 'social':
                await SocialUI.renderConnections('social-content');
                break;
            case 'analytics':
                await AnalyticsUI.renderUserDashboard('analytics-content');
                break;
        }
    },

    async updateNotificationsBadge() {
        try {
            const { unread_count } = await SocialService.getNotifications(true);
            const badge = document.getElementById('notifications-badge');
            if (badge) {
                badge.textContent = unread_count;
                badge.classList.toggle('hidden', unread_count === 0);
            }
        } catch (error) {
            console.error('Error updating notifications:', error);
        }
    },

    startNotificationPolling() {
        setInterval(() => this.updateNotificationsBadge(), 30000); // Check every 30 seconds
    },

    registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', async () => {
                try {
                    const registration = await navigator.serviceWorker.register('/sw.js');
                    console.log('ServiceWorker registration successful');
                } catch (error) {
                    console.error('ServiceWorker registration failed:', error);
                }
            });
        }
    }
};

// Initialize UI helpers when document is ready
document.addEventListener('DOMContentLoaded', () => {
    UIHelpers.initializeNavigation();
    UIHelpers.registerServiceWorker();
});