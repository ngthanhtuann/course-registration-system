import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


class Database:
    """Quản lý kết nối PostgreSQL và vòng đời truy vấn/giao dịch của một thao tác."""

    def __init__(self):
        """Mở kết nối từ biến môi trường; không ghi thông tin mật khẩu ra log."""
        self.conn = psycopg2.connect(
            connect_timeout=5,
            host=os.getenv("db_host", "localhost"),
            port=os.getenv("db_port", "5432"),
            database=os.getenv("db_name", "course_registration_system"),
            user=os.getenv("db_user", "postgres"),
            password=os.getenv("db_password", ""),
        )

    def execute_query(self, query, params=None):
        """Thực thi lệnh ghi và commit; trả số hàng tác động thay vì cursor đã đóng."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, params)
            self.conn.commit()
            return cursor.rowcount

        except Exception:
            self.conn.rollback()
            raise

        finally:
            cursor.close()

    def execute(self, query, params=None):
        """Thực thi lệnh ghi trong giao dịch hiện tại; bên gọi chủ động commit."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(query, params)
            return cursor.rowcount
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        """Đọc một hàng dạng dictionary hoặc None và luôn đóng cursor sau truy vấn."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, params)
            return cursor.fetchone()

        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """Đọc tất cả hàng dạng dictionary; giữ giao dịch và khóa cho bên gọi."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, params)
            return cursor.fetchall()

        finally:
            cursor.close()

    def close(self):
        """Đóng kết nối; PostgreSQL hủy giao dịch chưa commit và giải phóng khóa."""
        if self.conn:
            self.conn.close()


def get_db():
    """Tạo kết nối riêng cho thao tác; bên gọi phải đóng trong khối finally."""
    return Database()
