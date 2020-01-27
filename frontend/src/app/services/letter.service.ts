import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Injectable({
  providedIn: "root"
})
export class LetterService {
  constructor(private http: HttpClient) {}

  getHTML(employeeId: number) {
    return this.http.get("/gen-html/" + String(employeeId) + "/", {
      responseType: "text"
    });
  }

  getPDF(employeeId) {
    return this.http.get<File>("/gen-pdf/" + String(employeeId) + "/");
  }

  getTemplate() {
    return this.http.get("/get-template/", { responseType: "text" });
  }

  updateTemplate(template: string) {
    return this.http.post("/update-template/", template, {});
  }
}
