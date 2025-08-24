-- We will create this database for handaling live data


create sequence live_data_serial_number start with 1000 increment by 1;
--drop sequence live_data_serial_number

--drop table live_data;
create table live_data(
serial_no integer default next value for live_data_serial_number primary key,
ticker varchar(20),
ltp decimal(10,2),
volume bigint,
last_time Datetime default getdate()
);

alter table live_data alter column volume bigint;