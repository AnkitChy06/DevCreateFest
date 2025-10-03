// API Service for eco-related features
class EcoService {
    static async logAction(actionId, quantity = 1) {
        try {
            const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.eco.actions}`, {
                method: 'POST',
                headers: AuthService.getHeaders(),
                body: JSON.stringify({ action_id: actionId, quantity })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to log eco action');

            return data;
        } catch (error) {
            console.error('Error logging eco action:', error);
            throw error;
        }
    }

    static async getUserImpact() {
        try {
            const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.eco.impact}`, {
                headers: AuthService.getHeaders()
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to fetch impact data');

            return data;
        } catch (error) {
            console.error('Error fetching user impact:', error);
            throw error;
        }
    }

    static async createProject(projectData) {
        try {
            const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.eco.projects}`, {
                method: 'POST',
                headers: AuthService.getHeaders(),
                body: JSON.stringify(projectData)
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to create project');

            return data;
        } catch (error) {
            console.error('Error creating project:', error);
            throw error;
        }
    }

    static async getAchievements() {
        try {
            const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.eco.achievements}`, {
                headers: AuthService.getHeaders()
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to fetch achievements');

            return data.achievements;
        } catch (error) {
            console.error('Error fetching achievements:', error);
            throw error;
        }
    }
}

// UI Components for Eco Features
class EcoUI {
    static async renderDashboard(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        try {
            const [impact, achievements] = await Promise.all([
                EcoService.getUserImpact(),
                EcoService.getAchievements()
            ]);

            container.innerHTML = `
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
                    <!-- Impact Stats -->
                    <div class="bg-white rounded-xl shadow-lg p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-4">Your Environmental Impact</h3>
                        <div class="space-y-4">
                            <div class="flex justify-between items-center">
                                <span class="text-gray-600">Total Impact:</span>
                                <span class="font-bold text-green-600">${impact.total_impact.toFixed(2)} units</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="text-gray-600">Actions Taken:</span>
                                <span class="font-bold text-blue-600">${impact.actions_taken}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Achievements -->
                    <div class="bg-white rounded-xl shadow-lg p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-4">Recent Achievements</h3>
                        <div class="space-y-4">
                            ${achievements.slice(0, 3).map(achievement => `
                                <div class="flex items-center space-x-4">
                                    <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
                                        <span class="text-2xl">🏆</span>
                                    </div>
                                    <div>
                                        <h4 class="font-bold text-gray-800">${achievement.name}</h4>
                                        <p class="text-sm text-gray-600">${achievement.description}</p>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- Action Logger -->
                    <div class="bg-white rounded-xl shadow-lg p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-4">Log Eco Action</h3>
                        <form id="ecoActionForm" class="space-y-4">
                            <div>
                                <label class="block text-gray-700 mb-2">Action Type</label>
                                <select name="actionId" class="w-full p-2 border rounded-lg">
                                    <option value="1">Recycle Paper</option>
                                    <option value="2">Save Energy</option>
                                    <option value="3">Plant a Tree</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-gray-700 mb-2">Quantity</label>
                                <input type="number" name="quantity" min="1" value="1" 
                                    class="w-full p-2 border rounded-lg">
                            </div>
                            <button type="submit" 
                                class="w-full bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600">
                                Log Action
                            </button>
                        </form>
                    </div>
                </div>
            `;

            // Add event listener for the form
            const form = document.getElementById('ecoActionForm');
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(form);
                try {
                    await EcoService.logAction(
                        parseInt(formData.get('actionId')),
                        parseInt(formData.get('quantity'))
                    );
                    showSuccess('Eco action logged successfully!');
                    EcoUI.renderDashboard(containerId); // Refresh the dashboard
                } catch (error) {
                    showError(error.message);
                }
            });
        } catch (error) {
            container.innerHTML = `
                <div class="p-6 text-center">
                    <p class="text-red-500">Error loading eco dashboard: ${error.message}</p>
                </div>
            `;
        }
    }
}