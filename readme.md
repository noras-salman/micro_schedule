# micro_schedule

## Config
You need to define your triggers as a json array in the file ./config
Here are some examples (see json below):
- Example1: Trigger every minute
- Example2: Trigger every monday at 11:01:01
- Example3: Trigger every weekend at 05:00:00
- Example4: Trigger every weekday at 15:30:00
- Example5: Trigger on 29-june at 18:15:00
```json
[
    {
        "at_weekday":"any",
        "at_hour":"any",
        "at_minute":"any",
        "at_second":"0",
        "at_day":"any",
        "at_month":"any",
        "url":"https://www.example.com"
    },
     {
        "at_weekday":"monday",
        "at_hour":"11",
        "at_minute":"1",
        "at_second":"1",
        "at_day":"any",
        "at_month":"any",
        "url":"https://www.example.com"
    },
     {
        "at_weekday":"weekend",
        "at_hour":"5",
        "at_minute":"0",
        "at_second":"0",
        "at_day":"any",
        "at_month":"any",
        "url":"https://www.example.com"
    },
     {
        "at_weekday":"weekday",
        "at_hour":"15",
        "at_minute":"30",
        "at_second":"0",
        "at_day":"any",
        "at_month":"any",
        "url":"https://www.example.com"
    },
     {
        "at_weekday":"any",
        "at_hour":"18",
        "at_minute":"15",
        "at_second":"0",
        "at_day":"29",
        "at_month":"6",
        "url":"https://www.example.com"
    }
]
```

## Enable file logs and timezone
```yml
version: "3.2"
services:
    micro_schedule_service:
        build: ./
        volumes:
            - ./:/micro_schedule
        environment: 
            - ENABLE_LOGS=true
            - TZ=Europe/Stockholm
        restart: always
```

## Runing
```sh
docker-compose up
```