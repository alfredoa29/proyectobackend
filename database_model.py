import oracledb


# metodo al que se le pasan los datos para la conexion a la bd oracle
def conexion_bd():
    try:

        conexion = oracledb.connect(
            user="system",
            password="root",
            dsn="192.168.50.82:1521/XE"
        )
        return conexion
    except oracledb.DatabaseError as e:
        print(f"Error conectado {e}")
        return None


# query  para obtener los datos de la vista con la informacion de los tablespaces de la db
def tablespace_usage():
    query = """
    SELECT 
        tablespace_name,
        total_space,
        free_space,
        (total_space - free_space) * 100 / total_space AS used_percentage,
        free_space * 100 / total_space AS free_percentage
    FROM (
        SELECT 
            tablespace_name,
            SUM(bytes) AS total_space,
            SUM(CASE WHEN status = 'FREE' THEN bytes ELSE 0 END) AS free_space
        FROM dba_data_files
        GROUP BY tablespace_name
    )
    """

    connection = conexion_bd()
    if connection is None:
        return []

    cursor = connection.cursor()
    cursor.execute(query)

    # se recorre el query y se mete a la una lista asi cuenta cuantos tablespaces hay disponibles y su resp info
    result = []
    for row in cursor:
        result.append({
            "tablespace_name": row[0],
            "total_space": row[1],
            "free_space": row[2],
            "used_percentage": row[3],
            "free_percentage": row[4]
        })

    cursor.close()
    connection.close()

    return result


def conexiones_activas():
    query = """
    SELECT username, status, COUNT(*) AS numero_sesiones
FROM v$session
GROUP BY username, status


    """

    connection = conexion_bd()
    if connection is None:
        return []

    cursor = connection.cursor()
    cursor.execute(query)

    result = []
    for row in cursor:
        result.append({
            "username": row[0] if row[0] is not None else "Internal/Background Process",
            "status": row[1],
            "numero_sesiones": row[2]
        })

    cursor.close()
    connection.close()

    return result


def estado_backups():
    query = """
    SELECT 
        bs.backup_type,  -- Tipo de backup (FULL, INCREMENTAL)
        MAX(bs.start_time) AS last_backup_date,  -- Última fecha de backup
        SUM(bp.bytes) AS total_size_bytes,  -- Tamaño total ocupado por los archivos de backup en bytes
        ROUND(SUM(bp.bytes) / 1024 / 1024, 2) AS total_size_mb  -- Tamaño total en MB
    FROM 
        v$backup_set bs
    JOIN 
        v$backup_piece bp ON bs.set_stamp = bp.set_stamp AND bs.set_count = bp.set_count
    GROUP BY 
        bs.backup_type
    ORDER BY 
        last_backup_date DESC  -- Ordenar por la última fecha de backup
    """

    connection = conexion_bd()
    cursor = connection.cursor()
    cursor.execute(query)

    result = []
    for row in cursor:
        result.append({
            "backup_type": row[0],
            "last_backup_date": row[1],
            "total_size_bytes": row[2],
            "total_size_mb": row[3]
        })

    cursor.close()
    connection.close()

    if not result:
        return {"message": "No hay backups disponibles."}

    return {"backups": result}


def estado_tablespaces():
    query = """
     SELECT 
        tablespace_name,
        SUM(bytes) / 1024 / 1024 AS total_size_mb,
        SUM(CASE WHEN file_id IS NOT NULL THEN bytes ELSE 0 END) / 1024 / 1024 AS used_size_mb,
        (SUM(bytes) - SUM(CASE WHEN file_id IS NOT NULL THEN bytes ELSE 0 END)) / 1024 / 1024 AS free_size_mb,
        ROUND(SUM(CASE WHEN file_id IS NOT NULL THEN bytes ELSE 0 END) / SUM(bytes) * 100, 2) AS used_percentage,
        ROUND((SUM(bytes) - SUM(CASE WHEN file_id IS NOT NULL THEN bytes ELSE 0 END)) / SUM(bytes) * 100, 2) AS free_percentage
    FROM 
        dba_data_files
    GROUP BY 
        tablespace_name

    """

    connection = conexion_bd()
    cursor = connection.cursor()
    cursor.execute(query)

    result = []
    for row in cursor:
        result.append({
            "tablespace_name": row[0],
            "total_size_mb": row[1],
            "used_size_mb": row[2],
            "free_size_mb": row[3],
            "used_percentage": row[4],
            "free_percentage": row[5]
        })

    cursor.close()
    connection.close()

    if not result:
        return {"message": "No hay info disponible."}

    return result


def alertas_eventos_criticos():
    query = """

        SELECT 
        ORIGINATING_TIMESTAMP, 
        MESSAGE_TEXT, 
        MESSAGE_LEVEL, 
        HOST_ID 
    FROM 
        X$DBGALERTEXT
    ORDER BY 
        ORIGINATING_TIMESTAMP DESC
    FETCH FIRST 10 ROWS ONLY
    """

    connection = conexion_bd()
    cursor = connection.cursor()
    cursor.execute(query)

    result = []

    for row in cursor:
        result.append({
            "ORIGINATING_TIMESTAMP": row[0],
            "MESSAGE_TEXT": row[1],
            "Mesage_LEVEL": row[2],
            "HOST_ID": row[3]
        })

    cursor.close()
    connection.close()

    if not result:
        return {"message": "No hay info"}

    return result


def monitoreo_lectua_escritura_disco():
    query = """
        SELECT 
        (SELECT VALUE FROM V$SYSSTAT WHERE NAME = 'physical reads') AS physical_reads,
        (SELECT VALUE FROM V$SYSSTAT WHERE NAME = 'physical writes') AS physical_writes,
        (SELECT VALUE FROM V$SYSSTAT WHERE NAME = 'physical read total bytes') AS read_bytes,
        (SELECT VALUE FROM V$SYSSTAT WHERE NAME = 'physical write total bytes') AS write_bytes
    FROM 
        dual
    """

    connection = conexion_bd()
    cursor = connection.cursor()
    cursor.execute(query)

    result = []

    for row in cursor:
        result.append({
            "PHYSICAL_READS": row[0],
            "Physical WRITES": row[1],
            "Read Bytes": row[2],
            "write Bytes": row[3]
        })

    cursor.close()
    connection.close()

    if not result:
        return {"message": "No hay info disponible."}

    return result