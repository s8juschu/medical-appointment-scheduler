import { Injectable } from '@angular/core';
import { IDepartment } from '../types';
import { HttpClient } from '@angular/common/http';
import { CrudService } from './crud.service';

@Injectable({
  providedIn: 'root'
})
export class DepartmentsService extends CrudService<IDepartment> {
  constructor(http: HttpClient) {
    super('/departments/', http);
  }
}
