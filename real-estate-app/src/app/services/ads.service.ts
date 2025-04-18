import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AdsService {

  private apiUrl = 'http://127.0.0.1:5000/api/property/mock';

  constructor(private http: HttpClient) { }

  getProperties(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}