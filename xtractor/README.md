# xtractor

Extract data from various news website

\*\*Steps to run the extractor

1.  create a .env folder inside xtractor and create a file called db-config.env
2.  Add below data which would be considered for postgsql parameter
    POSTGRES_PASSWORD=p@ssw0rd
    POSTGRES_DB=stockfinch
    POSTGRES_USER=app_user
3.  exec into the xtractor container got to scapers folder and run - python money_control.py

# Docker commands:

1. Set up all services 

    ```
    docker-compose up -d
    ```
2. Tear down all services

    ```
    docker-compose down
    ```

3. Run scrapers

    ```
    docker exec -it stockfinch_xtractor_1 python scrapers/money_control.py

    docker exec -it stockfinch_xtractor_1 python scrapers/economic_times.py

    docker exec -it stockfinch_xtractor_1 python scrapers/nse_indices.py

    docker exec -it stockfinch_xtractor_1 python scrapers/money_control_historical.py

    docker exec -it stockfinch_xtractor_1 python scrapers/economic_times_historical.py


    ```

4. Run psql

    ```
    docker exec -it stockfinch_db psql -U app_user -d stockfinch
    ```