WITH file_size AS (
    SELECT id, parent_id, name, type, SYS_CONNECT_BY_PATH(name, '/') path,
           COALESCE(file_size, 0) + COALESCE(
               (SELECT SUM(file_size) dir_size
               FROM file_system sub_dir
               CONNECT BY PRIOR sub_dir.id = sub_dir.parent_id
               START WITH sub_dir.parent_id = fs.id), 0) total_size
    FROM file_system fs
    CONNECT BY PRIOR fs.id = fs.parent_id
    START WITH fs.parent_id IS NULL),

     file_ratio AS (
         SELECT id, name, type, path, total_size,
                RATIO_TO_REPORT(total_size) OVER (PARTITION BY parent_id) ratio
         FROM file_size
     )

SELECT id, name, path, total_size, ratio
FROM file_ratio
WHERE type = 'DIR'
ORDER BY id;
