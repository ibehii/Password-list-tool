#  GitHub: https://github.com/ibehii
#  Telegram: https://T.me/BZHNAM
#  e-mail: Behii@tutanota.com
#  ____________________________________________

# ======== # Import Part # ======== #
from pathlib import Path
import sqlite3

current_path: Path = Path(__file__).parent.resolve()

def initializer() -> None:
    if not (database_path := current_path / "db" / ".passwords.db").exists():
        if not database_path.parent.exists():
            database_path.parent.mkdir()
        database_path.touch()
        connection: sqlite3.Connection = sqlite3.connect(database_path)
        cursor: sqlite3.Cursor = connection.cursor()
        
        cursor.execute("""CREATE TABLE password ( password TEXT,
            date TEXT,
            reminder TEXT)""")
        connection.commit()
        connection.close()
        
    