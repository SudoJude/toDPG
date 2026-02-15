import { Component, OnInit, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatCheckboxModule,
    MatButtonModule
  ],
  template: `
    <h2 mat-dialog-title>Configuration</h2>
    <mat-dialog-content class="mat-typography" *ngIf="config">
      <div class="section">
        <h3>Video</h3>
        <div class="form-row">
          <mat-form-field appearance="outline">
            <mat-label>Bitrate (kbps)</mat-label>
            <input matInput type="number" [(ngModel)]="config.VIDEO.video_bitrate">
          </mat-form-field>

          <mat-form-field appearance="outline">
            <mat-label>FPS</mat-label>
            <mat-select [(ngModel)]="config.VIDEO.video_fps">
              <mat-option value="15">15</mat-option>
              <mat-option value="20">20</mat-option>
              <mat-option value="24">24</mat-option>
            </mat-select>
          </mat-form-field>
        </div>
        
        <mat-checkbox [(ngModel)]="config.VIDEO.video_keepaspect">
          Keep Aspect Ratio
        </mat-checkbox>
      </div>

      <div class="section">
        <h3>Audio</h3>
        <div class="form-row">
          <mat-form-field appearance="outline">
            <mat-label>Bitrate (kbps)</mat-label>
            <mat-select [(ngModel)]="config.AUDIO.audio_bitrate_mp2">
              <mat-option value="64">64</mat-option>
              <mat-option value="96">96</mat-option>
              <mat-option value="128">128</mat-option>
              <mat-option value="192">192</mat-option>
            </mat-select>
          </mat-form-field>

          <mat-checkbox [(ngModel)]="config.AUDIO.audio_normalize">
            Normalize Volume
          </mat-checkbox>
        </div>
      </div>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button mat-dialog-close>Cancel</button>
      <button mat-raised-button color="primary" (click)="saveConfig()">Save Settings</button>
    </mat-dialog-actions>
  `,
  styles: [`
    .section { margin-bottom: 24px; }
    .section h3 { margin-top: 0; margin-bottom: 16px; font-size: 1.1em; color: #555; }
    .form-row { display: flex; gap: 16px; flex-wrap: wrap; align-items: center; }
    mat-form-field { flex: 1; min-width: 150px; }
    mat-checkbox { margin-bottom: 16px; }
  `]
})
export class SettingsComponent implements OnInit {
  config: any = null;

  constructor(
    private api: ApiService,
    private dialogRef: MatDialogRef<SettingsComponent>
  ) { }

  ngOnInit() {
    this.api.getConfig().subscribe({
      next: (data) => this.config = data,
      error: (err) => console.error('Failed to load config', err)
    });
  }

  saveConfig() {
    this.api.updateConfig(this.config).subscribe({
      next: () => this.dialogRef.close(true),
      error: (err) => console.error('Failed to save config', err)
    });
  }
}
