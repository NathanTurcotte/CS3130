drop table if exists employees;
create table employees(
    id integer primary key,
    fname text not null,
    lname text not null,
    department text not null
);
