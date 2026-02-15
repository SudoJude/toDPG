import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FileBrowserComponent } from './file-browser';
import { SettingsComponent } from './settings';
import { ApiService } from '../services/api';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    FileBrowserComponent,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatDialogModule
  ],
  template: `
    <div class="dashboard-container">
      <mat-toolbar color="primary">
        <span>DPG4X Web</span>
        <span class="spacer"></span>
        <button mat-icon-button (click)="openSettings()" title="Settings">
          <mat-icon>settings</mat-icon>
        </button>
      </mat-toolbar>

      <div class="main-content">
        <app-file-browser (fileSelected)="onFileSelected($event)"></app-file-browser>
      </div>
    </div>
  `,
  styles: [`
    .dashboard-container {
      display: flex;
      flex-direction: column;
      height: 100vh;
      background-color: #f5f5f5;
    }
    .spacer { flex: 1 1 auto; }
    .main-content {
      flex: 1;
      padding: 20px;
      overflow: auto;
    }
  `]
})
export class DashboardComponent {
  constructor(
    private api: ApiService,
    private dialog: MatDialog
  ) { }

  openSettings() {
    this.dialog.open(SettingsComponent, {
      width: '500px'
    });
  }

  onFileSelected(path: string) {
    // console.log('Selected file in dashboard:', path);
  }
}
