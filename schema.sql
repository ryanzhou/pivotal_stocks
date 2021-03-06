drop table if exists stocks;
create table stocks (
  id integer primary key autoincrement,
  asx_code string not null,
  company_name string not null,
  sector string,
  market_cap integer not null,
  div_yield decimal(8,2) not null,
  pe_ratio decimal(8,2),
  franking integer not null,
  asx200 boolean default 'f' not null,
  eps decimal(8,2),
  tsr_3y decimal(8,2),
  market_cap_bin string,
  franking_bin string,
  div_yield_bin string,
  eps_bin string,
  tsr_3y_bin string
);
