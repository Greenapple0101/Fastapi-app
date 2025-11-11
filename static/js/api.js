/**
 * API Client for Todo REST endpoints
 */
class TodoAPI {
    constructor(baseURL = '') {
        this.baseURL = baseURL;
    }

    async list() {
        const response = await fetch(`${this.baseURL}/todos`);
        if (!response.ok) throw new Error(`Failed to fetch todos: ${response.statusText}`);
        return response.json();
    }

    async get(id) {
        const response = await fetch(`${this.baseURL}/todos/${id}`);
        if (!response.ok) throw new Error(`Failed to fetch todo: ${response.statusText}`);
        return response.json();
    }

    async create(title, description) {
        const response = await fetch(`${this.baseURL}/todos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description })
        });
        if (!response.ok) throw new Error(`Failed to create todo: ${response.statusText}`);
        return response.json();
    }

    async update(id, updates) {
        const response = await fetch(`${this.baseURL}/todos/${id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updates)
        });
        if (!response.ok) throw new Error(`Failed to update todo: ${response.statusText}`);
        return response.json();
    }

    async delete(id) {
        const response = await fetch(`${this.baseURL}/todos/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error(`Failed to delete todo: ${response.statusText}`);
        return response.status === 204;
    }
}

