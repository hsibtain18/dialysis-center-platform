// app/features/auth/services/auth.service.ts

import { Injectable, inject } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { AuthApiService } from '../api/auth-api.service'; 
import { LoginRequest, LoginResponse } from '../models/auth.models';
import { TokenService } from '@core/services/token';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private authApi = inject(AuthApiService);
  private tokenService = inject(TokenService);
  private router = inject(Router);

  login(payload: LoginRequest): Observable<LoginResponse> {
    return this.authApi.login(payload).pipe(
      tap(() => {
        this.tokenService.setLoggedIn(true);
        this.router.navigate(['/dashboard']);
      })
    );
  }

  logout(): void {
    this.authApi.logout().subscribe(() => {
      this.tokenService.setLoggedIn(false);
      this.router.navigate(['/login']);
    });
  }
}