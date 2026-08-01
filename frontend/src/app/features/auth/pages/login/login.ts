// app/features/auth/pages/login/login.component.ts

import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LoginResponse } from '@features/auth/models/auth.models';
import { AuthService } from '@features/auth/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login.html'
})
export class Login {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);

  loading = signal(false);
  errorMessage = signal<string | null>(null);

  form = this.fb.group({
    email: ['has@dialysiscenter.com', [Validators.required, Validators.email]],
    password: ['521541', [Validators.required, Validators.minLength(6)]]
  });

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading.set(true);
    this.errorMessage.set(null);

    const { email, password } = this.form.getRawValue();

    this.authService.login({ email: email!, password: password! }).subscribe({
      next: (data: LoginResponse) => {
        this.loading.set(false);
      },
      error: (err) => {
        this.loading.set(false);
        this.errorMessage.set(
          err.status === 401 ? 'Invalid email or password' : 'Something went wrong. Try again.'
        );
      }
    });
  }
}