import { Component, ElementRef, ViewChild } from '@angular/core';
import { AdsService } from 'src/app/services/ads.service';
import { FavoritesService } from 'src/app/services/favorites.service';

@Component({
  selector: 'app-ads-list',
  templateUrl: './ads-list.component.html',
  styleUrls: ['./ads-list.component.css']
})
export class AdsListComponent {

  @ViewChild('imageContainer', { static: false }) imageContainer!: ElementRef;

  ads: any[] = [];
  selectedAd: any = null;

  constructor(
    private adsService: AdsService,
    private favoritesService: FavoritesService
  ) {}

  ngOnInit() {
    this.getAds();
  }

  getAds() {
    this.adsService.getProperties().subscribe(
      (data) => {
        this.ads = data;
        console.log('Ads:', this.ads);
      },
      (error) => {
        console.error('Error fetching ads:', error);
      }
    )
  }

  selectAd(ad: any) {
    this.selectedAd = ad;
    
    // Reset the image carousel scroll position to the first image
    if (this.imageContainer) {
      const container = this.imageContainer.nativeElement;
      container.scrollLeft = 0; // This ensures the first image is shown
    }
  }

  closeAdPanel() {
    this.selectedAd = null;
  }

  toggleFavorite(ad: any) {
    this.favoritesService.toggleFavorite(ad.Id);
    console.log("favorite ad ads from local storage: ", localStorage.getItem('favoriteAdIds'));
  }
  
  isFavorite(ad: any): boolean {
    return this.favoritesService.isFavorite(ad.Id);
  }

  get propertyKeys(): string[] {
    return this.selectedAd && this.selectedAd.Properties 
        ? Object.keys(this.selectedAd.Properties) 
        : [];
  }

  scrollImages(direction: number): void {
      if (this.imageContainer) {
          const container = this.imageContainer.nativeElement;
          container.scrollLeft += direction * 750; // Adjust scrolling amount
      }
  }

  showFullDescription: boolean = false;

  toggleDescription() {
      this.showFullDescription = !this.showFullDescription;
  }

  isAdFavorite(adId: string): boolean {
    const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    return favorites.includes(adId);
  }

  currentPage: number = 1;
  adsPerPage: number = 12;

  get paginatedAds(): any[] {
    const startIndex = (this.currentPage - 1) * this.adsPerPage;
    return this.ads.slice(startIndex, startIndex + this.adsPerPage);
  }

  get totalPages(): number {
    return Math.ceil(this.ads.length / this.adsPerPage);
  }

  nextPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }
  
  prevPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }

}