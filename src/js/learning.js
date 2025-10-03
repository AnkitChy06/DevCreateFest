// Learning Service for handling educational features
class LearningService {
    static async getProgress(pathId = null) {
        try {
            const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.learning.progress}${pathId ? `?path_id=${pathId}` : ''}`;
            const response = await fetch(url, {
                headers: AuthService.getHeaders()
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to fetch progress');

            return data;
        } catch (error) {
            console.error('Error fetching learning progress:', error);
            throw error;
        }
    }

    static async completeModule(moduleId) {
        try {
            const url = API_CONFIG.endpoints.learning.complete.replace('{id}', moduleId);
            const response = await fetch(`${API_CONFIG.baseUrl}${url}`, {
                method: 'POST',
                headers: AuthService.getHeaders()
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to complete module');

            return data;
        } catch (error) {
            console.error('Error completing module:', error);
            throw error;
        }
    }

    static async getRecommendations() {
        try {
            const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.learning.recommended}`, {
                headers: AuthService.getHeaders()
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to fetch recommendations');

            return data.recommendations;
        } catch (error) {
            console.error('Error fetching recommendations:', error);
            throw error;
        }
    }
}

// UI Components for Learning Features
class LearningUI {
    static async renderDashboard(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        try {
            const [progress, recommendations] = await Promise.all([
                LearningService.getProgress(),
                LearningService.getRecommendations()
            ]);

            container.innerHTML = `
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
                    <!-- Learning Paths Progress -->
                    <div class="bg-white rounded-xl shadow-lg p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-4">Your Learning Progress</h3>
                        <div class="space-y-6">
                            ${progress.map(path => `
                                <div class="space-y-2">
                                    <div class="flex justify-between items-center">
                                        <h4 class="font-semibold text-gray-700">${path.path_name}</h4>
                                        <span class="text-sm text-gray-500">
                                            ${path.completed_modules}/${path.total_modules} Completed
                                        </span>
                                    </div>
                                    <div class="h-2 bg-gray-200 rounded-full">
                                        <div class="h-full bg-green-500 rounded-full transition-all" 
                                            style="width: ${path.progress}%">
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- Recommended Modules -->
                    <div class="bg-white rounded-xl shadow-lg p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-4">Recommended for You</h3>
                        <div class="space-y-4">
                            ${recommendations.map(module => `
                                <div class="p-4 border rounded-lg ${module.prerequisites_completed ? 'hover:border-green-500' : 'opacity-75'}">
                                    <div class="flex justify-between items-start">
                                        <div>
                                            <h4 class="font-semibold text-gray-800">${module.module_name}</h4>
                                            <p class="text-sm text-gray-600">${module.description}</p>
                                        </div>
                                        ${module.prerequisites_completed ? `
                                            <button onclick="LearningUI.startModule(${module.module_id})"
                                                class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600">
                                                Start
                                            </button>
                                        ` : `
                                            <span class="text-sm text-yellow-600">
                                                Complete prerequisites first
                                            </span>
                                        `}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        } catch (error) {
            container.innerHTML = `
                <div class="p-6 text-center">
                    <p class="text-red-500">Error loading learning dashboard: ${error.message}</p>
                </div>
            `;
        }
    }

    static async startModule(moduleId) {
        try {
            // Here you would typically navigate to the module content page
            // For now, we'll just mark it as complete
            await LearningService.completeModule(moduleId);
            showSuccess('Module completed successfully!');
            this.renderDashboard('learning-container'); // Refresh the dashboard
        } catch (error) {
            showError(error.message);
        }
    }
}