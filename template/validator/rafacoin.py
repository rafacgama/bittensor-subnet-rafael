import os

RAFACOIN_LEDGER = 'rafacoin_ledger.txt'  # Example file path


def get_last_rafacoin_hash() -> str:
    """
    Retrieves the hash of the last recorded transaction in the RAFACOIN ledger.

    Returns:
        str: The hash of the last recorded transaction.
    """
    with open(RAFACOIN_LEDGER, 'ab+') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        return f.readline().decode().replace('\n', '')


def add_rafacoin_hash(line: str) -> None:
    """
    Appends a new line to the ledger file, typically used to add a new block hash.
    """
    with open(RAFACOIN_LEDGER, 'a+') as f:
        f.write(line + '\n')
