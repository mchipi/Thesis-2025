import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PaginationService {
  currentPage : number = 1;
  adsPerPage : number = 30;
  totalAds : number = 0;

  pageChange : Subject<number> = new Subject<number>();

  get totalPages(): number {
    console.log('Total pages2:', Math.ceil(this.totalAds / this.adsPerPage));
    return Math.ceil(this.totalAds / this.adsPerPage);
  }

  nextPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.pageChange.next(this.currentPage);
    }
  }

  prevPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.pageChange.next(this.currentPage);
    }
  }
}
