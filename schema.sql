drop table if exists stocks;
create table stocks (
  id integer primary key autoincrement,
  ticker string not null,
  company_name string not null,
  industry_group string,
  market_cap integer not null,
  div_yield decimal(8,2) not null,
  pe_ratio decimal(8,2),
  franking_percentage integer not null,
  asx_200 boolean
);
