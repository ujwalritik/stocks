--We will create a table to store stock today data with time_stamp

Use Stock;
create sequence stock_serial_no start with 1000 increment by 1;


--drop table today_stock;
create table toady_stock(
	serial_no integer default next value for stock_serial_no primary key,
	stock_ticker varchar(20),
	open_price decimal(10,2),
	high_price decimal(10,2),
	low_price decimal(10,2),
	close_price decimal(10,2),
	volume bigint,
	on_date date default getdate()
)

select * from toady_stock;