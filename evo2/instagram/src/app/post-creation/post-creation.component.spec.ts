import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostCreationComponent } from './post-creation.component';

describe('PostCreationComponent', () => {
  let component: PostCreationComponent;
  let fixture: ComponentFixture<PostCreationComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PostCreationComponent]
    });
    fixture = TestBed.createComponent(PostCreationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
