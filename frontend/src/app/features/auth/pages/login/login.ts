// app/features/auth/pages/login/login.component.ts

import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthApiService } from '@features/auth/services/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login.html'
})
export class Login {
  private fb = inject(FormBuilder);
  private authService = inject(AuthApiService);

  loading = signal(false);
  errorMessage = signal<string | null>(null);

  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]]
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
      next: () => {
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