import { Component, OnInit, OnDestroy, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-file-browser',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="file-browser">
      <div class="header">
        <button (click)="navigateUp()" [disabled]="!parentPath">⬆ Up</button>
        <span class="current-path">{{ currentPath }}</span>
        <div class="upload-actions">
          <input type="file" #fileInput (change)="onUploadSelected($event)" style="display: none">
          <button (click)="fileInput.click()" [disabled]="uploadingFile">
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
      <div class="dpg-info" *ngIf="dpgInfo">
        <h3>DPG Info</h3>
        <p><strong>Version:</strong> {{ dpgInfo.version }}</p>
        <p><strong>Frames:</strong> {{ dpgInfo.frames }}</p>
        <p><strong>FPS:</strong> {{ dpgInfo.fps }}</p>
        <p><strong>Duration:</strong> {{ dpgInfo.duration_seconds | number:'1.0-2' }}s</p>
        <p><strong>Video Size:</strong> {{ formatSize(dpgInfo.video_size) }}</p>
        <p><strong>Audio Size:</strong> {{ formatSize(dpgInfo.audio_size) }}</p>

        <div class="thumbnail-section">
          <h4>Thumbnail</h4>
          <img [src]="thumbnailUrl" alt="DPG Thumbnail" (error)="onThumbnailError()" class="thumbnail" *ngIf="thumbnailUrl">
          <div *ngIf="!thumbnailUrl && !thumbnailError" class="loading">Loading thumbnail...</div>
          <div *ngIf="thumbnailError" class="no-thumb">No thumbnail available</div>
          
          <div class="update-thumb">
            <label>Change Thumbnail: 
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
          <button (click)="generatePreview()" [disabled]="loadingPreview" *ngIf="!previewUrl">
            {{ loadingPreview ? 'Generating Preview...' : 'Preview Video' }}
          </button>
          <div *ngIf="previewError" class="error">{{ previewError }}</div>
          <video *ngIf="previewUrl" [src]="previewUrl" controls autoplay width="100%"></video>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .file-browser { border: 1px solid #ccc; padding: 10px; border-radius: 4px; height: 600px; display: flex; flex-direction: column; }
    .header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #eee; }
    .current-path { font-family: monospace; font-size: 0.9em; color: #666; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .file-list { list-style: none; padding: 0; margin: 0; overflow-y: auto; flex: 1; }
    .file-list li { display: flex; align-items: center; padding: 5px; cursor: pointer; border-radius: 3px; }
    .file-list li:hover { background-color: #f5f5f5; }
    .file-list li.selected { background-color: #e3f2fd; }
    .icon { margin-right: 10px; }
    .name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .size { font-size: 0.8em; color: #999; margin-left: 10px; }
    .dpg-info { margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee; font-size: 0.9em; overflow-y: auto; max-height: 300px; }
    .dpg-info h3 { margin: 0 0 5px 0; font-size: 1em; }
    .dpg-info p { margin: 2px 0; }
    .preview-section { margin-top: 10px; }
    .thumbnail-section { margin: 10px 0; padding: 10px; background: #f9f9f9; border-radius: 4px; }
    .thumbnail { max-width: 256px; max-height: 192px; border: 1px solid #ddd; }
    .update-thumb { margin-top: 5px; display: flex; flex-direction: column; gap: 5px; }
    .error { color: red; font-size: 0.9em; margin-top: 5px; }
    .success { color: green; font-size: 0.9em; margin-top: 5px; }
    video { margin-top: 10px; border-radius: 4px; background: black; }
    .upload-actions { margin-left: auto; }
    .actions { margin-left: 10px; }
    .actions a { text-decoration: none; font-size: 1.2em; }
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
      this.loadFiles(this.currentPath);
    });
  }

  ngOnDestroy() {
    if (this.refreshSub) {
      this.refreshSub.unsubscribe();
    }
  }

  loadFiles(path?: string) {
    this.api.listFiles(path).subscribe({
      next: (data) => {
        this.currentPath = data.current_path;
        this.parentPath = data.parent_path;
        this.rootPath = data.root_path; // Capture (new) root path from backend
        this.items = data.items;
        this.selectedFile = null;
        this.dpgInfo = null;
        this.resetPreview();
        this.resetThumbnail();
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
