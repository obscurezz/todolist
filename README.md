# TODOLIST for SKYPRO

***

## Initialize local postgres DB and api

* you have to install local environment, try `export $(cat .testenv | xargs)`
* up docker container with db and api `docker-compose up -d --build`

# Success result is:

>[+] Running 4/4
> - Container todolist_pg_db               Healthy                                                                                                                                                                                 13.2s 
> - Container actual_project-migrations-1  Exited                                                                                                                                                                                  14.2s 
> - Container api                          Started                                                                                                                                                                                 14.6s
> - Container todolist_nginx_front         Started                                                                                                                                                                                  4.7s

***

## Application deployed to `akopylov.ga`

* Try testing registration, login and password change
