import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard';

export const routes: Routes = [
    { path: '', component: DashboardComponent },
    { path: '**', redirectTo: '' }
];
