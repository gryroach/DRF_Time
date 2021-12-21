# DRF_Time
DRF project for time check by post method
## Setup
The first thing to do is to clone the repository:
```sh
$ git clone https://github.com/gryroach/DRF_Time.git
$ cd DRF_Time
```
Create a virtual environment to install dependencies in and activate it:
```sh
$ pip install virtualenv
$ python3 -m venv env
$ source env/bin/activate
```
Then install the dependencies:
```sh
(env)$ pip install -r requirements.txt
```
Once pip has finished downloading the dependencies:
```sh
(env)$ cd DRF_time
(env)$ python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` to see available urls.
## Work
In order to check the time, you can use two methods:
- Checking the time accurate to the minute - `http://127.0.0.1:8000/time-is-right/`
- Checking the time with the specified accuracy (delta) - `http://127.0.0.1:8000/time-plus-delta-is-right/`

Time is checked by post-request to the corresponding address. Data is sent in json format.
Example of data:
- `http://127.0.0.1:8000/time-is-right/`:
```json
{ 
"time": "15:00" 
}
```
- `http://127.0.0.1:8000/time-plus-delta-is-right/`:
```json
{ 
"time": "15:20:00",
"delta": "00:05:30"
}
```

The check is carried out by comparing the entered data with the time on the server in accordance with the set time zone (by default Europe/Moscow). 

The result is displayed in json format as follows:
```json
{ 
"result": "True" 
}
```
