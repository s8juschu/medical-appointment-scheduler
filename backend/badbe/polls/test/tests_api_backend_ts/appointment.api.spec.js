const chakram = require("chakram");
const expect = chakram.expect;
const url = "http://localhost:8000/appointments/";
const id = 9;

describe("Appointment API", () => {
  it("Should require an employee as id", () => {
    const res = chakram.post(url, { date: "2016-01-01" });
    expect(res).to.have.status(400);
    return chakram.wait();
  });

  it("Should require a date", () => {
    const res = chakram.post(url, { employee: 1 });
    expect(res).to.have.status(400);
    return chakram.wait();
  });

  it("Should be able to create an appointment", () => {
    return chakram.post(url, { employee: 1, date: "2016-01-01" }).then(res => {
      expect(res).to.have.status(201);
      expect(res.body).to.have.property("employee");
      expect(res.body).to.have.property("date");
      expect(res.body.employee).to.be.equal(1);
      expect(res.body.date).to.be.equal("2016-01-01");
    });
  });

  it("Should be able to query an appointment by id", () => {
    return chakram.get(url + id + "/").then(res => {
      expect(res).to.have.status(200);
      expect(res.body).to.have.property("id");
      expect(res.body).to.have.property("date");
      expect(res.body).to.have.property("employee");
      expect(res.body.employee).to.be.a("number");
      expect(res.body.id).to.be.eqal(id);
    });
  });

  it("Should be able to query all appointments", () => {
    return chakram.get(url).then(res => {
      expect(res).to.have.status(200);
      expect(res.body).to.have.property("results");
      expect(res.body.results).to.have.property("length");
    });
  });

  it("Should be able to update an appointment", () => {
    const res = chakram.patch(url + id + "/", { date: "2017-02-02" });
    expect(res).to.have.status(200);
    return chakram.wait();
  });

  it("Should be able to delete an user", () => {
    const res = chakram.delete(url + id + "/");
    expect(res).to.have.status(204);
    return chakram.wait();
  });

  it("Should not be able to find deleted appointments", () => {
    const res = chakram.get(url + id + "/");
    expect(res).to.have.status(404);
    return chakram.wait();
  });
});
