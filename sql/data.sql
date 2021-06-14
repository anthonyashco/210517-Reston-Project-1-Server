begin;

insert into expense.user values (default, 'manager@email.com', '153417bd132637ba71cf236c323a55bd', '71a8b28bf9986f51ab5e31c1c20993f3', 'manager', 'expense', 'manager');
insert into expense.user values (default, 'employee@email.com', '153417bd132637ba71cf236c323a55bd', '71a8b28bf9986f51ab5e31c1c20993f3', 'employee', 'expense', 'employee');
insert into expense.user values (default, 'closed@email.com', '153417bd132637ba71cf236c323a55bd', '71a8b28bf9986f51ab5e31c1c20993f3', 'closed', 'expense', 'closed');

commit;
