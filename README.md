# gpsr
- ubuntu server czy coś tam podobnego, python3 i pip3 doinstalować jak nie ma
- potem git clone git@github.com:gkujawsk/gpsr.git
- potem po wejściu do katalogu gpsr
    - pip3 install -f requirements.txt
    - python3 manage.py migrate && python3 manage.py createsuperuser
- potem testowo python3 manage.py runserver 0.0.0.0:8080
- Z przeglądarki teraz powinno udać się dostać pod http://0.0.0.0:8080 i zalogować na usera założonego we wcześniejszym kroku

- Jak zadziałało, to teraz na NGFW trzeba trochę skonfigurować.
- Device > Server Profiles > HTTP > Add >
[Servers]
Name: gpreports
Address: Adres IP serwera z appką
Port: 8080
HTTP Method: POST
[Payload Format > System ]
Name: reports
URI FORMAT: /api/globalprotectevent/
Payload: $opaque

- Idziesz do device > logging settings > System > Add i tworzysz nowy wpis
z filtrem ( eventid eq globalprotectgateway-regist-succ ) or ( eventid eq globalprotectgateway-logout-succ )
i wysyłasz logi do profilu HTTP utworzonego powyżej.
