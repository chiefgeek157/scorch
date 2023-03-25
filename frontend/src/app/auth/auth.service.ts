import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const TOKEN_KEY = 'login-token';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  isLoggedIn: boolean = false;

  constructor(private httpClient: HttpClient) { }

  login(username: string, password: string): Observable<Boolean> | boolean {
    if (this.isLoggedIn) {
      return true
    }

    this.isLoggedIn = true
    localStorage.setItem(TOKEN_KEY, String(this.isLoggedIn));

    return of(this.isUserLoggedIn).pipe(
      delay(1000), tap(val => { console.log("User authentication: " + val); })
    );
  }
}
