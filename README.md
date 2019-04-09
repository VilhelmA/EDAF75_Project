# EDAF75 Database Project

This is the report for

+ Vilhelm Åkerström, dat15vak
+ Emil Ahlberg, har12eah
+ Ola Johansson, jur10ojo

We solved this project on our own, except for:

+ The Peer-review meeting

![Database design uml](databas_design.png)

## Relations:

+ recipes(**bar_code**, name)
+ customers(**customer_name**, address)
+raw_materials(**ingredient_name**, balance, unit, update_date, update_amount)
+ recipe\*entries(amount, \*\*\_bar*code**\*, **\_ingredient_name*\*\*)
+ orders(**order_id**, order*date, delivery_date, \*\*\_customer_name*\*\*)
+ pallets(**pallet_nbr**, **_bar_code_**, pallet*time, pallet_date, is_blocked, \*\*\_order_id*\*\*)
+ order\*spec(\*\*\_bar*code**\*, **\_order_id*\*\*, quantity)

[Link to the repository](https://github.com/VilhelmA/EDAF75_Project)

## How to run

+ cd to git repository
+ run the following commands:
+ sqlite3 applications.sqlite < create+schema.sql
+ python rest.py
+ server is now running on localhost:8888
+ to populate the database use curl -X POST http://localhost:8888/reset
