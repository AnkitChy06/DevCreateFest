// Social features service
class SocialService {
    static async getConnections(status = null) {
        try {
            const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.social.connections}${status ? `?status=${status}` : ''}`;
            const response = await fetch(url, {
                headers: AuthService.getHeaders()
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to fetch connections');

            return data.connections;
        } catch (error) {
            console.error('Error fetching connections:', error);
            throw error;
        }
    }

    static async sendConnectionRequest(friendId) {
        try {
            const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.social.connections}`, {
                method: 'POST',
                headers: AuthService.getHeaders(),
                body: JSON.stringify({ friend_id: friendId })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to send connection request');

            return data;
        } catch (error) {
            console.error('Error sending connection request:', error);
            throw error;
        }
    }

    static async acceptConnection(friendId) {
        try {
            const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.social.connections}/accept`, {
                method: 'POST',
                headers: AuthService.getHeaders(),
                body: JSON.stringify({ friend_id: friendId })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to accept connection');

            return data;
        } catch (error) {
            console.error('Error accepting connection:', error);
            throw error;
        }
    }

    static async getNotifications(unreadOnly = false, page = 1) {
        try {
            const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.social.notifications}?unread=${unreadOnly}&page=${page}`;
            const response = await fetch(url, {
                headers: AuthService.getHeaders()
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to fetch notifications');

            return data;
        } catch (error) {
            console.error('Error fetching notifications:', error);
            throw error;
        }
    }
}

// UI Components for Social Features
class SocialUI {
    static async renderConnections(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        try {
            const [accepted, pending] = await Promise.all([
                SocialService.getConnections('accepted'),
                SocialService.getConnections('pending')
            ]);

            container.innerHTML = `
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
                    <!-- Accepted Connections -->
                    <div class="bg-white rounded-xl shadow-lg p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-4">Your Connections</h3>
                        <div class="space-y-4">
                            ${accepted.length ? accepted.map(connection => `
                                <div class="flex items-center justify-between p-4 border rounded-lg">
                                    <div class="flex items-center space-x-4">
                                        <div class="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
                                            <span class="text-xl">👤</span>
                                        </div>
                                        <div>
                                            <h4 class="font-semibold text-gray-800">${connection.username}</h4>
                                            <p class="text-sm text-gray-500">Connected ${connection.connected_since}</p>
                                        </div>
                                    </div>
                                    <button onclick="SocialUI.viewProfile(${connection.user_id})"
                                        class="text-blue-500 hover:text-blue-600">
                                        View Profile
                                    </button>
                                </div>
                            `).join('') : `
                                <p class="text-gray-500 text-center">No connections yet</p>
                            `}
                        </div>
                    </div>

                    <!-- Pending Requests -->
                    <div class="bg-white rounded-xl shadow-lg p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-4">Pending Requests</h3>
                        <div class="space-y-4">
                            ${pending.length ? pending.map(request => `
                                <div class="flex items-center justify-between p-4 border rounded-lg">
                                    <div class="flex items-center space-x-4">
                                        <div class="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
                                            <span class="text-xl">👤</span>
                                        </div>
                                        <div>
                                            <h4 class="font-semibold text-gray-800">${request.username}</h4>
                                            <p class="text-sm text-gray-500">Request pending</p>
                                        </div>
                                    </div>
                                    <button onclick="SocialUI.acceptRequest(${request.user_id})"
                                        class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600">
                                        Accept
                                    </button>
                                </div>
                            `).join('') : `
                                <p class="text-gray-500 text-center">No pending requests</p>
                            `}
                        </div>
                    </div>
                </div>
            `;
        } catch (error) {
            container.innerHTML = `
                <div class="p-6 text-center">
                    <p class="text-red-500">Error loading social connections: ${error.message}</p>
                </div>
            `;
        }
    }

    static async viewProfile(userId) {
        // Implement profile viewing functionality
        console.log('Viewing profile:', userId);
    }

    static async acceptRequest(friendId) {
        try {
            await SocialService.acceptConnection(friendId);
            showSuccess('Connection request accepted!');
            this.renderConnections('social-container'); // Refresh the connections list
        } catch (error) {
            showError(error.message);
        }
    }
}