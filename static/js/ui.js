/**
 * UI rendering and DOM manipulation
 */
class TodoUI {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) throw new Error(`Container #${containerId} not found`);
    }

    renderTodo(todo) {
        const li = document.createElement('li');
        li.className = 'item';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = !!todo.completed;
        checkbox.dataset.todoId = todo.id;

        const textWrap = document.createElement('div');
        const titleEl = document.createElement('div');
        titleEl.className = 'title';
        titleEl.textContent = todo.title;

        const descEl = document.createElement('div');
        descEl.className = 'desc';
        descEl.textContent = todo.description;
        if (todo.completed) {
            descEl.style.textDecoration = 'line-through';
        }

        textWrap.appendChild(titleEl);
        textWrap.appendChild(descEl);

        const spacer = document.createElement('div');
        spacer.className = 'spacer';

        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = '삭제';
        deleteBtn.className = 'danger';
        deleteBtn.dataset.todoId = todo.id;

        li.appendChild(checkbox);
        li.appendChild(textWrap);
        li.appendChild(spacer);
        li.appendChild(deleteBtn);

        return li;
    }

    renderTodos(todos) {
        this.container.innerHTML = '';
        todos.forEach(todo => {
            this.container.appendChild(this.renderTodo(todo));
        });
    }

    clearForm(formId) {
        const form = document.getElementById(formId);
        if (form) {
            form.reset();
        }
    }
}

