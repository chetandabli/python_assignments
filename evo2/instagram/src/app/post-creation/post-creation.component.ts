import { Component } from '@angular/core';

import { Post, DataService} from "../data.service"

@Component({
  selector: 'app-post-creation',
  templateUrl: './post-creation.component.html',
  styleUrls: ['./post-creation.component.css']
})
export class PostCreationComponent {
  constructor(posts: DataService) {
  }

  posts.createPost()
}
