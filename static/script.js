document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('task-form');
    const taskInput = document.getElementById('task-input');
    const taskList = document.getElementById('task-list');
    const errorAlert = document.getElementById('error-alert');

    const showError = (message) => {
        errorAlert.textContent = message;
        errorAlert.classList.remove('d-none');
    };

    const clearError = () => {
        errorAlert.textContent = '';
        errorAlert.classList.add('d-none');
    };

    const createTaskElement = (task) => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center bg-white border rounded-3 px-3 py-2';
        li.dataset.id = task.id;

        const span = document.createElement('span');
        span.textContent = task.title;

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn btn-sm btn-outline-danger';
        deleteBtn.textContent = 'Delete';
        deleteBtn.addEventListener('click', () => deleteTask(task.id, li));

        li.appendChild(span);
        li.appendChild(deleteBtn);
        return li;
    };

    const loadTasks = async () => {
        try {
            const response = await fetch('/api/tasks');
            if (!response.ok) throw new Error('Failed to load tasks');
            const data = await response.json();
            taskList.innerHTML = '';
            data.tasks.forEach((task) => taskList.appendChild(createTaskElement(task)));
        } catch (err) {
            showError(err.message);
        }
    };

    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearError();
        const title = taskInput.value.trim();
        if (!title) return;

        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to add task');

            taskList.appendChild(createTaskElement(data.task));
            taskInput.value = '';
        } catch (err) {
            showError(err.message);
        }
    });

    const deleteTask = async (id, listItem) => {
        clearError();
        try {
            const response = await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
            if (!response.ok) throw new Error('Failed to delete task');
            listItem.remove();
        } catch (err) {
            showError(err.message);
        }
    };

    loadTasks();
});
