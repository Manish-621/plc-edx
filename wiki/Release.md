After running migration for the first time run the following code 


```
insert into openedx.course_overviews_coursecustomdetails
(course_key,display_name, Duration, FocusArea)
SELECT id, display_name, Duration, FocusArea FROM openedx.course_overviews_courseoverview
where id not in
(select course_key from openedx.course_overviews_coursecustomdetails);

 

SET SQL_SAFE_UPDATES = 0;

 

update openedx.course_overviews_courseoverview co INNER JOIN openedx.course_overviews_coursecustomdetails ccd
set course_custom_details_id = ccd.id
where ccd.course_key = co.id;

update openedx.course_overviews_coursecustomdetails ccd
INNER JOIN openedx.course_overviews_coursetype ct
set course_type_choice = ct.type
where ct.id = ccd.course_type_id
 
SET SQL_SAFE_UPDATES = 1;
```
