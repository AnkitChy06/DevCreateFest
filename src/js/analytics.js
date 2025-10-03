// Analytics Service
class AnalyticsService {
    static async getUserAnalytics(userId) {
        try {
            const url = API_CONFIG.endpoints.analytics.user.replace('{id}', userId);
            const response = await fetch(`${API_CONFIG.baseUrl}${url}`, {
                headers: AuthService.getHeaders()
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to fetch user analytics');

            return data;
        } catch (error) {
            console.error('Error fetching user analytics:', error);
            throw error;
        }
    }

    static async getSchoolAnalytics(schoolId) {
        try {
            const url = API_CONFIG.endpoints.analytics.school.replace('{id}', schoolId);
            const response = await fetch(`${API_CONFIG.baseUrl}${url}`, {
                headers: AuthService.getHeaders()
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to fetch school analytics');

            return data;
        } catch (error) {
            console.error('Error fetching school analytics:', error);
            throw error;
        }
    }
}

// UI Components for Analytics
class AnalyticsUI {
    static formatNumber(number) {
        return new Intl.NumberFormat().format(number);
    }

    static createChart(ctx, data, options) {
        return new Chart(ctx, {
            ...options,
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                ...options.chartOptions
            }
        });
    }

    static async renderUserDashboard(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        try {
            const user = AuthService.getUser();
            const analytics = await AnalyticsService.getUserAnalytics(user.id);

            container.innerHTML = `
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
                    <!-- Activity Overview -->
                    <div class="bg-white rounded-xl shadow-lg p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-6">Activity Overview</h3>
                        <div class="grid grid-cols-2 gap-4">
                            <div class="text-center p-4 bg-green-50 rounded-lg">
                                <p class="text-sm text-gray-600">Eco Actions</p>
                                <p class="text-2xl font-bold text-green-600">
                                    ${this.formatNumber(analytics.eco_actions.week)}
                                </p>
                                <p class="text-xs text-gray-500">This Week</p>
                            </div>
                            <div class="text-center p-4 bg-blue-50 rounded-lg">
                                <p class="text-sm text-gray-600">Learning Progress</p>
                                <p class="text-2xl font-bold text-blue-600">
                                    ${this.formatNumber(analytics.learning.modules_completed_week)}
                                </p>
                                <p class="text-xs text-gray-500">Modules this Week</p>
                            </div>
                        </div>
                        <canvas id="activityChart" class="mt-6" height="200"></canvas>
                    </div>

                    <!-- Monthly Progress -->
                    <div class="bg-white rounded-xl shadow-lg p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-6">Monthly Overview</h3>
                        <div class="space-y-4">
                            <div>
                                <div class="flex justify-between text-sm text-gray-600 mb-1">
                                    <span>Eco Actions</span>
                                    <span>${analytics.eco_actions.month} actions</span>
                                </div>
                                <div class="h-2 bg-gray-200 rounded-full">
                                    <div class="h-full bg-green-500 rounded-full transition-all" 
                                        style="width: ${(analytics.eco_actions.month / 100) * 100}%">
                                    </div>
                                </div>
                            </div>
                            <div>
                                <div class="flex justify-between text-sm text-gray-600 mb-1">
                                    <span>Learning Progress</span>
                                    <span>${analytics.learning.modules_completed_month} modules</span>
                                </div>
                                <div class="h-2 bg-gray-200 rounded-full">
                                    <div class="h-full bg-blue-500 rounded-full transition-all" 
                                        style="width: ${(analytics.learning.modules_completed_month / 20) * 100}%">
                                    </div>
                                </div>
                            </div>
                        </div>
                        <canvas id="monthlyChart" class="mt-6" height="200"></canvas>
                    </div>
                </div>
            `;

            // Initialize charts
            this.initializeCharts(analytics);
        } catch (error) {
            container.innerHTML = `
                <div class="p-6 text-center">
                    <p class="text-red-500">Error loading analytics dashboard: ${error.message}</p>
                </div>
            `;
        }
    }

    static initializeCharts(analytics) {
        // Activity Chart
        const activityCtx = document.getElementById('activityChart').getContext('2d');
        this.createChart(activityCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [
                    {
                        label: 'Eco Actions',
                        data: analytics.eco_actions.daily,
                        borderColor: '#10B981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        tension: 0.4
                    }
                ]
            },
            chartOptions: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // Monthly Chart
        const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
        this.createChart(monthlyCtx, {
            type: 'bar',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                datasets: [
                    {
                        label: 'Eco Actions',
                        data: analytics.eco_actions.weekly,
                        backgroundColor: '#10B981'
                    },
                    {
                        label: 'Modules Completed',
                        data: analytics.learning.weekly,
                        backgroundColor: '#3B82F6'
                    }
                ]
            },
            chartOptions: {
                scales: {
                    y: {
                        beginAtZero: true,
                        stacked: true
                    },
                    x: {
                        stacked: true
                    }
                }
            }
        });
    }
}