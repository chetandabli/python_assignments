// todo.component.ts

import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

class Todo {
  id: number;
  title: string;
  completed: boolean;

  constructor(id: number, title: string, completed: boolean) {
    this.id = id;
    this.title = title;
    this.completed = completed;
  }
}

@Component({
  selector: 'app-todo',
  templateUrl: './todo.component.html',
  styleUrls: ['./todo.component.css']
})
export class TodoComponent {
  todos: Todo[] = [
    new Todo(1, 'Buy groceries', false),
    new Todo(2, 'Finish homework', false),
    new Todo(3, 'Walk the dog', false)
  ];

  newTodoTitle = '';

  addTodo() {
    if (this.newTodoTitle.trim() !== '') {
      const newTodoId = this.todos.length > 0 ? this.todos[this.todos.length - 1].id + 1 : 1;
      const newTodo = new Todo(newTodoId, this.newTodoTitle, false);
      this.todos.push(newTodo);
      this.newTodoTitle = '';
    }
  }

  deleteTodo(todo: Todo) {
    const todoIndex = this.todos.indexOf(todo);
    if (todoIndex !== -1) {
      this.todos.splice(todoIndex, 1);
    }
  }

  toggleCompleted(todo: Todo) {
    todo.completed = !todo.completed;
  }
}
