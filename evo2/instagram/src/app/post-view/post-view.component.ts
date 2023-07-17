import { Component } from '@angular/core';

import { Post, DataService} from "../data.service"

@Component({
  selector: 'app-post-view',
  templateUrl: './post-view.component.html',
  styleUrls: ['./post-view.component.css']
})
export class PostViewComponent {
  newposts: Post[] = []
  constructor(posts: DataService) {
    this.newposts = posts.getPost()
  }

}
