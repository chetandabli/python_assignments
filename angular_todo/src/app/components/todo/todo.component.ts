import { Component, OnInit } from '@angular/core';
import { Todo, TodoService } from '../../services/todo.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-todo',
  templateUrl: './todo.component.html',
  styleUrls: ['./todo.component.css']
})
export class TodoComponent {
  todos: Todo[] = [];
  constructor(private todoService: TodoService, private router: Router) {}

  ngOnInit(): void {
    this.todos = this.todoService.data;
  }

  toggleCompleted(todo: Todo): void {
    todo.completed = !todo.completed;
    this.todoService.updateTodoStatus(todo.id, todo.completed);
  }

  redirectToTodoDetail(todoId: number): void {
    this.router.navigate(['/todo', todoId]);
  }
}
