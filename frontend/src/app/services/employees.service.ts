import { Injectable } from "@angular/core";
import { IEmployee } from "../types";
import { HttpClient } from "@angular/common/http";
import { CrudService } from "./crud.service";

@Injectable({
  providedIn: "root"
})
export class EmployeesService extends CrudService<IEmployee> {
  constructor(http: HttpClient) {
    super("/employees/", http);
  }
}
