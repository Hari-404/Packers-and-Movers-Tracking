Uses python 3

Requements:
sqlite3 -> for database
flask -> for running web application


Install above packages using pip command

run "python3 web.py"

Open localhost:5000 in browser



Contains user page and Admin page.

User Page:
-----------
+New user can sign up.
+User login into his account and make a order by selecting source and destination.
+Generates unique order ID/Track ID. 
+User can view his history of orders by providing track ID/order ID or he can see all orders made by him/her.

email id : user1@mail.com
password : 1234

email id : user2@mail.com
password : 1234

Admin Page:
------------
+Admin enters into admin page and performs like view history of orders made by all customers.
+Admin can move a package from one location to another location and change status of the order.
+The same will be reflect to the customer.
