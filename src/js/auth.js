// API Configuration
const API_CONFIG = {
    baseUrl: 'http://127.0.0.1:5000/api',
    endpoints: {
        auth: {
            login: '/auth/login',
            register: '/auth/register',
            me: '/auth/me'
        },
        eco: {
            actions: '/eco/actions',
            impact: '/eco/impact',
            projects: '/eco/projects',
            achievements: '/eco/achievements'
        },
        learning: {
            progress: '/learning/progress',
            complete: '/learning/modules/{id}/complete',
            recommended: '/learning/modules/recommended'
        },
        social: {
            connections: '/social/connections',
            notifications: '/social/notifications'
        },
        analytics: {
            user: '/analytics/user/{id}',
            school: '/analytics/school/{id}'
        }
    }
};

// Authentication Service
class AuthService {
    static token = localStorage.getItem('token');
    static user = JSON.parse(localStorage.getItem('user'));

    static getHeaders() {
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`
        };
    }

    static async login(email, password) {
        try {
            const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.auth.login}`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Login failed');

            this.token = data.access_token;
            localStorage.setItem('token', this.token);
            
            await this.fetchUserProfile();
            return true;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    static async register(userData) {
        try {
            const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.auth.register}`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Registration failed');

            return true;
        } catch (error) {
            console.error('Registration error:', error);
            throw error;
        }
    }

    static async fetchUserProfile() {
        try {
            const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.auth.me}`, {
                headers: this.getHeaders()
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to fetch user profile');

            this.user = data;
            localStorage.setItem('user', JSON.stringify(data));
            return data;
        } catch (error) {
            console.error('Profile fetch error:', error);
            throw error;
        }
    }

    static logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/';
    }

    static isAuthenticated() {
        return !!this.token;
    }

    static getUser() {
        return this.user;
    }
}