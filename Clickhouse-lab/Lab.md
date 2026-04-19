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
Выполним запрос, что подсчитать rps за последние 30 секунд для API энтрипойнтов:

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

### Считаем P99 Latency
Выполним запрос, чтобы посчитать 99 парцентиль времени запроса:

```sql
SELECT
    round(quantile(0.99)(value), 3) AS p99_seconds
FROM metrics
WHERE metric = 'pastebin_http_request_duration_seconds'
  AND labels['path'] LIKE '/api/%'
  AND timestamp >= now() - INTERVAL 30 SECOND
```

#### Результат
P99: 0.029

### RPS в динамике
Выведем 21 значение rps за 30 секундный промежуток при помощи запроса:

```sql
SELECT
    time,
    round(sum(avg_rate), 2) AS rps
FROM (
    SELECT
        toStartOfInterval(timestamp, INTERVAL 30 SECOND) AS time,
        labels['method'] AS method,
        labels['path'] AS path,
        labels['status_code'] AS status_code,
        avg(value) AS avg_rate
    FROM metrics
    WHERE metric = 'pastebin_http_requests_rate'
      AND labels['path'] LIKE '/api/%'
      AND timestamp >= now() - INTERVAL 10 MINUTE
    GROUP BY time, method, path, status_code
)
GROUP BY time
ORDER BY time
```

#### Результат
21 значение порядка ~32 (30.8 -- 33.3)

### Статистика по всем эндпоинтам
Выполним следующий запрос:

```sql
SELECT
    path AS endpoint,
    sum(requests) AS total_requests
FROM (
    SELECT
        labels['path'] AS path,
        labels['method'] AS method,
        labels['status_code'] AS status_code,
        max(value) - min(value) AS requests
    FROM metrics
    WHERE metric = 'pastebin_http_requests_total'
      AND labels['path'] LIKE '/api/%'
      AND timestamp >= now() - INTERVAL 5 MINUTE
    GROUP BY path, method, status_code
)
GROUP BY path
ORDER BY total_requests DESC
```

#### Результат

end_point         | total_requests
/api/v1/paste/:id | 8211
/api/v1/paste     | 1686

### Количество ошибок 5xx
Расчитаем процент пятисотых ошибок:

```sql
WITH request_counts AS (
    SELECT
        status_code,
        sum(requests) AS total_requests
    FROM (
        SELECT
            labels['method'] AS method,
            labels['path'] AS path,
            labels['status_code'] AS status_code,
            max(value) - min(value) AS requests
        FROM metrics
        WHERE metric = 'pastebin_http_requests_total'
          AND timestamp >= now() - INTERVAL 1 MINUTE
        GROUP BY method, path, status_code
    )
    GROUP BY status_code
)
SELECT
    round(
        sumIf(total_requests, status_code LIKE '5%') * 100.0 / sum(total_requests),
        2
    ) AS error_rate_percent
FROM request_counts
```

#### Результат
0 
##### Замечание
Нагрузка малая, поэтому ничего не падает. Но большую мой компьютер не выдаст

### QPS

```sql
SELECT
    time,
    round(sum(avg_rate), 2) AS qps
FROM (
    SELECT
        toStartOfMinute(timestamp) AS time,
        labels['operation'] AS operation,
        avg(value) AS avg_rate
    FROM metrics
    WHERE metric = 'pastebin_db_queries_rate'
      AND timestamp >= now() - INTERVAL 10 MINUTE
    GROUP BY time, operation
)
GROUP BY time
ORDER BY time
```

#### Результат
Выводит количество запросов за минутный интервал в течение десяти минут. Значения порядка 33

---

### Prewhere

```sql
SELECT
    path AS endpoint,
    sum(requests) AS total_requests
FROM (
    SELECT
        labels['path'] AS path,
        labels['method'] AS method,
        labels['status_code'] AS status_code,
        max(value) - min(value) AS requests
    FROM metrics
    PREWHERE metric = 'pastebin_http_requests_total'
      AND timestamp >= now() - INTERVAL 5 MINUTE
    WHERE labels['path'] LIKE '/api/%'
    GROUP BY path, method, status_code
)
GROUP BY path
ORDER BY total_requests DESC
```

### Запрос к агрегированным данным

```sql
SELECT
    minute,
    avg(avg_value) AS avg_latency
FROM metrics_1min
WHERE metric = 'pastebin_http_request_duration_seconds'
  AND minute >= now() - INTERVAL 30 MINUTE
GROUP BY minute
ORDER BY minute
```