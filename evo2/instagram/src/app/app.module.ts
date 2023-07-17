import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PostCreationComponent } from './post-creation/post-creation.component';
import { PostViewComponent } from './post-view/post-view.component';
import { PostDeleteComponent } from './post-delete/post-delete.component';

@NgModule({
  declarations: [
    AppComponent,
    PostCreationComponent,
    PostViewComponent,
    PostDeleteComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
