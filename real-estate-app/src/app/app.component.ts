import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private router: Router) {}

  navigateToHome() {
    this.router.navigate(['/list']);
  }

  navigateToFavorites() {
    this.router.navigate(['/favorites']);
  }

  isFavoritesRoute(): boolean {
    return this.router.url.includes('/favorites');
  }

  isHomeRoute(): boolean {
    return this.router.url === '/list';
  }
}
