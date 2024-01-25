create table if not exists customers (
	customer_id uuid primary key,
	cpf varchar(14) unique,
    first_name varchar(30),
    last_name varchar(30),
    email varchar(80),
    phone varchar(20)
);
