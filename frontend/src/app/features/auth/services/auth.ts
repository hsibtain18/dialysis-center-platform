// app/features/auth/api/auth-api.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { LoginRequest, LoginResponse } from '../models/auth.models';

@Injectable({ providedIn: 'root' })
export class AuthApiService {
  private readonly baseUrl = `${environment.apiUrl}/auth`;

  constructor(private http: HttpClient) {}

  login(payload: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.baseUrl}/login`, payload, {
      withCredentials: true // allows the browser to accept the Set-Cookie refresh token
    });
  }

  refreshToken(): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.baseUrl}/refresh`, {}, {
      withCredentials: true // sends the httpOnly cookie automatically
    });
  }

  logout(): Observable<void> {
    return this.http.post<void>(`${this.baseUrl}/logout`, {}, {
      withCredentials: true // lets backend clear the cookie
    });
  }
}