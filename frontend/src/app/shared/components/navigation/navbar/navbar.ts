// app/shared/components/navbar/navbar.component.ts
import { Component, HostListener, signal } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

interface NavItem {
  label: string;
  path: string;
}

@Component({
  selector: 'Navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navbar.html',
})
export class NavbarComponent {
  protected readonly navItems: NavItem[] = [
    { label: 'Dashboard', path: '/dashboard' },
    { label: 'Patients', path: '/patients' },
    { label: 'Schedule', path: '/schedule' },
    { label: 'Treatments', path: '/treatments' },
    { label: 'Reports', path: '/reports' },
  ];

  protected readonly mobileOpen = signal(false);
  protected readonly isDark = signal(this.getInitialTheme());

  constructor() {
    this.applyTheme(this.isDark());
  }

  protected toggleTheme(): void {
    this.isDark.update((value) => !value);
    this.applyTheme(this.isDark());
    localStorage.setItem('theme', this.isDark() ? 'dark' : 'light');
  }

  protected toggleMobileMenu(): void {
    this.mobileOpen.update((value) => !value);
  }

  protected closeMobileMenu(): void {
    this.mobileOpen.set(false);
  }

  @HostListener('window:keydown.escape')
  protected onEscape(): void {
    this.mobileOpen.set(false);
  }

  private getInitialTheme(): boolean {
    const stored = localStorage.getItem('theme');
    if (stored) return stored === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  private applyTheme(dark: boolean): void {
    document.documentElement.classList.toggle('dark', dark);
  }
}