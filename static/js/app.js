/**
 * Main application controller
 */
class TodoApp {
    constructor() {
        this.api = new TodoAPI();
        this.ui = new TodoUI('todo-list');
        this.init();
    }

    init() {
        this.setupFormHandler();
        this.setupEventDelegation();
        this.loadTodos();
    }

    setupFormHandler() {
        const form = document.getElementById('todo-form');
        if (!form) return;

        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(form);
            const title = formData.get('title')?.trim() || form.querySelector('#title')?.value.trim();
            const description = formData.get('description')?.trim() || form.querySelector('#description')?.value.trim();

            if (!title || !description) return;

            try {
                await this.api.create(title, description);
                this.ui.clearForm('todo-form');
                await this.loadTodos();
            } catch (error) {
                console.error('Failed to create todo:', error);
                alert('할 일 추가에 실패했습니다.');
            }
        });
    }

    setupEventDelegation() {
        const container = this.ui.container;
        
        // Checkbox toggle
        container.addEventListener('change', async (event) => {
            if (event.target.type === 'checkbox') {
                const todoId = parseInt(event.target.dataset.todoId);
                const completed = event.target.checked;
                try {
                    await this.api.update(todoId, { completed });
                    await this.loadTodos();
                } catch (error) {
                    console.error('Failed to update todo:', error);
                    alert('상태 변경에 실패했습니다.');
                }
            }
        });

        // Delete button
        container.addEventListener('click', async (event) => {
            if (event.target.classList.contains('danger')) {
                const todoId = parseInt(event.target.dataset.todoId);
                if (confirm('정말 삭제하시겠습니까?')) {
                    try {
                        await this.api.delete(todoId);
                        await this.loadTodos();
                    } catch (error) {
                        console.error('Failed to delete todo:', error);
                        alert('삭제에 실패했습니다.');
                    }
                }
            }
        });
    }

    async loadTodos() {
        try {
            const todos = await this.api.list();
            this.ui.renderTodos(todos);
        } catch (error) {
            console.error('Failed to load todos:', error);
            this.ui.container.innerHTML = '<li style="color: var(--danger); padding: 20px; text-align: center;">할 일 목록을 불러올 수 없습니다.</li>';
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new TodoApp();
});

