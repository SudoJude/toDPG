import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FileBrowserComponent } from './file-browser';
import { SettingsComponent } from './settings';
import { ProgressComponent } from './progress';
import { ApiService } from '../services/api';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FileBrowserComponent, SettingsComponent, ProgressComponent],
  template: `
    <div class="dashboard">
    <div class="dashboard">
      <div class="main-content">
        <div class="left-panel">
          <h3>Select File</h3>
          <app-file-browser (fileSelected)="onFileSelected($event)"></app-file-browser>
          <div class="selected-file" *ngIf="selectedFile">
            <strong>Selected:</strong> {{ selectedFile }}
          </div>
        </div>

        <div class="right-panel">
          <app-settings></app-settings>
        </div>
      </div>

      <div class="action-bar">
        <button class="convert-btn" [disabled]="!selectedFile" (click)="startConversion()">
          Convert to DPG
        </button>
      </div>

      <app-progress></app-progress>
    </div>
  `,
  styles: [`
    .dashboard { max-width: 1200px; margin: 0 auto; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #eee; padding-bottom: 20px; }
    h1 { margin: 0; color: #333; }
    p { margin: 5px 0 0; color: #666; }
    
    .main-content { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    @media (max-width: 768px) { .main-content { grid-template-columns: 1fr; } }
    
    .selected-file { margin-top: 10px; padding: 10px; background: #e3f2fd; border-radius: 4px; word-break: break-all; }
    
    .action-bar { margin-top: 30px; text-align: center; }
    .convert-btn { font-size: 1.2em; padding: 12px 30px; background: #4caf50; color: white; border: none; border-radius: 5px; cursor: pointer; transition: background 0.2s; }
    .convert-btn:disabled { background: #ccc; cursor: not-allowed; }
    .convert-btn:hover:not(:disabled) { background: #388e3c; }
  `]
})
export class DashboardComponent {
  selectedFile: string | null = null;

  constructor(private api: ApiService) { }

  onFileSelected(path: string) {
    this.selectedFile = path;
  }

  startConversion() {
    if (this.selectedFile) {
      this.api.convert(this.selectedFile).subscribe({
        next: () => console.log('Conversion started'),
        error: (err) => alert('Failed to start conversion: ' + err.error.error)
      });
    }
  }
}
