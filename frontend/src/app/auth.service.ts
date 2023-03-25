import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';
import { delay, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  isUserLoggedIn: boolean = false;

  constructor() { }

  login(username: string, password: string): Observable<Boolean> {
    console.log(username);
    // Validate user here
    this.isUserLoggedIn = true
    localStorage.setItem('isUserLoggedIn', String(this.isUserLoggedIn));

    return of(this.isUserLoggedIn).pipe(
      delay(1000), tap(val => { console.log("User authentication: " + val); })
    );
  }

  logout(): void {
    this.isUserLoggedIn = false;
    localStorage.removeItem('isUserLoggedIn');
  }
}
