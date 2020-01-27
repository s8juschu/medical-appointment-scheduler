export class IEmployee {
  id: number;
  first_name: string;
  last_name: string;
  employee_id: string;
  date_of_birth: Date;
  date_of_entry: Date;
  date_of_exit: Date;
  next_appointment: Date;
  gender: string;
  reminder_interval: number; // time delta
  department: number;
  notes: string;
  wants_reminder: boolean;
  active: boolean;
  next_reminder: string;
}
