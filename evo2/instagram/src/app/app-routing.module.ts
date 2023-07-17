import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { PostCreationComponent } from './post-creation/post-creation.component';
import { PostViewComponent } from './post-view/post-view.component';
import { PostDeleteComponent } from './post-delete/post-delete.component';

const routes: Routes = [
  { path: 'postcreate', component: PostCreationComponent },
  { path: 'postview', component: PostViewComponent },
  { path: 'postdelete', component: PostDeleteComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
