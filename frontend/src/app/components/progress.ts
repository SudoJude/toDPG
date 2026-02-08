import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api';
import { interval, Subscription } from 'rxjs';

@Component({
  selector: 'app-progress',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="progress-container" *ngIf="status && status.status !== 'idle'">
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
    .progress-container { margin-top: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 4px; background: white; }
    .status-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .status-badge { padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
    .status-badge.running { background: #e3f2fd; color: #1976d2; }
    .status-badge.completed { background: #e8f5e9; color: #388e3c; }
    .status-badge.error { background: #ffebee; color: #d32f2f; }
    .status-badge.cancelled { background: #f5f5f5; color: #616161; }
    
    .progress-bar-bg { height: 10px; background: #eee; border-radius: 5px; overflow: hidden; margin-bottom: 15px; }
    .progress-bar-fill { height: 100%; background: #4caf50; transition: width 0.3s ease; }
    
    .log-window { background: #222; color: #0f0; font-family: monospace; font-size: 0.8em; padding: 10px; height: 100px; overflow-y: auto; border-radius: 4px; margin-bottom: 10px; }
    .log-line { white-space: pre-wrap; word-break: break-all; }
    
    .cancel-btn { background: #d32f2f; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
    .error-msg { color: #d32f2f; margin-top: 10px; font-weight: bold; }
  `]
})
export class ProgressComponent implements OnInit, OnDestroy {
  status: any = null;
  private pollSub: Subscription | null = null;

  constructor(private api: ApiService) { }

  ngOnInit() {
    // Poll status every second
    this.pollSub = interval(1000).subscribe(() => {
      this.api.getStatus().subscribe(data => {
        this.status = data;
      });
    });
  }

  ngOnDestroy() {
    if (this.pollSub) {
      this.pollSub.unsubscribe();
    }
  }

  cancel() {
    this.api.cancel().subscribe();
  }
}
