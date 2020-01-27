import { Injectable } from '@angular/core';
import { CrudService } from './crud.service';
import { HttpClient } from '@angular/common/http';
import { ITemplate } from '../types';

@Injectable({
  providedIn: 'root'
})
export class TemplateService extends CrudService<ITemplate> {
  constructor(http: HttpClient) {
    super('/templates/', http);
  }

  public getFilledTemplate(employeeId: number, templateId: number) {
    return this.http.get<ITemplate>(
      '/templates/' + String(templateId) + '/' + String(employeeId) + '/'
    );
  }
}
