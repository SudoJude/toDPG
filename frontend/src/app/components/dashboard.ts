import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FileBrowserComponent } from './file-browser';
import { SettingsComponent } from './settings';
import { ApiService } from '../services/api';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FileBrowserComponent, SettingsComponent],
  template: `
    <div class="dashboard">
      <div class="top-bar">
        <h1>DPG4X Web</h1>
        <button class="icon-btn settings-trigger" (click)="showSettings = true" title="Settings">⚙️</button>
      </div>

      <div class="main-content">
        <div class="file-panel">
          <app-file-browser (fileSelected)="onFileSelected($event)"></app-file-browser>
        </div>
      </div>

      <!-- Settings Modal -->
      <div class="modal-overlay" *ngIf="showSettings" (click)="showSettings = false">
        <div class="modal-content" (click)="$event.stopPropagation()">
          <app-settings (close)="showSettings = false"></app-settings>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .dashboard { max-width: 1000px; margin: 0 auto; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; position: relative; }
    
    .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #eee; padding-bottom: 15px; }
    h1 { margin: 0; color: #333; font-size: 1.5em; }
    
    .icon-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; padding: 5px; border-radius: 4px; transition: background 0.2s; }
    .icon-btn:hover { background: #eee; }

    .main-content { display: block; }
    .file-panel { background: white; border-radius: 8px; }
    
    /* Modal Styles */
    .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
    .modal-content { background: white; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); width: 90%; max-width: 500px; animation: modalIn 0.3s ease-out; }
    
    @keyframes modalIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
  `]
})
export class DashboardComponent {
  showSettings: boolean = false;

  constructor(private api: ApiService) { }

  onFileSelected(path: string) {
    // We can still track the selected file if we need it in the future
    // console.log('Selected file in dashboard:', path);
  }
}
