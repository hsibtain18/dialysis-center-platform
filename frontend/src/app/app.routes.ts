import { Routes } from '@angular/router';
import { authGuard } from '@core/guards/auth-guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: '',
    loadChildren: () =>
      import('@features/auth/auth.routes').then(m => m.AUTH_ROUTES)
  },
  {
    path: '',
    canActivate: [authGuard],
    loadComponent: () =>
      import('@layouts/dashboard/dashboard').then(m => m.DashboardLayout),
    children: [
      {
        path: 'dashboard',
        loadChildren: () =>
          import('@features/dashboard/dashboard.routes').then(m => m.DASHBOARD_ROUTES)
      },
      // patients, schedule, treatments, reports go here later,
      // each still under the guarded DashboardLayout
    ]
  },
  {
    path: '**',
    redirectTo: 'login'
  }
];