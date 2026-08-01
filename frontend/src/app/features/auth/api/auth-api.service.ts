// app/features/auth/api/auth-api.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { LoginRequest, LoginResponse } from '../models/auth.models';

@Injectable({ providedIn: 'root' })
export class AuthApiService {
  private readonly baseUrl = `${environment.apiUrl}auth`;

  constructor(private http: HttpClient) {}

  login(payload: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.baseUrl}/login`, payload, {
      withCredentials: true
    });
  }

  logout(): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(`${this.baseUrl}/logout`, {}, {
      withCredentials: true
    });
  }

  me(): Observable<LoginResponse['user']> {
    return this.http.get<LoginResponse['user']>(`${this.baseUrl}/me`, {
      withCredentials: true
    });
  }
}