import { Component, OnInit, OnDestroy, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api';
import { Subscription } from 'rxjs';
import { ProgressComponent } from './progress';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatProgressBarModule } from '@angular/material/progress-bar';

@Component({
  selector: 'app-file-browser',
  standalone: true,
  imports: [
    CommonModule,
    ProgressComponent,
    MatListModule,
    MatIconModule,
    MatButtonModule,
    MatCardModule,
    MatDividerModule,
    MatTooltipModule,
    MatProgressBarModule
  ],
  template: `
    <div class="file-browser-container">
      <div class="browser-section">
        <div class="header">
          <button mat-icon-button (click)="navigateUp()" [disabled]="!parentPath" matTooltip="Up">
            <mat-icon>arrow_upward</mat-icon>
          </button>
          <span class="current-path" [matTooltip]="currentPath">{{ currentPath }}</span>
          
          <div class="upload-actions">
            <input type="file" #fileInput (change)="onUploadSelected($event)" style="display: none">
            <button mat-raised-button color="primary" (click)="$event.stopPropagation(); fileInput.click()" [disabled]="uploadingFile">
              <mat-icon *ngIf="!uploadingFile">upload</mat-icon>
              {{ uploadingFile ? 'Uploading...' : 'Upload' }}
            </button>
          </div>
        </div>

        <mat-nav-list class="file-list">
          <mat-list-item *ngFor="let item of items" (click)="onItemClick(item)" [class.selected]="selectedFile === item.path">
            <mat-icon matListItemIcon>{{ item.is_dir ? 'folder' : 'insert_drive_file' }}</mat-icon>
            <div matListItemTitle class="name">{{ item.name }}</div>
            <div matListItemLine class="size" *ngIf="!item.is_dir">{{ formatSize(item.size) }}</div>
            <div matListItemMeta *ngIf="!item.is_dir">
               <button mat-icon-button (click)="$event.stopPropagation(); download(item.path)" matTooltip="Download">
                 <mat-icon>download</mat-icon>
               </button>
            </div>
          </mat-list-item>
        </mat-nav-list>
      </div>

      <div class="info-section">
        <app-progress [selectedFile]="selectedFile"></app-progress>

        <mat-card *ngIf="dpgInfo; else noDpg" class="info-card">
          <mat-card-header>
            <mat-card-title>DPG Information</mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <div class="metadata-grid">
              <div class="meta-item">
                <span class="label">Version</span>
                <span class="value">{{ dpgInfo.version }}</span>
              </div>
              <div class="meta-item">
                <span class="label">Frames</span>
                <span class="value">{{ dpgInfo.frames }}</span>
              </div>
              <div class="meta-item">
                <span class="label">FPS</span>
                <span class="value">{{ dpgInfo.fps }}</span>
              </div>
              <div class="meta-item">
                <span class="label">Duration</span>
                <span class="value">{{ dpgInfo.duration_seconds | number:'1.0-2' }}s</span>
              </div>
            </div>

            <mat-divider></mat-divider>

            <div class="thumbnail-section">
              <h4>Thumbnail</h4>
              <div class="thumb-container">
                <img [src]="thumbnailUrl" alt="DPG Thumbnail" (error)="onThumbnailError()" class="thumbnail" *ngIf="thumbnailUrl">
                <div *ngIf="!thumbnailUrl && !thumbnailError" class="loading-thumb">
                  <mat-progress-bar mode="indeterminate"></mat-progress-bar>
                </div>
                <div *ngIf="thumbnailError" class="no-thumb">
                  <mat-icon>image_not_supported</mat-icon>
                  <span>No thumbnail</span>
                </div>
              </div>
              
              <div class="update-thumb-actions">
                <input type="file" #thumbInput (change)="onThumbnailSelected($event)" accept="image/*" style="display: none">
                <button mat-button (click)="thumbInput.click()">Select Image</button>
                <button mat-flat-button color="accent" (click)="uploadThumbnail()" [disabled]="!selectedThumbnail || uploadingThumbnail">
                  {{ uploadingThumbnail ? 'Updating...' : 'Update' }}
                </button>
              </div>
              <p class="status-msg error" *ngIf="uploadError">{{ uploadError }}</p>
              <p class="status-msg success" *ngIf="uploadSuccess">Thumbnail updated!</p>
            </div>
            
            <mat-divider></mat-divider>

            <div class="preview-section">
              <button mat-raised-button color="primary" class="preview-btn" (click)="generatePreview()" [disabled]="loadingPreview" *ngIf="!previewUrl">
                <mat-icon>play_circle</mat-icon>
                {{ loadingPreview ? 'Generating...' : 'Video Preview' }}
              </button>
              <p class="status-msg error" *ngIf="previewError">{{ previewError }}</p>
              <video *ngIf="previewUrl" [src]="previewUrl" controls autoplay></video>
            </div>
          </mat-card-content>
        </mat-card>

        <ng-template #noDpg>
          <div class="no-selection" *ngIf="!selectedFile">
            <mat-icon>info</mat-icon>
            <p>Select a file to see details</p>
          </div>
          <mat-card class="conversion-card" *ngIf="selectedFile && !dpgInfo">
             <mat-card-header>
                <mat-card-title>Ready to Convert</mat-card-title>
                <mat-card-subtitle>{{ selectedFile.split('/').pop() }}</mat-card-subtitle>
             </mat-card-header>
             <mat-card-content>
                <p>Convert this file to DPG format for playback on your Nintendo DS.</p>
             </mat-card-content>
             <mat-card-actions align="end">
                <button mat-raised-button color="accent" (click)="startConversion()">
                  <mat-icon>movie_edit</mat-icon>
                  Convert to DPG
                </button>
             </mat-card-actions>
          </mat-card>
        </ng-template>
      </div>
    </div>
  `,
  styles: [`
    .file-browser-container { display: flex; height: 100%; min-height: 600px; gap: 20px; }
    
    .browser-section { flex: 1.5; display: flex; flex-direction: column; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); overflow: hidden; }
    .info-section { flex: 1; overflow-y: auto; }

    .header { display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-bottom: 1px solid #eee; }
    .current-path { flex: 1; font-family: 'Roboto Mono', monospace; font-size: 0.85em; color: #666; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    
    .file-list { overflow-y: auto; flex: 1; }
    .selected { background-color: rgba(63, 81, 181, 0.08) !important; }
    .name { font-weight: 500; }
    .size { color: #888; }
    
    .info-card, .conversion-card { margin-bottom: 20px; }
    
    .metadata-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }
    .meta-item { display: flex; flex-direction: column; }
    .meta-item .label { font-size: 0.75em; color: #888; text-transform: uppercase; letter-spacing: 0.5px; }
    .meta-item .value { font-weight: 500; }
    
    .thumbnail-section { padding: 16px 0; }
    .thumbnail-section h4 { margin: 0 0 12px 0; font-size: 0.9em; color: #666; }
    .thumb-container { background: #f0f0f0; border-radius: 4px; overflow: hidden; height: 144px; display: flex; align-items: center; justify-content: center; position: relative; }
    .thumbnail { width: 100%; height: 100%; object-fit: contain; }
    .loading-thumb { width: 100%; padding: 0 20px; }
    .no-thumb { display: flex; flex-direction: column; align-items: center; color: #bbb; gap: 8px; }
    .no-thumb mat-icon { font-size: 40px; width: 40px; height: 40px; }

    .update-thumb-actions { display: flex; gap: 8px; margin-top: 12px; }
    
    .preview-section { padding-top: 16px; }
    .preview-btn { width: 100%; }
    .preview-btn mat-icon { margin-right: 8px; }
    video { width: 100%; margin-top: 12px; border-radius: 4px; background: black; display: block; }
    
    .no-selection { height: 200px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #999; gap: 12px; }
    .no-selection mat-icon { font-size: 48px; width: 48px; height: 48px; }
    
    .status-msg { font-size: 0.85em; margin-top: 8px; }
    .error { color: #f44336; }
    .success { color: #4caf50; }
  `]
})
export class FileBrowserComponent implements OnInit, OnDestroy {
  @Output() fileSelected = new EventEmitter<string>();

  currentPath: string = '';
  parentPath: string = '';
  items: any[] = [];
  selectedFile: string | null = null;
  dpgInfo: any = null;
  previewUrl: string | null = null;
  loadingPreview: boolean = false;
  previewError: string | null = null;

  thumbnailUrl: string | null = null;
  thumbnailError: boolean = false;
  selectedThumbnail: File | null = null;
  uploadingThumbnail: boolean = false;
  uploadError: string | null = null;
  uploadSuccess: boolean = false;

  uploadingFile: boolean = false;
  rootPath: string = '';
  private refreshSub: Subscription | null = null;

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.loadFiles();
    this.refreshSub = this.api.refreshFiles$.subscribe(() => {
      this.loadFiles(this.currentPath, true);
    });
  }

  ngOnDestroy() {
    if (this.refreshSub) {
      this.refreshSub.unsubscribe();
    }
  }

  loadFiles(path?: string, preserveSelection: boolean = false) {
    this.api.listFiles(path).subscribe({
      next: (data) => {
        this.currentPath = data.current_path;
        this.parentPath = data.parent_path;
        this.rootPath = data.root_path;
        this.items = data.items;

        if (!preserveSelection) {
          this.selectedFile = null;
          this.dpgInfo = null;
          this.resetPreview();
          this.resetThumbnail();
        } else if (this.selectedFile) {
          const stillExists = this.items.some(item => item.path === this.selectedFile);
          if (!stillExists) {
            this.selectedFile = null;
            this.dpgInfo = null;
            this.resetPreview();
            this.resetThumbnail();
          }
        }
      },
      error: (err) => console.error('Failed to load files', err)
    });
  }

  navigateUp() {
    if (this.parentPath) {
      this.loadFiles(this.parentPath);
    }
  }

  onItemClick(item: any) {
    if (item.is_dir) {
      this.loadFiles(item.path);
    } else {
      this.selectedFile = item.path;
      this.fileSelected.emit(item.path);

      if (item.name.toLowerCase().endsWith('.dpg')) {
        this.resetThumbnail();
        this.api.getDpgInfo(item.path).subscribe({
          next: (info) => {
            this.dpgInfo = info;
            this.loadThumbnail(item.path);
          },
          error: (err) => {
            console.error('Failed to load DPG info', err);
            this.dpgInfo = null;
          }
        });
      } else {
        this.dpgInfo = null;
        this.resetPreview();
        this.resetThumbnail();
      }
    }
  }

  resetPreview() {
    this.previewUrl = null;
    this.loadingPreview = false;
    this.previewError = null;
  }

  resetThumbnail() {
    this.thumbnailUrl = null;
    this.thumbnailError = false;
    this.selectedThumbnail = null;
    this.uploadingThumbnail = false;
    this.uploadError = null;
    this.uploadSuccess = false;
  }

  loadThumbnail(path: string) {
    this.thumbnailUrl = this.api.getThumbnailUrl(path);
    this.thumbnailError = false;
  }

  onThumbnailError() {
    this.thumbnailError = true;
    this.thumbnailUrl = null;
  }

  onThumbnailSelected(event: any) {
    if (event.target.files && event.target.files.length > 0) {
      this.selectedThumbnail = event.target.files[0];
      this.uploadError = null;
      this.uploadSuccess = false;
    }
  }

  uploadThumbnail() {
    if (!this.selectedFile || !this.selectedThumbnail) return;

    this.uploadingThumbnail = true;
    this.uploadError = null;
    this.api.updateThumbnail(this.selectedFile, this.selectedThumbnail).subscribe({
      next: () => {
        this.uploadingThumbnail = false;
        this.uploadSuccess = true;
        this.selectedThumbnail = null;
        this.loadThumbnail(this.selectedFile!);
      },
      error: (err) => {
        this.uploadingThumbnail = false;
        this.uploadError = 'Failed to update: ' + (err.error?.error || err.message);
      }
    });
  }

  onUploadSelected(event: any) {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      this.uploadingFile = true;
      this.api.uploadFile(this.currentPath, file).subscribe({
        next: () => {
          this.uploadingFile = false;
          this.loadFiles(this.currentPath);
        },
        error: (err) => {
          this.uploadingFile = false;
          alert('Upload failed: ' + (err.error?.error || err.message));
        }
      });
    }
  }

  download(path: string) {
    window.open(this.api.getDownloadUrl(path), '_blank');
  }

  startConversion() {
    if (!this.selectedFile) return;
    this.api.convert(this.selectedFile).subscribe({
      next: () => { },
      error: (err) => alert('Failed to start conversion: ' + (err.error?.error || err.message))
    });
  }

  generatePreview() {
    if (!this.selectedFile) return;

    this.loadingPreview = true;
    this.previewError = null;

    this.api.generatePreview(this.selectedFile).subscribe({
      next: (data) => {
        this.loadingPreview = false;
        this.previewUrl = 'http://localhost:5001' + data.preview_url;
      },
      error: (err) => {
        this.loadingPreview = false;
        this.previewError = 'Failed to generate preview: ' + (err.error?.error || err.message);
      }
    });
  }

  formatSize(bytes: number): string {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}
