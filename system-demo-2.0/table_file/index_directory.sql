CREATE TABLE IF NOT EXISTS index_directory (
    file_id STRING,
    keywords ARRAY<STRING>,
    roles ARRAY<STRING>,
    policy STRING,
    path STRING
)
STORED AS ORC
TBLPROPERTIES (
    'transactional'='true'
);
