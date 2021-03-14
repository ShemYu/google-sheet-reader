import os, sys

sys.path.append(os.getcwd())

from gsheetreader.base import GoogleSheets


if __name__ == "__main__":
    sheet = GoogleSheets(
        "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
        "Class data",
        "A2:E"
    )
    sheet.load()