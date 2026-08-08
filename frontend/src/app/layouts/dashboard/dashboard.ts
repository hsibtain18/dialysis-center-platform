import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from '@shared/components/navigation/navbar/navbar';

@Component({
  selector: 'dashboard-layout',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent],
  templateUrl: './dashboard.html',
})
export class DashboardLayout {}