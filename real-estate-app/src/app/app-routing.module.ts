import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdsListComponent } from './components/ads-list/ads-list.component';
import { AdDetailsComponent } from './components/ad-details/ad-details.component';

const routes: Routes = [
  { path: 'list', component: AdsListComponent },
  { path: 'favorites', component: AdsListComponent }, 
  { path: 'details/:id', component: AdDetailsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
