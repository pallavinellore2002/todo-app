const API_URL = "http://127.0.0.1:8000/api/todos";

const todoList = document.getElementById("todo-list");
const todoInput = document.getElementById("todo-input");
const addButton = document.getElementById("add-button");

const completedCount = document.getElementById("completed-count");
const pendingCount = document.getElementById("pending-count");


async function loadTodos() {
    const response = await fetch(API_URL);

    if (!response.ok) {
        throw new Error("Failed to fetch todos");
    }

    const todos = await response.json();

    todoList.innerHTML = "";

    todos.forEach((todo, index) => {
        createTodoElement(todo, index);
    });

    updateCounts(todos);
}


function createTodoElement(todo, index) {

    const listItem = document.createElement("li");

    listItem.className = "todo-item";


    const number = document.createElement("span");

    number.className = "todo-number";

    number.textContent = `${index + 1}.`;


    const checkbox = document.createElement("input");

    checkbox.type = "checkbox";

    checkbox.checked = Number(todo.completed) === 1;


    const title = document.createElement("span");

    title.className = "todo-title";

    title.textContent = todo.title;


    const buttonContainer = document.createElement("div");

    buttonContainer.className = "todo-buttons";


    const deleteButton = document.createElement("button");

    deleteButton.textContent = "Delete";

    deleteButton.className = "delete-button";


    const editButton = document.createElement("button");

    editButton.textContent = "Edit";

    editButton.className = "edit-button";


    checkbox.addEventListener("change", async () => {

        await updateTodo(
            todo.id,
            todo.title,
            checkbox.checked
        );

    });


    deleteButton.addEventListener("click", async () => {

        await deleteTodo(todo.id);

    });


    editButton.addEventListener("click", async () => {

        const newTitle = prompt(
            "Enter the new task name:",
            todo.title
        );

        if (newTitle === null) {
            return;
        }

        const trimmedTitle = newTitle.trim();

        if (trimmedTitle === "") {
            alert("Task name cannot be empty.");
            return;
        }

        await updateTodo(
            todo.id,
            trimmedTitle,
            todo.completed
        );

    });


    buttonContainer.appendChild(deleteButton);

    buttonContainer.appendChild(editButton);


    listItem.appendChild(number);

    listItem.appendChild(checkbox);

    listItem.appendChild(title);

    listItem.appendChild(buttonContainer);


    todoList.appendChild(listItem);
}


async function addTodo() {

    const title = todoInput.value.trim();

    if (title === "") {
        alert("Please enter a task.");
        return;
    }


    const response = await fetch(API_URL, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: title
        })

    });


    if (!response.ok) {
        throw new Error("Failed to add todo");
    }


    todoInput.value = "";

    await loadTodos();
}


async function deleteTodo(todoId) {

    const response = await fetch(
        `${API_URL}/${todoId}`,
        {
            method: "DELETE"
        }
    );


    if (!response.ok) {
        throw new Error("Failed to delete todo");
    }


    await loadTodos();
}


async function updateTodo(todoId, title, completed) {

    const response = await fetch(
        `${API_URL}/${todoId}`,
        {
            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                title: title,
                completed: completed
            })
        }
    );


    if (!response.ok) {
        throw new Error("Failed to update todo");
    }


    await loadTodos();
}


function updateCounts(todos) {

    const completed = todos.filter(
        todo => Number(todo.completed) === 1
    ).length;


    const pending = todos.length - completed;


    completedCount.textContent = completed;

    pendingCount.textContent = pending;
}


addButton.addEventListener("click", addTodo);


todoInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {
        addTodo();
    }

});


loadTodos().catch(error => {

    console.error(error);

    alert("Could not connect to the Todo API.");

});