import datetime as dt

from database import connection

def matching_user(db_connection, email=""):
    with db_connection.cursor() as cursor:
        sql = f"""
        select m.full_name as 'full name', m.read_fullname as 'reading', m.email as 'mail',  
        m.hobby as 'hobby', m.gender as gender, m.job as job, m.income as income, m.birthday as birthday, 
        ss.starsign as constellation from user_data as m join (select u.gender as gender, u.starsign as starsign, 
        s.matching_star_sign as matching_star_sign from user_data as u join star_sign_match as s 
        on u.starsign = s.starsign where u.email = "{email}") as ud on ud.matching_star_sign = m.starsign join starsign as ss 
        on ss.id = m.starsign where ud.gender != m.gender order by rand() limit 15
        """

        cursor.execute(sql)
        match_data = cursor.fetchall()

        birth = [d.get("birthday") for d in match_data]

        for i, md in enumerate(birth):
            bd_data = md.split('.')
            bd_object = dt.date(year=int(bd_data[0]), month=int(bd_data[1]), day=int(bd_data[2]))
            age_gap = dt.date.today() - bd_object
            age = round(age_gap.days / 365)
            match_data[i]['age'] = age

    return match_data


if __name__ == "__main__":
    print(matching_user(db_connection=connection))
