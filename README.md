# Automated timetable generator
Automated timetable generator for schedule class schedules using the genetic algorithm. The algorithm will consider 10 teachers, 5 classes, 5 sections and 10 rooms.

## Features:
* After each class, there will be a break. break time will be definable. And there will be lunchtime which also be defineable for its start time and break length.
* The timetable should be regenerateable. and for the first 3 generations, the data will be stored in the database. we will consider 5 days for a week.
* The timetable generator has to generate a weekly schedule for all sections of classes.
* In this timetable, Admin can choose the starting time of the break, the starting time of lunch, and class duration.
* Break time and lunchtime duration can choose using the dropdown bar.
* During the distribution of the instructor, it must be aware of the instructor’s shift and working hours/day so that the instructor’s shift can’t change and working hours can’t be exceeded, and don't overlap the instructor's time.
* Don’t overlap with the instructors as well as room numbers.
* All the needed information like room numbers, teacher’s details, subjects name, classes, sections etc. have to trace from the database.
* Admin will have the opportunity to regenerate the table if he wants but only up to 3 times will be stored the regenerated table in the database, the rest of the time only generate without storing it in the database.


