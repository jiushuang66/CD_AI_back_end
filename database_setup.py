from __future__ import annotations

import os
from typing import Dict

import pymysql
from urllib.parse import parse_qs, urlparse


def parse_mysql_url(url: str) -> Dict:
    parsed = urlparse(url)
    if parsed.scheme not in ("mysql", "mysql+pymysql"):
        raise ValueError("DATABASE_URL must start with mysql:// or mysql+pymysql://")

    user = parsed.username or "root"
    password = parsed.password or ""
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 3306
    db = parsed.path.lstrip("/") or None
    qs = parse_qs(parsed.query)
    charset = qs.get("charset", ["utf8mb4"])[0]

    return dict(host=host, port=port, user=user, password=password, database=db, charset=charset)


DEFAULT_DB_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@127.0.0.1:3306/cd_ai_db?charset=utf8mb4",
)


STUDENTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS `students` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `student_id` VARCHAR(20) UNIQUE COMMENT '学号',
    `name` VARCHAR(128) NOT NULL COMMENT '姓名',
    `grade` VARCHAR(64) DEFAULT NULL COMMENT '年级',
    `class_name` VARCHAR(64) DEFAULT NULL COMMENT '班级',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_student_id (student_id),
    INDEX idx_name (name),
    INDEX idx_grade (grade),
    INDEX idx_class_name (class_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""


TEACHERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS `teachers` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `teacher_id` VARCHAR(64) UNIQUE COMMENT '教师工号',
    `name` VARCHAR(128) NOT NULL COMMENT '姓名',
    `department` VARCHAR(128) DEFAULT NULL COMMENT '院系/部门',
    `title` VARCHAR(64) DEFAULT NULL COMMENT '职称',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_teacher_id (teacher_id),
    INDEX idx_name (name),
    INDEX idx_department (department)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""


ADMINS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS `admins` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `admin_id` VARCHAR(64) UNIQUE COMMENT '管理员账号ID',
    `name` VARCHAR(128) NOT NULL COMMENT '姓名',
    `role` VARCHAR(64) DEFAULT 'admin' COMMENT '管理员角色',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_admin_id (admin_id),
    INDEX idx_name (name),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""


# 修改file_records表，使用name字段代替author_name，保持一致性
FILE_RECORDS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS `file_records` (
  `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(128) NOT NULL COMMENT '作者/上传者姓名',
  `filename` VARCHAR(255) NOT NULL COMMENT '文件名',
  `upload_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
  `storage_path` VARCHAR(500) NOT NULL COMMENT '文件存储地址',
  `file_type` ENUM('document', 'essay') NOT NULL DEFAULT 'document' COMMENT '文件类型：document(文档)或essay(文章)',
  `version` INT NOT NULL DEFAULT 1 COMMENT '版本号',
  `remark` TEXT COMMENT '备注',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  INDEX idx_name (name),
  INDEX idx_filename (filename),
  INDEX idx_upload_time (upload_time),
  INDEX idx_file_type (file_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""


def init_db(database_url: str | None = None) -> None:
    """Create base tables if missing (one-time use)."""
    url = database_url or DEFAULT_DB_URL
    params = parse_mysql_url(url)

    conn = pymysql.connect(
        host=params["host"],
        port=params["port"],
        user=params["user"],
        password=params["password"],
        database=params["database"],
        charset=params.get("charset", "utf8mb4"),
        autocommit=True,
    )

    try:
        with conn.cursor() as cur:
            for sql in (STUDENTS_TABLE_SQL, TEACHERS_TABLE_SQL, ADMINS_TABLE_SQL, FILE_RECORDS_TABLE_SQL):
                cur.execute(sql)
        print("Tables ensured: students, teachers, admins, file_records")
    finally:
        conn.close()


def _get_existing_columns(conn: pymysql.connections.Connection, db_name: str, table: str) -> set:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
            (db_name, table),
        )
        return {row[0] for row in cur.fetchall()}


def _get_existing_indexes(conn: pymysql.connections.Connection, db_name: str, table: str) -> set:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT INDEX_NAME FROM information_schema.STATISTICS WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
            (db_name, table),
        )
        return {row[0] for row in cur.fetchall()}


# 统一管理各表的字段定义
TABLE_COLUMN_DEFINITIONS = {
    "students": {
        "id": "`id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY",
        "student_id": "`student_id` VARCHAR(20) UNIQUE COMMENT '学号'",
        "name": "`name` VARCHAR(128) NOT NULL COMMENT '姓名'",
        "grade": "`grade` VARCHAR(64) DEFAULT NULL COMMENT '年级'",
        "class_name": "`class_name` VARCHAR(64) DEFAULT NULL COMMENT '班级'",
        "created_at": "`created_at` DATETIME DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "`updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
    },
    "teachers": {
        "id": "`id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY",
        "teacher_id": "`teacher_id` VARCHAR(64) UNIQUE COMMENT '教师工号'",
        "name": "`name` VARCHAR(128) NOT NULL COMMENT '姓名'",
        "department": "`department` VARCHAR(128) DEFAULT NULL COMMENT '院系/部门'",
        "title": "`title` VARCHAR(64) DEFAULT NULL COMMENT '职称'",
        "created_at": "`created_at` DATETIME DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "`updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
    },
    "admins": {
        "id": "`id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY",
        "admin_id": "`admin_id` VARCHAR(64) UNIQUE COMMENT '管理员账号ID'",
        "name": "`name` VARCHAR(128) NOT NULL COMMENT '姓名'",
        "role": "`role` VARCHAR(64) DEFAULT 'admin' COMMENT '管理员角色'",
        "created_at": "`created_at` DATETIME DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "`updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
    },
    "file_records": {
        "id": "`id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY",
        "name": "`name` VARCHAR(128) NOT NULL COMMENT '作者/上传者姓名'",
        "filename": "`filename` VARCHAR(255) NOT NULL COMMENT '文件名'",
        "upload_time": "`upload_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间'",
        "storage_path": "`storage_path` VARCHAR(500) NOT NULL COMMENT '文件存储地址'",
        "file_type": "`file_type` ENUM('document', 'essay') NOT NULL DEFAULT 'document' COMMENT '文件类型：document(文档)或essay(文章)'",
        "version": "`version` INT NOT NULL DEFAULT 1 COMMENT '版本号'",
        "remark": "`remark` TEXT COMMENT '备注'",
        "created_at": "`created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间'",
        "updated_at": "`updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间'",
    },
}


TABLE_INDEX_DEFINITIONS = {
    "students": [
        "CREATE INDEX idx_student_id ON `students` (student_id)",
        "CREATE INDEX idx_name ON `students` (name)",
        "CREATE INDEX idx_grade ON `students` (grade)",
        "CREATE INDEX idx_class_name ON `students` (class_name)"
    ],
    "teachers": [
        "CREATE INDEX idx_teacher_id ON `teachers` (teacher_id)",
        "CREATE INDEX idx_name ON `teachers` (name)",
        "CREATE INDEX idx_department ON `teachers` (department)"
    ],
    "admins": [
        "CREATE INDEX idx_admin_id ON `admins` (admin_id)",
        "CREATE INDEX idx_name ON `admins` (name)",
        "CREATE INDEX idx_role ON `admins` (role)"
    ],
    "file_records": [
        "CREATE INDEX idx_name ON `file_records` (name)",
        "CREATE INDEX idx_filename ON `file_records` (filename)",
        "CREATE INDEX idx_upload_time ON `file_records` (upload_time)",
        "CREATE INDEX idx_file_type ON `file_records` (file_type)"
    ],
}


def sync_schema(database_url: str | None = None) -> None:
    """Ensure tables exist and add missing columns/indexes dynamically."""
    url = database_url or DEFAULT_DB_URL
    params = parse_mysql_url(url)

    conn = pymysql.connect(
        host=params["host"],
        port=params["port"],
        user=params["user"],
        password=params["password"],
        database=params["database"],
        charset=params.get("charset", "utf8mb4"),
        autocommit=True,
    )

    try:
        # Create base tables if missing
        with conn.cursor() as cur:
            for sql in (STUDENTS_TABLE_SQL, TEACHERS_TABLE_SQL, ADMINS_TABLE_SQL, FILE_RECORDS_TABLE_SQL):
                cur.execute(sql)

        db_name = params["database"]

        # Add missing columns
        for table, cols in TABLE_COLUMN_DEFINITIONS.items():
            existing = _get_existing_columns(conn, db_name, table)
            for col_name, col_def in cols.items():
                if col_name not in existing:
                    stmt = f"ALTER TABLE `{table}` ADD COLUMN {col_def};"
                    with conn.cursor() as cur:
                        cur.execute(stmt)

        # Ensure indexes
        for table, idx_list in TABLE_INDEX_DEFINITIONS.items():
            existing_idx = _get_existing_indexes(conn, db_name, table)
            for idx_sql in idx_list:
                # Parse index name from SQL
                parts = idx_sql.split()
                idx_name = None
                try:
                    if "UNIQUE" in parts:
                        idx_name = parts[3]
                    else:
                        idx_name = parts[2]
                except Exception:
                    continue

                if idx_name and idx_name in existing_idx:
                    continue

                with conn.cursor() as cur:
                    try:
                        cur.execute(idx_sql)
                    except pymysql.err.InternalError:
                        # Retry without IF NOT EXISTS if needed
                        cur.execute(idx_sql)

        print("Schema synchronized (added missing columns/indexes if any).")
    finally:
        conn.close()


if __name__ == "__main__":
    sync_schema()
