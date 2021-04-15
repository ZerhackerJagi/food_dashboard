# food_dashboard
analysis of food (r/food and spoonacular)


## Requirements
- python 3.7
- python package virtualenv 
- jupyter notebook


## Basic Usage
### 1. Setting everything up

   git clone https://github.com/ZerhackerJagi/food_dashboard.git  
   cd food_dashboard  
   python -m venv name_of_your_project  
   source ./name_of_your_project/bin/activate  
   pip install -r requirements.txt  


## Mining your own data
1. Setting up your environment on debian based systems

1.1. Install your database

   sudo apt update  
   sudo apt install mariadb  

1.2. Making it safe

   sudo mysql_safe_installation  
```
Change the root password? y
Remove anonymous users? y
Disallow root login remotely? (depends on how you access your server - on your local machine: yes!)
Remove test database and access to it? y
Reload privilege tables now? y
```

1.3. Configuring your database

   mysql -u root -p [Enter] your_root_password [Enter]  
   create database reddit  

```mysql
create table reddit( 
	id int not null auto_increment,
	hour_created varchar(2), 
	time_created varchar(255), 
	day_created varchar(255), 
	author varchar(255), 
	title varchar(255), 
	ups int, 
	downs int, 
	num_comments int, 
	text varchar(255), 
	thumbnail varchar(255), 
	url varchar(255), 
	curr_time varchar(255), 
	primary key(id)
);

create table users(
	uid int auto_increment, 
	username varchar(255), 
	created_utc varchar(30), 
	is_mod tinyint, 
	is_employee tinyint, 
	link_karma int, 
	primary key(uid)
);

```

   create user 'reddituser'@'localhost' identified by 'your_password';  
   grant all on reddit.* to 'reddituser'@'localhost';  
   flush privileges  

2. Creating a cronjob for the crawler

   crontab -e (choose the editor you like - easiest of course is nano)  
   move to the last line and enter the following  
```
*/10 * * * * /usr/bin/python3.7 /path/to/your/scraper/reddit_scraper.py
```
   if you used nano use ctrl+o -> enter -> ctrl+x to safe and exit  

## Analyze the data on your own
1. Start your notebook

   jupyter notebook (leads you to your browser - start exploring)  



