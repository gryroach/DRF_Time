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
(env)$ touch .env
(env)$ vim .env
```
Define the following environment variables:
- ```DEBUG```
- ```SECRET_KEY```
- ```ALLOWED_HOSTS```
- ```POSTGRES_DB```
- ```POSTGRES_USER```
- ```POSTGRES_PASSWORD```
- ```POSTGRES_HOST```
- ```POSTGRES_PORT```
- ```REMOTE_TIME_URL```
- ```DELTA_TIME_DEFAULT```

After that, do the following:

```sh
(env)$ cd DRF_time
(env)$ python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` to see available urls.
## Work
In order to check the time you will use method with the specified accuracy (delta). If delta is not specified explicitly, then it is equal to `DELTA_TIME_DEFAULT` (%H:%M:%S format)

Time is checked by post-request to the address `http://127.0.0.1:8000/time-is-right/`. 

Data is sent in json format. Example:
```json
{ 
"time": "15:20:00",
"delta": "00:05:30"
}
```

The check is carried out by comparing the entered data with the time on the server in accordance with `REMOTE_TIME_URL`. 

The result is displayed in json format as follows:
```json
{ 
"result": "true" 
}
```
