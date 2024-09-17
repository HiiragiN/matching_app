GRANT ALL privileges on *.* to `mariadb`@`%`;
create table if not exists myoji(id int primary key auto_increment, kanji varchar(255), kana varchar(255), roma varchar(255));
create table if not exists name(id int primary key auto_increment, kanji varchar(255), kana varchar(255), roma varchar(255),
                    gender varchar(255));
create table if not exists star_sign_match(starsign int, matching_star_sign int);
insert ignore into star_sign_match (starsign, matching_star_sign) value ("1", "6"), ("2", "9"), ("3", "8"),
("4", "11"), ("5", "10"), ("6", "1"), ("7", "12"), ("8", "3"), ("9", "2"), ("10", "5"), ("11", "4"), ("12", "7");
create table if not exists starsign(id int primary key auto_increment, starsign varchar(255));
insert ignore into starsign (starsign) value ("牡羊座"), ("牡牛座"), ("双子座"), ("蟹座"), ("獅子座"), ("乙女座"), ("天秤座"),
("蟹座"), ("射手座"), ("山羊座"), ("水瓶座"), ("魚座");
create table if not exists user_data(id int primary key auto_increment, fullname varchar(255), read_fullname varchar(255),
email varchar(255), hobby varchar(255), birthday varchar(255), starsign int, gender varchar(10),
job varchar(255), income varchar(255));
create table if not exists relation_id(id int, kc_id varchar(255), email varchar(255));