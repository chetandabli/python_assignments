import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { TodoComponent } from './components/todo/todo.component';
import { CreateTodoComponent } from './components/create-todo/create-todo.component';
import { TodoDetailComponent } from './components/todo-detail/todo-detail.component';

const routes: Routes = [
  { path: 'todo', component: TodoComponent },
  { path: 'createtodo', component: CreateTodoComponent },
  { path: 'todo/:id', component: TodoDetailComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
