import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  template: `
    <header style="display: flex; align-items: center; gap: 15px; padding: 15px; background: #f8f9fa; border-bottom: 1px solid #dee2e6;">
      <img src="assets/logo.png" alt="DPG4x Logo" style="height: 50px;">
      <h1 style="margin: 0; font-size: 1.5rem; color: #333;">DPG4x Web</h1>
    </header>
    <main style="padding: 20px;">
      <router-outlet />
    </main>
  `,
  styles: [],
})
export class App {
  protected readonly title = signal('frontend');
}
