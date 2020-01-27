import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export abstract class CrudService<Type> {
  constructor(private url: string, protected http: HttpClient) {}

  public get(filter: any = {}): Observable<Type[]> {
    let params = new HttpParams();
    for (const key in filter) {
      if (!(filter == null || filter === undefined)) {
        params = params.append(String(key), String(filter[key]));
      }
    }
    return this.http.get<Type[]>(this.url, { params });
  }

  public getById(id: number): Observable<Type> {
    return this.http.get<Type>(this.url + String(id) + '/');
  }

  public create(partial: Partial<Type>): Observable<Type> {
    return this.http.post<Type>(this.url, partial);
  }

  public update(id: number, partial: Partial<Type>): Observable<Type> {
    return this.http.patch<Type>(this.url + String(id) + '/', partial);
  }

  public delete(id: number): Observable<void> {
    return this.http.delete<void>(this.url + String(id) + '/');
  }
}
