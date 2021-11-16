alter table hedgefunds.book8_paiva2
rename column ï»¿Product  to Product;

create table hedgefunds.paiva as
SELECT Product, FinancialPrice, STR_TO_DATE(data, '%d/%m/%Y %H:%i:%s') as date_value
FROM hedgefunds.book8_paiva2;

create table hedgefunds.paive2
SELECT * FROM hedgefunds.database
union all
SELECT * FROM hedgefunds.paiva;

drop table hedgefunds.database;

ALTER TABLE hedgefunds.paive2
RENAME TO 'database';

drop table hedgefunds.paive2;