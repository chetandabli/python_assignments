import { Component } from '@angular/core';
import { TodoService } from '../../services/todo.service';

@Component({
  selector: 'app-create-todo',
  templateUrl: './create-todo.component.html',
  styleUrls: ['./create-todo.component.css']
})

export class CreateTodoComponent {
  constructor(private todoService: TodoService) {}

  newItem: string = "";
  des: string = "";
  

  addItem() {
    if (this.newItem && this.des) {
      this.todoService.data.push({"id": this.todoService.data[this.todoService.data.length-1].id + 1, "title": this.newItem, "description": this.des, "completed": false});
      this.newItem = '';
      this.des = '';
      console.log(this.todoService.data)
      alert("todo created!")
    }else{
      alert("please enter all details to create todo!")
    }
  }
}
