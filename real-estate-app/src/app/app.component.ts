import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { PaginationService } from './services/pagination.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(
    private router: Router,
    public paginationService: PaginationService
  ) {}

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

  get currentPage() {
    return this.paginationService.currentPage;
  }

  get totalPages() {
    console.log('Total pages:', this.paginationService.totalPages);
    return this.paginationService.totalPages;
  }

  nextPage() {
    this.paginationService.nextPage();
    this.scrollToTop();
  }
  
  prevPage() {
    this.paginationService.prevPage();
    this.scrollToTop();
  }

  get showPagination(): boolean {
    return this.router.url === '/list';
  }

  scrollToTop() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth' // optional: makes it smooth
    });
  }
}
