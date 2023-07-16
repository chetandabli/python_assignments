import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

export interface Todo {
    id: number;
    title: string;
    description: string;
    completed: boolean;
  }

@Injectable({
  providedIn: 'root'
})
export class TodoService {
  data: Todo[] = [
    {
      id: 1,
      title: 'Sample Todo 1',
      description: 'This is the first sample todo item',
      completed: false
    },
    {
      id: 2,
      title: 'Sample Todo 2',
      description: 'This is the second sample todo item',
      completed: true
    },
    {
      id: 3,
      title: 'Sample Todo 3',
      description: 'This is the third sample todo item',
      completed: false
    }
  ];

  updateTodoStatus(todoId: number, completed: boolean): void {
    const todo = this.data.find(todo => todo.id === todoId);
    if (todo) {
      todo.completed = completed;
    }
  }

  getTodoById(id: number): Observable<Todo | undefined> {
    const todo = this.data.find(todo => todo.id === id);
    return of(todo);
  }
}
