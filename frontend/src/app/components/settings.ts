import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="settings-panel" *ngIf="config">
      <h3>Configuration</h3>
      
      <div class="section">
        <h4>Video</h4>
        <div class="form-group">
          <label>Bitrate (kbps)</label>
          <input type="number" [(ngModel)]="config.VIDEO.video_bitrate">
        </div>
        <div class="form-group">
          <label>FPS</label>
          <select [(ngModel)]="config.VIDEO.video_fps">
            <option value="15">15</option>
            <option value="20">20</option>
            <option value="24">24</option>
          </select>
        </div>
        <div class="form-group">
          <label>
            <input type="checkbox" [(ngModel)]="config.VIDEO.video_keepaspect"> Keep Aspect Ratio
          </label>
        </div>
      </div>

      <div class="section">
        <h4>Audio</h4>
        <div class="form-group">
          <label>Bitrate (kbps)</label>
          <select [(ngModel)]="config.AUDIO.audio_bitrate_mp2">
            <option value="64">64</option>
            <option value="96">96</option>
            <option value="128">128</option>
            <option value="192">192</option>
          </select>
        </div>
        <div class="form-group">
          <label>
            <input type="checkbox" [(ngModel)]="config.AUDIO.audio_normalize"> Normalize Volume
          </label>
        </div>
      </div>

      <div class="actions">
        <button (click)="saveConfig()">Save Settings</button>
      </div>
    </div>
  `,
  styles: [`
    .settings-panel { padding: 15px; border: 1px solid #eee; border-radius: 4px; background: #f9f9f9; }
    .section { margin-bottom: 20px; }
    h4 { margin-top: 0; margin-bottom: 10px; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
    .form-group { margin-bottom: 10px; }
    label { display: block; margin-bottom: 5px; font-weight: 500; }
    input[type="number"], select { width: 100%; padding: 5px; border: 1px solid #ccc; border-radius: 3px; }
    input[type="checkbox"] { width: auto; margin-right: 5px; }
    .actions { text-align: right; }
    button { background: #007bff; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
    button:hover { background: #0056b3; }
  `]
})
export class SettingsComponent implements OnInit {
  config: any = null;

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.api.getConfig().subscribe({
      next: (data) => this.config = data,
      error: (err) => console.error('Failed to load config', err)
    });
  }

  saveConfig() {
    this.api.updateConfig(this.config).subscribe({
      next: () => alert('Settings saved!'),
      error: (err) => console.error('Failed to save config', err)
    });
  }
}
