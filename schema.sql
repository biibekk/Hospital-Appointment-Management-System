-- sqlite3 app.db < schema.sql
PRAGMA foreign_keys = ON;

create table if not exists patient(
    patient_id integer primary key autoincrement,
    name text not null,
    dob date not null,
    gender text not null,
    contact text not null
);

create table if not exists doctor(
    doctor_id integer primary key autoincrement,
    name text not null,
    specialisation text not null,
    consultation_fee integer default 1000
);

create table if not exists doctorschedule(
    schedule_id integer primary key autoincrement,
    doctor_id integer not null,
    date date not null,
    start_time time not null,
    end_time time not null,
    slot_duration integer not null,

    check(start_time < end_time),
    check(slot_duration > 0),
    foreign key(doctor_id) references doctor(doctor_id) on delete cascade
);

create table if not exists appointments(
    appointment_id integer primary key autoincrement,
    patient_id integer not null,
    doctor_id integer not null,
    date date not null,
    start_time time not null,
    end_time time not null,
    status text not null default 'BOOKED'
        check (status in ('BOOKED', 'CANCELLED', 'COMPLETED')),
    priority integer not null default 2
        check(priority in (1,2)),
    appointment_cost integer not null,
    problem_description text not null,

    check(start_time < end_time),
    foreign key(patient_id) references patient(patient_id) on delete cascade,
    foreign key(doctor_id) references doctor(doctor_id) on delete cascade
);

create unique index unique_active_appointment
on appointments(doctor_id, date, start_time)
where status != 'CANCELLED';