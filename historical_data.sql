-- We will create a master table to store historical price data of stocks

create sequence stock_historical_data_serial_no start with 0 increment by 1;
--alter sequence stock_historical_data_serial_no restart with 7279641 increment by 1;
--drop sequence stock_historical_data_serial_no

--drop table historical_data
create table historical_data(
serial_no integer default next value for stock_historical_data_serial_no primary key,
	stock_ticker varchar(20),
	open_price decimal(10,2),
	high_price decimal(10,2),
	low_price decimal(10,2),
	close_price decimal(10,2),
	volume bigint,
	on_date date
)

CREATE NONCLUSTERED INDEX [historical_data_index] ON 
[dbo].[historical_data] ([stock_ticker]) INCLUDE 
([open_price],[high_price],[low_price],[close_price],[volume],[on_date])

select * from historical_data order by serial_no desc;


--7279641 Serial number --