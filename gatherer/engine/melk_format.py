# FIELDS = ["ID", "SOURCE", "SECTION", "SOURCE_URL", "DATE", "TITLE", "FULL_TEXT", "TYPE"]
# one of the benefits of using a class here is that we can require certain fields as positional arguements,
# and give default/empty values of "" to non-required fields.

# Defining Melk format - see data dictionary for more info



melk_fields = ["ID", "SOURCE", "SECTION", "SOURCE_URL", "DATE", "TITLE", "FULL_TEXT", "TYPE"]

class MelkRow:
    def __init__(
        self, id, source, full_text, type, title="", section="", source_url="", date=""
    ):
        self.ID = id
        self.SECTION = section
        self.SOURCE = source
        self.SOURCE_URL = source_url
        self.DATE = date
        self.TITLE = title
        self.FULL_TEXT = full_text
        self.TYPE = type

    # use vars(name) to get dictionary of variables as key/value pairs
