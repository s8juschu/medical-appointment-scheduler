import { Injectable } from '@angular/core';
import { IAppointment } from '../types';
import { CrudService } from './crud.service';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AppointmentsService extends CrudService<IAppointment> {
  constructor(http: HttpClient) {
    super('/appointments/', http);
  }
}
