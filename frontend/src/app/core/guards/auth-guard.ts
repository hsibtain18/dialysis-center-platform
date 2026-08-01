// app/core/guards/auth.guard.ts

import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { catchError, map, of } from 'rxjs';
import { AuthApiService } from '../../features/auth/api/auth-api.service';
import { TokenService } from '@core/services/token';

export const authGuard: CanActivateFn = () => {
  const authApi = inject(AuthApiService);
  const tokenService = inject(TokenService);
  const router = inject(Router);

  return authApi.me().pipe(
    map(() => {
      tokenService.setLoggedIn(true);
      return true;
    }),
    catchError(() => {
      tokenService.setLoggedIn(false);
      router.navigate(['/login']);
      return of(false);
    })
  );
};