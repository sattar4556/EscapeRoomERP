from pathlib import Path

import shutil

from datetime import datetime


DATABASE_FILE = Path(

    "database.sqlite3"

)


BACKUP_DIR = Path(

    "backups"

)

BACKUP_DIR.mkdir(

    exist_ok=True,

)


def create_backup():

    if not DATABASE_FILE.exists():

        return None

    filename = datetime.now().strftime(

        "backup_%Y%m%d_%H%M%S.sqlite3"

    )

    destination = BACKUP_DIR / filename

    shutil.copy2(

        DATABASE_FILE,

        destination,

    )

    return destination


def list_backups():

    return sorted(

        BACKUP_DIR.glob(

            "*.sqlite3"

        ),

        reverse=True,

    )


def latest_backup():

    backups = list_backups()

    if backups:

        return backups[0]

    return None


def restore_backup(

    backup_file,

):

    backup_file = Path(

        backup_file,

    )

    if not backup_file.exists():

        return False

    shutil.copy2(

        backup_file,

        DATABASE_FILE,

    )

    return True


def delete_backup(

    backup_file,

):

    backup_file = Path(

        backup_file,

    )

    if backup_file.exists():

        backup_file.unlink()

        return True

    return False
