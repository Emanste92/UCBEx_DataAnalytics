-- mySQL Sakila sample database exercises
-- installed sql database files locally as sakila
use sakila;

-- 1a: Displaying the first and last names of all actors from the table actor.
select first_name, last_name from actor;

-- 1b. Displaying the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
select concat(first_name, ' ', last_name) as 'Actor Name' from actor;

-- 2a. Finding the ID number, first name, and last name of an actor with first name Joe
select actor_id, first_name, last_name from actor
where first_name = 'Joe';

-- 2b. Finding all actors whose last name contain the letters GEN
select actor_id, first_name, last_name from actor
where last_name like '%gen%';

-- 2c. Finding all actors whose last names contain the letters LI, results ordered by last name and first name
select last_name, first_name from actor
where last_name like '%li%';

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
select country_id, country from country
where country in ('Afghanistan', 'Bangladesh', 'China');

-- You want to keep a description of each actor. You don't think you will be performing queries on a description, so create a
-- 3a. Creating a 'description' column in the table actor with the BLOB datatype
alter table actor
add column `description` blob after last_name;    

-- 3b. Deleting the 'description' column that was just created
alter table actor
drop `description`;
select * from actor;

-- 4a. Listing actor last names and their frequencies in the database
select last_name, count(*) as `frequencies`
from actor
group by last_name;

-- 4b. Listing actor last names and frequencies of 2 or greater in the database 
select last_name, count(*) as `frequencies`
from actor
group by last_name
having count(*) >= 2;

-- 4c. Updating the record for GROUCHO WILLIAMS; changing to HARPO WILLIAMS
update actor
set first_name = 'HARPO'
where first_name = 'GROUCHO' AND actor_id > 0;

-- Note: this where statement works without having to 'SET SQL_SAFE_UPDATES = 0;'
-- see: https://stackoverflow.com/questions/11448068/mysql-error-code-1175-during-update-in-mysql-workbench
-- Checking to see if field updated
select first_name, last_name from actor
where last_name = 'WILLIAMS';

-- 4d. Changing the recent change HARPO back to GROUCHO 
update actor
set first_name = 'GROUCHO'
where first_name = 'HARPO' AND actor_id > 0;

-- Checking to see if field updated
select first_name, last_name from actor
where last_name = 'WILLIAMS';

-- 5a. Printing the query that created the 'address' table
show create table address;
-- next steps: right click create table output cell in result grid,
-- click on 'Open Value in Viewer', click on text tab to see string

-- 6a. Joinng tables address and staff by address_id to display staff members' first name, last name, and address
-- seeing how tables look like first
-- select * from address;
-- select * from staff;

select s.first_name, s.last_name, a.address, a.district
from address as a
inner join staff as s on a.address_id = s.address_id;

-- 6b. Joining tables staff and payment to display total amount rung up by each staff member in August 2005
-- seeing how tables look like first
-- select * from staff;
-- select * from payment;

select s.staff_id, s.first_name, s.last_name, sum(p.amount)
from payment as p
inner join staff as s on p.staff_id = s.staff_id
where payment_date like '2005-08-%'
group by s.staff_id;

-- 6c. Listing each film and the number of actors listed for that film
-- seeing how tables look like first
-- select * from film_actor;
-- select * from film;

select f.film_id, f.title, count(fa.film_id) as 'number of actors'
from film as f
inner join film_actor as fa on f.film_id = fa.film_id
group by f.title;

-- 6d. Displaying the number of copies of 'Hunchback Impossible' in inventory table
-- seeing how tables look like first
-- select * from inventory;

select title, (
	select count(*)
	from inventory
	where film.film_id = inventory.film_id) as 'Number of copies'
from film
where title = 'Hunchback Impossible';

-- 6e. Listing the total paid by each customer, ordering this list alphabetically by last name
-- seeing how tables look like first
-- select * from payment;
-- select * from customer;

select c.last_name, c.first_name, sum(p.amount) as 'total paid'
from customer as c
inner join payment as p on p.customer_id = c.customer_id
group by c.last_name
order by c.last_name;

-- 7a. Using subqueries to display movie titles starting with K and Q that are in English
-- seeing how tables look like first
-- NEED TO DOUBLE CHECK DIS ONE
-- select * from film;
-- select * from `language`;

select title
from film
where ((title like 'K%') or 
	  (title like 'Q%'))
	and language_id in (
		select language_id
		from `language`
		where name = 'English'
	);

-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.
-- DOUBLE CHECK
select first_name, last_name
from actor
where actor_id in (
	select actor_id
	from film_actor
	where film_id in (
		select film_id
		from film
		where title = 'Alone Trip'
		)
	);

-- 7c. Using joins to display the names and email addresses of all Canadian customers
-- seeing how tables look like first
-- select * from customer;
-- select * from address;
-- select * from city;
-- select * from country;
-- note: display code to see if the id joins match
-- select c.last_name, c.first_name, c.email, c.address_id, a.district, a.city_id,
-- ci.city_id, ci.country_id, co.country_id

-- DOUBLE check this, really only 5 output?

select c.last_name, c.first_name, c.email
from customer as c
inner join address as a on c.address_id = a.address_id
inner join city as ci on a.city_id = ci.city_id
inner join country as co on ci.country_id = co.country_id
where co.country = 'Canada'
order by c.last_name;

-- 7d. Displaying all movies categorized as family films.
-- seeing how tables look like first
-- select * from film;
-- select * from film_category;
-- select * from category;
-- note: display code to see if the id joins match
-- select f.title, f.rating, f.film_id, fc.film_id, fc.category_id, c.category_id, c.`name`

select f.title, f.rating, f.film_id, fc.film_id, fc.category_id
from film as f
inner join film_category as fc on f.film_id = fc.film_id 
inner join category as c on fc.category_id = c.category_id
where c.`name` = 'Family'
order by f.title;

-- 7e. Displaying the most frequently rented movies in descending order
-- seeing how tables look like first
select * from rental;
select * from inventory;
select * from film;
-- note: display code to see if the id joins match
-- select f.title, f.film_id, r.rental_id, r.inventory_id, i.inventory_id, i.film_id

-- DOUBLE CHECK

select f.title, count(f.film_id) as 'times rented (descending)'
from inventory as i
inner join rental as r on i.inventory_id = r.inventory_id
inner join film as f on i.film_id = f.film_id
group by f.title
order by count(f.film_id) desc; 

-- 7f. Displaying the dollar amount each store brought in
-- seeing how tables look like first
-- select * from store;
-- select * from customer;
-- select * from payment;
-- note: display code to see if the id joins match
-- select s.store_id, c.store_id, c.customer_id, p.customer_id, sum(p.amount)

select s.store_id, sum(p.amount) as 'store total earnings'
from store as s
inner join customer as c on s.store_id = c.store_id
inner join payment as p on c.customer_id = p.customer_id
group by s.store_id;

-- 7g. Displaying each store ID's city and country.
-- seeing how tables look like first
-- select * from store;
-- select * from address;
-- select * from city;
-- select * from country;
-- note: display code to see if the id joins match
-- select s.store_id, s.address_id, a.address_id, a.city_id, ci.city_id, ci.city, ci.country_id, co.country_id, co.country

select s.store_id, ci.city, co.country
from store as s
inner join address as a on s.address_id = a.address_id
inner join city as ci on a.city_id = ci.city_id
inner join country as co on ci.country_id = co.country_id
group by s.store_id;

-- 7h. Listing the top five genres in gross revenue in descending order
-- seeing how tables look like first
select * from category;
select * from film_category;
select * from inventory;
select * from payment;
select * from rental;
-- note: display code to see if the id joins match
-- select c.`name`, c.category_id, fc.category_id, fc.film_id, r.rental_id, r.inventory_id, 
-- i.inventory_id, i.film_id, p.rental_id, sum(p.amount)

-- DOUBLE CHECK

select c.`name`, sum(p.amount) as 'gross revenue'
from category as c
inner join film_category as fc on c.category_id = fc.category_id
inner join inventory as i on fc.film_id = i.film_id
inner join rental as r on i.inventory_id = r.inventory_id
inner join payment as p on r.rental_id = p.rental_id
group by c.`name`
order by sum(p.amount) desc limit 5; 

-- 8a. Creating a view for the top 5 genres by gross revenue using the solution above 
create view `Top 5 Genres by Gross Revenue` as
	select c.`name`, sum(p.amount) as 'gross revenue'
	from category as c
	inner join film_category as fc on c.category_id = fc.category_id
	inner join inventory as i on fc.film_id = i.film_id
	inner join rental as r on i.inventory_id = r.inventory_id
	inner join payment as p on r.rental_id = p.rental_id
	group by c.`name`
	order by sum(p.amount) desc limit 5; 

-- 8b. Displaying the view created above
select * from `Top 5 Genres by Gross Revenue`;

-- 8c. Deleting the view created above
drop view if exists `Top 5 Genres by Gross Revenue`;