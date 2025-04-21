import { Component, ElementRef, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { AdsService } from 'src/app/services/ads.service';
import { FavoritesService } from 'src/app/services/favorites.service';
import { PaginationService } from 'src/app/services/pagination.service';

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
    private favoritesService: FavoritesService,
    public paginationService: PaginationService,
    private router: Router,
  ) {}

  ngOnInit() {
    if (this.router.url === '/favorites'){
      this.getFavoriteAds();
      return;
    }

    this.paginationService.pageChange.subscribe((page: number) => {
      this.getPaginatedAds(page, this.paginationService.adsPerPage);
    });
  
    // Initial load
    this.getPaginatedAds(this.paginationService.currentPage, this.paginationService.adsPerPage);
  }

  getFavoriteAds() {
    this.adsService.getAds().subscribe(
      (data) => {
        this.ads = data.filter((ad: any) => {
          const favorites = JSON.parse(localStorage.getItem('favoriteAdIds') || '[]');
          return favorites.includes(ad.Id);
        });
      },
      (error) => {
        console.error('Error fetching ads:', error);
      }
    )
  }

  getPaginatedAds(page: number, perPage: number) {
    this.adsService.getPaginatedAds(page, perPage).subscribe(
      (response) => {
        this.ads = response.ads;
        this.paginationService.totalAds = response.total;
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



}