import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class FavoritesService {
  private storageKey = 'favoriteAdIds';

  getFavorites(): string[] {
    const stored = localStorage.getItem(this.storageKey);
    return stored ? JSON.parse(stored) : [];
  }

  isFavorite(adId: string): boolean {
    return this.getFavorites().includes(adId);
  }

  addFavorite(adId: string): void {
    const favorites = this.getFavorites();
    if (!favorites.includes(adId)) {
      favorites.push(adId);
      localStorage.setItem(this.storageKey, JSON.stringify(favorites));
    }
  }

  removeFavorite(adId: string): void {
    const favorites = this.getFavorites().filter(id => id !== adId);
    localStorage.setItem(this.storageKey, JSON.stringify(favorites));
  }

  toggleFavorite(adId: string): void {
    this.isFavorite(adId) ? this.removeFavorite(adId) : this.addFavorite(adId);
  }
}
