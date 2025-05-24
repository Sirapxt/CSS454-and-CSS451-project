CREATE TABLE keyword_index_nurse (
    keyword_hash STRING,
    file_id STRING
)
STORED AS ORC
TBLPROPERTIES (
    'transactional'='true'
);
