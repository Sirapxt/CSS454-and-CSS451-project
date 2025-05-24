CREATE TABLE keyword_index_doctor (
    keyword_hash STRING,
    file_id STRING
)
STORED AS ORC
TBLPROPERTIES (
    'transactional'='true'
);
