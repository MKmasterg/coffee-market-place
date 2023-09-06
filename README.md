
# CoffeeMarketPlace

A simple coffee market place written with Django!
# How Does It Work?
This application consists of two sections:

 1. Sellers/Supervisors; Who sell products and manage markets
 2. Customers; Who buy stuff
 
 You just have to register as either of those and you're good to go!
 
 **Sellers/Supervisors:**
 When you first register as seller the application suggests either create a market and become a supervisor and the seller of your market yourself or ask from a supervisor you know to assign you as their market's seller; Either way seller's work is to manage orders and stock management.
 A supervisor's job as mentioned is market management and seller assignment plus sellers' job.  
 
 **Markets:**
 Markets are places for sellers and customers to get in touch and interact; When you first create a market you need Admin's (The superuser of the whole site and the one who can access django's admin site) permission in order to get you're market accessible to users.
 
**Customers:**
 Customers' job is to buy and place order.
 
**NoRole/BaseUser:**
Each user after basic registration doesn't have any roles so the application considers them as "NoRole"s or  "BaseUser"s and suggest them to get a role immediately! 

**This application is in state of developing and bugs and vulnerabilities are to be expected, If noticed any please commit.**
**I also appreciate your commits if you have better and efficient ways of doing things in mind for functions and views of this application**
