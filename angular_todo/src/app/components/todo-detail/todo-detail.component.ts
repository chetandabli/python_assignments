import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Todo, TodoService } from '../../services/todo.service';

@Component({
  selector: 'app-todo-detail',
  templateUrl: './todo-detail.component.html',
  styleUrls: ['./todo-detail.component.css']
})
export class TodoDetailComponent implements OnInit {
  todoId: number | null = null;
  todo: Todo | undefined;

  constructor(
    private route: ActivatedRoute,
    private todoService: TodoService
  ) {}

  async ngOnInit(): Promise<void> {
    const id = this.route.snapshot.paramMap.get('id');
    this.todoId = id !== null ? +id : null;

    if (this.todoId !== null) {
      this.todoService.getTodoById(this.todoId).subscribe(
        todo => {
          this.todo = todo;
        },
        error => {
          console.error('Failed to fetch todo:', error);
        }
      );
    }
  }
}
