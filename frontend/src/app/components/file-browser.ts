import { Component, OnInit, OnDestroy, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api';
import { Subscription } from 'rxjs';
import { ProgressComponent } from './progress';

@Component({
  selector: 'app-file-browser',
  standalone: true,
  imports: [CommonModule, ProgressComponent],
  template: `
    <div class="file-browser-container">
      <div class="browser-section">
        <div class="header">
          <button (click)="navigateUp()" [disabled]="!parentPath">⬆ Up</button>
          <span class="current-path">{{ currentPath }}</span>
          <div class="upload-actions">
            <input type="file" #fileInput (change)="onUploadSelected($event)" style="display: none">
            <button (click)="$event.stopPropagation(); fileInput.click()" [disabled]="uploadingFile">
              {{ uploadingFile ? 'Uploading...' : 'Upload File' }}
            </button>
          </div>
        </div>
        <ul class="file-list">
          <li *ngFor="let item of items" (click)="onItemClick(item)" [class.selected]="selectedFile === item.path">
            <span class="icon">{{ item.is_dir ? '📁' : '📄' }}</span>
            <span class="name">{{ item.name }}</span>
            <span class="size" *ngIf="!item.is_dir">{{ formatSize(item.size) }}</span>
            <div class="actions" *ngIf="!item.is_dir">
               <a [href]="getDownloadUrl(item.path)" target="_blank" (click)="$event.stopPropagation()">⬇</a>
            </div>
          </li>
        </ul>
      </div>

      <div class="info-section">
        <app-progress [selectedFile]="selectedFile"></app-progress>

        <div class="dpg-info" *ngIf="dpgInfo; else noDpg">
          <h3>DPG Info</h3>
          <div class="metadata">
            <p><strong>Version:</strong> {{ dpgInfo.version }}</p>
            <p><strong>Frames:</strong> {{ dpgInfo.frames }}</p>
            <p><strong>FPS:</strong> {{ dpgInfo.fps }}</p>
            <p><strong>Duration:</strong> {{ dpgInfo.duration_seconds | number:'1.0-2' }}s</p>
            <p><strong>Video Size:</strong> {{ formatSize(dpgInfo.video_size) }}</p>
            <p><strong>Audio Size:</strong> {{ formatSize(dpgInfo.audio_size) }}</p>
          </div>

          <div class="thumbnail-section">
            <h4>Thumbnail</h4>
            <div class="thumb-container">
              <img [src]="thumbnailUrl" alt="DPG Thumbnail" (error)="onThumbnailError()" class="thumbnail" *ngIf="thumbnailUrl">
              <div *ngIf="!thumbnailUrl && !thumbnailError" class="loading">Loading thumbnail...</div>
              <div *ngIf="thumbnailError" class="no-thumb">No thumbnail available</div>
            </div>
            
            <div class="update-thumb">
              <label class="file-label">
                <span>Change Thumbnail:</span>
                <input type="file" (change)="onThumbnailSelected($event)" accept="image/*">
              </label>
              <button (click)="uploadThumbnail()" [disabled]="!selectedThumbnail || uploadingThumbnail">
                {{ uploadingThumbnail ? 'Uploading...' : 'Update' }}
              </button>
              <div *ngIf="uploadError" class="error">{{ uploadError }}</div>
              <div *ngIf="uploadSuccess" class="success">Thumbnail updated!</div>
            </div>
          </div>
          
          <div class="preview-section">
            <button class="preview-btn" (click)="generatePreview()" [disabled]="loadingPreview" *ngIf="!previewUrl">
              {{ loadingPreview ? 'Generating Preview...' : 'Preview Video' }}
            </button>
            <div *ngIf="previewError" class="error">{{ previewError }}</div>
            <video *ngIf="previewUrl" [src]="previewUrl" controls autoplay width="100%"></video>
          </div>
        </div>
        <ng-template #noDpg>
          <div class="no-selection" *ngIf="!selectedFile">
            <p>Select a file to see details</p>
          </div>
          <div class="conversion-section" *ngIf="selectedFile && !dpgInfo">
             <div class="selected-header">
                <h3>Selected: {{ selectedFile.split('/').pop() }}</h3>
             </div>
             <div class="conversion-actions">
                <p>Convert this file to DPG format for playback.</p>
                <button class="convert-btn" (click)="startConversion()">
                  Convert to DPG
                </button>
             </div>
          </div>
        </ng-template>
      </div>
    </div>
  `,
  styles: [`
    .file-browser-container { display: flex; border: 1px solid #ddd; border-radius: 8px; height: 650px; background: white; overflow: hidden; }
    
    .browser-section { flex: 1.5; display: flex; flex-direction: column; border-right: 1px solid #eee; }
    .info-section { flex: 1; background: #fafafa; overflow-y: auto; padding: 15px; }

    .header { display: flex; align-items: center; gap: 10px; padding: 15px; border-bottom: 1px solid #eee; background: #fff; }
    .current-path { font-family: monospace; font-size: 0.85em; color: #666; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }
    
    .file-list { list-style: none; padding: 0; margin: 0; overflow-y: auto; flex: 1; }
    .file-list li { display: flex; align-items: center; padding: 10px 15px; cursor: pointer; border-bottom: 1px solid #f9f9f9; transition: background 0.1s; }
    .file-list li:hover { background-color: #f5f5f5; }
    .file-list li.selected { background-color: #e3f2fd; border-left: 3px solid #2196f3; padding-left: 12px; }
    
    .icon { margin-right: 12px; font-size: 1.2em; }
    .name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 0.95em; }
    .size { font-size: 0.8em; color: #999; margin-left: 10px; }
    
    .dpg-info h3 { margin: 0 0 15px 0; font-size: 1.1em; color: #333; }
    .metadata p { margin: 5px 0; font-size: 0.9em; line-height: 1.4; color: #555; }
    
    .thumbnail-section { margin-top: 20px; padding: 15px; background: white; border: 1px solid #eee; border-radius: 6px; }
    .thumbnail-section h4 { margin: 0 0 10px 0; font-size: 0.95em; }
    .thumb-container { display: flex; justify-content: center; background: #eee; border-radius: 4px; overflow: hidden; min-height: 120px; align-items: center; }
    .thumbnail { max-width: 100%; height: auto; display: block; }
    
    .update-thumb { margin-top: 15px; display: flex; flex-direction: column; gap: 10px; }
    .file-label { font-size: 0.85em; display: flex; flex-direction: column; gap: 5px; }
    .file-label input { font-size: 0.9em; }
    
    .preview-section { margin-top: 20px; }
    .preview-btn { width: 100%; padding: 10px; background: #2196f3; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: 500; }
    .preview-btn:hover { background: #1976d2; }
    
    .conversion-section { padding: 10px; }
    .selected-header h3 { margin: 0 0 15px 0; font-size: 1.1em; color: #333; word-break: break-all; }
    .conversion-actions { background: white; padding: 20px; border-radius: 8px; border: 1px solid #eee; }
    .conversion-actions p { margin: 0 0 20px 0; color: #666; font-size: 0.9em; }
    .convert-btn { width: 100%; padding: 12px; background: #4caf50; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: 600; font-size: 1em; transition: background 0.2s; }
    .convert-btn:hover { background: #388e3c; }

    .no-selection { height: 100%; display: flex; align-items: center; justify-content: center; color: #999; font-style: italic; }
    
    .error { color: #d32f2f; font-size: 0.85em; margin-top: 5px; }
    .success { color: #388e3c; font-size: 0.85em; margin-top: 5px; }
    video { margin-top: 10px; border-radius: 4px; background: black; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    
    .upload-actions { margin-left: auto; }
    .actions { margin-left: 10px; opacity: 0.5; transition: opacity 0.2s; }
    li:hover .actions { opacity: 1; }
    .actions a { text-decoration: none; font-size: 1.1em; }
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

    // Listen for file refresh requests
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
        this.rootPath = data.root_path; // Capture (new) root path from backend
        this.items = data.items;

        if (!preserveSelection) {
          this.selectedFile = null;
          this.dpgInfo = null;
          this.resetPreview();
          this.resetThumbnail();
        } else if (this.selectedFile) {
          // If preserving selection, we might want to refresh dpgInfo if the file still exists
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
        // Reload thumbnail to show new image
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
          this.loadFiles(this.currentPath); // Refresh list
        },
        error: (err) => {
          this.uploadingFile = false;
          alert('Upload failed: ' + (err.error?.error || err.message));
        }
      });
    }
  }

  getDownloadUrl(path: string): string {
    return this.api.getDownloadUrl(path);
  }

  startConversion() {
    if (!this.selectedFile) return;
    this.api.convert(this.selectedFile).subscribe({
      next: () => {
        // The ProgressComponent already listens for status changes
        // No need for extra feedback here besides the conversion starting
      },
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
        // Backend returns relative path like /static/previews/...
        // We need to prepend backend URL if running on different port in dev
        // But for now assuming proxy or same origin
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
