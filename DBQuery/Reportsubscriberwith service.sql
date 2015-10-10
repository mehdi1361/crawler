SELECT * from users LIMIT 100;

select State.stateName,count(users.id) from users
INNER  JOIN PrefixNum on PrefixNum.idPrefixNum = users.idPrefixNum
INNER JOIN City on City.idCity = PrefixNum.IdCity
INNER  join State on State.idState = City.IdState
where users.service_id in (11,14)
      and created_at BETWEEN  '2015-09-19 00:00:00' and '2015-10-02 23:59:59'
      and subscribed =1
GROUP BY State.stateName
LIMIT  100;


select * from services where id in (11,14);