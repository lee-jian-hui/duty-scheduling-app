## SETUP
refer to `SETUP.md`


## Features:
Staff Manager to add/delete staffs
![alt text](images/staff.png)

Scheduler Calendar
- intelligent scheduling
- clean UI
![alt text](images/schedule_cal.png)
- picker to upsert staff schedule
![alt text](images/picker.png)
- schedule export to csv
![alt text](images/exportcsv1.png)
![alt text](images/exportcsv2.png)

## Backend Architecture
![alt text](images/arch.png)



## Known Bugs / Issues / Improvements
- no loading modal on frontend to prevent db lock contention operations causing race conditions without user's knowledge
- Setup docker compose orchestration flows