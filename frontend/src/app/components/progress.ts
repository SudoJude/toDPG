import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api';
import { interval, Subscription } from 'rxjs';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';

@Component({
  selector: 'app-progress',
  standalone: true,
  imports: [
    CommonModule,
    MatProgressBarModule,
    MatCardModule,
    MatButtonModule,
    MatChipsModule
  ],
  template: `
    <mat-card class="progress-card" *ngIf="shouldShow()">
      <mat-card-header>
        <mat-card-title>Encoding Progress</mat-card-title>
        <mat-card-subtitle>
          <mat-chip-set>
            <mat-chip [ngClass]="status.status">{{ status.status | uppercase }}</mat-chip>
          </mat-chip-set>
        </mat-card-subtitle>
      </mat-card-header>
      
      <mat-card-content>
        <div class="progress-info">
          <span>{{ status.progress }}% Complete</span>
        </div>
        <mat-progress-bar
          mode="determinate"
          [value]="status.progress"
          [color]="status.status === 'error' ? 'warn' : 'primary'">
        </mat-progress-bar>

        <div class="log-window">
          <div *ngFor="let line of status.log" class="log-line">{{ line }}</div>
        </div>
        
        <div class="error-msg" *ngIf="status.error">
          Error: {{ status.error }}
        </div>
      </mat-card-content>

      <mat-card-actions align="end" *ngIf="status.status === 'running'">
        <button mat-button color="warn" (click)="cancel()">Cancel</button>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [`
    .progress-card { margin-bottom: 20px; }
    .progress-info { display: flex; justify-content: flex-end; margin-bottom: 8px; font-size: 0.9em; font-weight: 500; }
    mat-progress-bar { height: 8px; border-radius: 4px; margin-bottom: 16px; }
    
    .log-window { background: #222; color: #0f0; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.75em; padding: 12px; height: 120px; overflow-y: auto; border-radius: 4px; margin: 16px 0; }
    .log-line { white-space: pre-wrap; word-break: break-all; line-height: 1.4; }
    
    .error-msg { color: #f44336; margin-top: 10px; font-weight: 500; }
    
    /* Status Chip Styles */
    .running { --mdc-chip-elevated-container-color: #e3f2fd; --mdc-chip-label-text-color: #1976d2; }
    .completed { --mdc-chip-elevated-container-color: #e8f5e9; --mdc-chip-label-text-color: #388e3c; }
    .error { --mdc-chip-elevated-container-color: #ffebee; --mdc-chip-label-text-color: #d32f2f; }
  `]
})
export class ProgressComponent implements OnInit, OnDestroy {
  @Input() selectedFile: string | null = null;
  status: any = null;
  private pollSub: Subscription | null = null;

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.pollSub = interval(1000).subscribe(() => {
      this.api.getStatus().subscribe((data: any) => {
        if (this.status?.status === 'running' && data.status === 'completed') {
          this.api.triggerFileRefresh();
        }
        this.status = data;
      });
    });
  }

  ngOnDestroy() {
    if (this.pollSub) {
      this.pollSub.unsubscribe();
    }
  }

  shouldShow(): boolean {
    if (!this.status || this.status.status === 'idle') return false;
    if (!this.selectedFile) return false;
    return this.status.input_file === this.selectedFile;
  }

  cancel() {
    this.api.cancel().subscribe();
  }
}
