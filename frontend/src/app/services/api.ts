import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = '/api';

  constructor(private http: HttpClient) { }

  listFiles(path?: string): Observable<any> {
    const url = path ? `${this.baseUrl}/files?path=${encodeURIComponent(path)}` : `${this.baseUrl}/files`;
    return this.http.get(url);
  }

  getConfig(): Observable<any> {
    return this.http.get(`${this.baseUrl}/config`);
  }

  updateConfig(config: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/config`, config);
  }

  convert(file: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/convert`, { file });
  }

  getStatus(): Observable<any> {
    return this.http.get(`${this.baseUrl}/status`);
  }

  cancel(): Observable<any> {
    return this.http.post(`${this.baseUrl}/cancel`, {});
  }

  getDpgInfo(path: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/dpg/info?path=${encodeURIComponent(path)}`);
  }

  generatePreview(path: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/dpg/preview`, { path });
  }

  getThumbnailUrl(path: string): string {
    return `${this.baseUrl}/dpg/thumbnail?path=${encodeURIComponent(path)}&t=${new Date().getTime()}`;
  }

  updateThumbnail(path: string, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('path', path);
    formData.append('image', file);
    return this.http.post(`${this.baseUrl}/dpg/thumbnail`, formData);
  }

  uploadFile(path: string, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('path', path);
    formData.append('file', file);
    return this.http.post(`${this.baseUrl}/upload`, formData);
  }

  getDownloadUrl(path: string): string {
    return `${this.baseUrl}/download?path=${encodeURIComponent(path)}`;
  }
}
