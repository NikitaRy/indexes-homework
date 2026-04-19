# Отчет по лабораторной работе "Clickhouse"
Clickhouse -- это колоночная база данных. В данной работе выполнены задания из репозитория: 
БД поднимается из докер-контейнера. 

## Предварительные шаги
* Запускаем compose-файл и через Locust (порт 8089) делаем нагрузку
* Clickhouse расположен на localhost:8123/play

## Отчет
### Метрики
Выполним следующий запрос, чтобы узнать доступные метрики:

```sql
SELECT
    metric,
    count(*) as data_points
FROM metrics
GROUP BY metric;
```

#### Результат
metric                                 | data_points
pastebin_db_queries_rate               | 6670
pastebin_http_request_duration_seconds | 6733
pastebin_http_requests_rate            | 8643
pastebin_pastes_created_total          | 2311
pastebin_db_queries_total              | 6715
pastebin_pastes_created_rate           | 2296
pastebin_http_requests_total           | 8702

### Считаем RPS
Выполним запрос, что подсчитать rpc за последние 30 секунд для API энтрипойнтов:

```sql
SELECT
    round(sum(avg_rate), 2) AS rps
FROM (
    SELECT
        labels['method'] AS method,
        labels['path'] AS path,
        labels['status_code'] AS status_code,
        avg(value) AS avg_rate
    FROM metrics
    WHERE metric = 'pastebin_http_requests_rate'
      AND labels['path'] LIKE '/api/%'
      AND timestamp >= now() - INTERVAL 30 SECOND
    GROUP BY method, path, status_code
)
```

#### Результат
RPS: 32.8