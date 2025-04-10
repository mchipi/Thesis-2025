import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AdsService } from '../../services/ads.service';

@Component({
  selector: 'app-ad-details',
  templateUrl: './ad-details.component.html',
  styleUrls: ['./ad-details.component.css']
})
export class AdDetailsComponent implements OnInit {
  property: any | null = null;

  constructor(private route: ActivatedRoute, private adsService: AdsService) {}

  ngOnInit(): void {
    const propertyId = this.route.snapshot.paramMap.get('id'); // Get the ID from the route
    if (propertyId) {
      this.adsService.getProperties().subscribe(
        (data) => {
          // Find the property by ID
          this.property = data.find((prop: any) => prop.id === +propertyId);
          console.log('Property details:', this.property);
        },
        (error) => {
          console.error('Error fetching property details:', error);
        }
      );
    }
  }

  getKeys(obj: any): string[] {
    return Object.keys(obj);
  }
}