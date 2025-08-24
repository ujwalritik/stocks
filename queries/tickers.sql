--We will create table

create sequence ticker_no start with 1000 increment by 1;
--drop sequence ticker_no;
Use Stock;
--drop table tickers;
create table tickers(
	serial_no integer,
	Stock_Name varchar(500),
	Stock_ticker varchar(20) primary key
);