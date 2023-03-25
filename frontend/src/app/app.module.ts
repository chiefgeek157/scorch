/*
Copyright 2023 The Scorch Authors.
*/

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http'

import { AppComponent } from './app.component';
import { AuthModule } from './auth/auth.module';
import { TopNavComponent } from './top-nav/top-nav.component';
import { UserMenuComponent } from './user-menu/user-menu.component';

@NgModule({
  declarations: [
    AppComponent,
    TopNavComponent,
    UserMenuComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AuthModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
