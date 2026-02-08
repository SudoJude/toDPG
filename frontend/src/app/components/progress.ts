import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api';
import { interval, Subscription } from 'rxjs';

@Component({
  selector: 'app-progress',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="progress-container" *ngIf="shouldShow()">
      <div class="status-header">
        <span class="status-badge" [ngClass]="status.status">{{ status.status | uppercase }}</span>
        <span class="percent">{{ status.progress }}%</span>
      </div>
      
      <div class="progress-bar-bg">
        <div class="progress-bar-fill" [style.width.%]="status.progress"></div>
      </div>

      <div class="log-window">
        <div *ngFor="let line of status.log" class="log-line">{{ line }}</div>
      </div>

      <div class="actions" *ngIf="status.status === 'running'">
        <button (click)="cancel()" class="cancel-btn">Cancel</button>
      </div>
      
      <div class="error-msg" *ngIf="status.error">
        Error: {{ status.error }}
      </div>
    </div>
  `,
  styles: [`
    .progress-container { margin-bottom: 20px; padding: 15px; background: white; border: 1px solid #eee; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    .status-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .status-badge { padding: 4px 8px; border-radius: 4px; font-size: 0.75em; font-weight: bold; }
    .status-badge.running { background: #e3f2fd; color: #1976d2; }
    .status-badge.completed { background: #e8f5e9; color: #388e3c; }
    .status-badge.error { background: #ffebee; color: #d32f2f; }
    .status-badge.cancelled { background: #f5f5f5; color: #616161; }
    
    .percent { font-size: 0.85em; font-weight: 600; color: #666; }
    .progress-bar-bg { height: 8px; background: #eee; border-radius: 4px; overflow: hidden; margin-bottom: 15px; }
    .progress-bar-fill { height: 100%; background: #4caf50; transition: width 0.3s ease; }
    
    .log-window { background: #222; color: #0f0; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.75em; padding: 10px; height: 100px; overflow-y: auto; border-radius: 4px; margin-bottom: 10px; }
    .log-line { white-space: pre-wrap; word-break: break-all; line-height: 1.4; }
    
    .actions { text-align: right; }
    .cancel-btn { background: #d32f2f; color: white; border: none; padding: 6px 15px; border-radius: 4px; cursor: pointer; font-size: 0.85em; font-weight: 500; transition: background 0.2s; }
    .cancel-btn:hover { background: #b71c1c; }
    .error-msg { color: #d32f2f; margin-top: 10px; font-weight: bold; font-size: 0.85em; }
  `]
})
export class ProgressComponent implements OnInit, OnDestroy {
  @Input() selectedFile: string | null = null;
  status: any = null;
  private pollSub: Subscription | null = null;

  constructor(private api: ApiService) { }

  ngOnInit() {
    // Poll status every second
    this.pollSub = interval(1000).subscribe(() => {
      this.api.getStatus().subscribe((data: any) => {
        // Trigger refresh if status just transitioned to completed
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

    // Normalize paths if needed, but assuming absolute paths from backend
    return this.status.input_file === this.selectedFile;
  }

  cancel() {
    this.api.cancel().subscribe();
  }
}
