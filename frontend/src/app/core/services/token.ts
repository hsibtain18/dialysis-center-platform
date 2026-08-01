// app/core/services/token.service.ts

import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class TokenService {
 
  private loggedIn = false;

  setLoggedIn(state: boolean): void {
    this.loggedIn = state;
  }

  isLoggedIn(): boolean {
    return this.loggedIn;
  }
}