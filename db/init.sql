-- CREATE DATABASE flaskpersistent;

CREATE TABLE projects (
  pid int not null auto_increment,
  name varchar(255) not null,
  primary key (pid)
);

CREATE TABLE floorplans (
  fid int not null auto_increment,
  pid int not null,
  name varchar(255) not null,
  urls varchar(5000) not null,
  primary key (fid),
  foreign key (pid) REFERENCES projects(pid)
);