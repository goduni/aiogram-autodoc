from aiogram.dispatcher.filters import BoundFilter


class DescriptionFilter(BoundFilter):
    key = 'description'

    def __init__(self, description):
        self.description = description

    async def check(self, *args) -> bool:
        return True
