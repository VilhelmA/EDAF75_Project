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
+ raw_materials(**ingredient_name**, balance, unit, update_date, update_amount)
+ recipe_entries(amount, **_bar\_code_**, **_ingredient\_name_**)
+ orders(**order_id**, order_date, delivery_date, **_customer\_name_**)
+ pallets(**pallet_nbr**, **_bar\_code_**, pallet_time, pallet_date, is_blocked, **_order\_id_**)
+ order_spec(**_bar\_code_**, **_order\_id_**, quantity)

[Link to the repository](https://github.com/VilhelmA/EDAF75_Project)
