import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AdsService {

  private apiUrl = 'http://127.0.0.1:5000/';

  constructor(private http: HttpClient) { }

  getPaginatedAds(page: number, perPage: number): Observable<any> {
    const params = new HttpParams()
      .set('page', page.toString())
      .set('per_page', perPage.toString());
  
    return this.http.get(this.apiUrl + 'api/property/mock_paginated', { params });
  }  

  getAds(): Observable<any> {
    return this.http.get<any>(this.apiUrl + 'api/property/mock');
  }
  
  getProperties(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}