drop table if exists users;
create table users(
	username text primary key,
	password text
);
drop table if exists messages;
create table messages(
	id integer primary key autoincrement,
	sender text,
	receiver text,
	message text
);
drop table if exists friends;
create table friends(
	id integer primary key autoincrement,
	owner text,
	friend text
);
