from typing import Optional

from click import Context, Argument

from cellphonedb.src.database.manager import DatabaseVersionManager


def choose_database(ctx: Context, argument: Argument, value: str) -> Optional[str]:
    return DatabaseVersionManager.find_database_for(value)