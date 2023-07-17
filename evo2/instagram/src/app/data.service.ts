import { Injectable } from '@angular/core';

export interface Post {
  id: number;
  name: string;
  caption: string;
  like: number;
  comments: Array<string>
}

@Injectable({
  providedIn: 'root'
})
export class DataService {
  posts: Post[] = [
    {id: 1, name: "my first post", caption: "caption", like: 0, comments: []},
    {id: 2, name: "my second post", caption: "caption", like: 2, comments: []},
    {id: 3, name: "my third post", caption: "caption", like: 0, comments: ["yes"]}
  ]
  constructor() { 
  }

  getPost(){
    return this.posts
  }

  createPost(p: Post): any{
    this.posts.push(p)
    return "done"
  }

}
