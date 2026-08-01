// app/core/services/token.service.ts

import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class TokenService {
  private accessToken: string | null = null;

  setToken(token: string): void {
    this.accessToken = token;
  }

  getToken(): string | null {
    return this.accessToken;
  }

  clear(): void {
    this.accessToken = null;
    // refresh token cookie is httpOnly — cleared server-side via /auth/logout
  }

  isLoggedIn(): boolean {
    return !!this.accessToken;
  }
}