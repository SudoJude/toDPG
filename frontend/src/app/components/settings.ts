import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="settings-panel" *ngIf="config">
      <div class="settings-header">
        <h3>Configuration</h3>
        <button class="close-btn" (click)="close.emit()" title="Close">×</button>
      </div>
      
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
    .settings-panel { padding: 0; background: white; border-radius: 8px; overflow: hidden; }
    .settings-header { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; background: #f8f9fa; border-bottom: 1px solid #eee; }
    .settings-header h3 { margin: 0; font-size: 1.2em; color: #333; }
    .close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #999; line-height: 1; padding: 0; }
    .close-btn:hover { color: #333; }
    
    .section { padding: 15px 20px; border-bottom: 1px solid #f0f0f0; }
    .section:last-of-type { border-bottom: none; }
    h4 { margin-top: 0; margin-bottom: 12px; font-size: 1em; color: #555; }
    .form-group { margin-bottom: 12px; }
    label { display: block; margin-bottom: 5px; font-weight: 500; font-size: 0.9em; color: #666; }
    input[type="number"], select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 0.9em; }
    input[type="checkbox"] { width: auto; margin-right: 8px; vertical-align: middle; }
    .actions { padding: 15px 20px; background: #f8f9fa; text-align: right; border-top: 1px solid #eee; }
    button:not(.close-btn) { background: #007bff; color: white; border: none; padding: 8px 20px; border-radius: 4px; cursor: pointer; font-weight: 600; transition: background 0.2s; }
    button:not(.close-btn):hover { background: #0056b3; }
  `]
})
export class SettingsComponent implements OnInit {
  @Output() close = new EventEmitter<void>();
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
      next: () => this.close.emit(),
      error: (err) => console.error('Failed to save config', err)
    });
  }
}
