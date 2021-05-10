from typing import List, Union, Optional, Iterable

from aiogram import Dispatcher
from aiogram.dispatcher.handler import Handler, FilterObj
from aiogram.dispatcher.filters.builtin import Command

from .filters import DescriptionFilter
from .types import AutoDocResult, CommandResult


class AutoDoc:
    dp: Dispatcher
    exclude_empty: bool
    support_multiple_command: bool
    support_doc_strings: bool
    disable_prefixes: bool

    def __init__(self,
                 dp: Dispatcher,
                 exclude_empty: bool = True,
                 support_doc_strings: bool = True,
                 disable_prefixes: bool = False
                 ):
        self.dp = dp
        self.exclude_empty = exclude_empty
        self.support_doc_strings = support_doc_strings
        self.disable_prefixes = disable_prefixes

        self._result = None

    @property
    def results(self) -> AutoDocResult:
        if not self._result:
            raise ValueError('results must be parsed')
        return self._result

    def __parse_commands_with_prefixes(self, command: Command) -> List[str]:
        commands_with_prefixes = []
        for cmd in command.commands:
            if not self.disable_prefixes:
                for prefix in command.prefixes:
                    commands_with_prefixes.append(f'{prefix}{cmd}')
        return commands_with_prefixes

    def __parse_commands_from_handler(self, filters: Iterable[FilterObj]) -> List[Union[str, List[str]]]:
        result = []
        for filter_obj in filters:
            f = filter_obj.filter
            if isinstance(f, Command):
                commands = self.__parse_commands_with_prefixes(f)
                for command in commands:
                    result.append(command)
        return result

    def __parse_description_from_handler(self, handler: Handler.HandlerObj) -> Optional[str]:
        doc_string = handler.handler.__doc__
        if not self.support_doc_strings or not doc_string:
            for filter_obj in handler.filters:
                if isinstance(filter_obj.filter, DescriptionFilter):
                    return filter_obj.filter.description
        return doc_string

    def __parse_message_handler(self, handler: Handler.HandlerObj) -> Union[CommandResult, List[CommandResult]]:
        result = None
        filters = handler.filters
        if filters:
            commands = self.__parse_commands_from_handler(filters)
            if commands:
                description = self.__parse_description_from_handler(handler)
                result = CommandResult(command=commands, description=description)
        return result

    def __parse_message_handlers(self) -> List[Union[CommandResult, List[CommandResult]]]:
        results = []
        for handler in self.dp.message_handlers.handlers:
            description = self.__parse_description_from_handler(handler)
            if description:
                res = self.__parse_handler(handler, handler_type='message')
                if res:
                    results.append(res)
            else:
                if not self.exclude_empty:
                    res = self.__parse_handler(handler, handler_type='message')
                    if res:
                        results.append(res)
        return results

    def __parse_handler(self, handler: Handler.HandlerObj, handler_type: str) -> Union[
        CommandResult, List[CommandResult]
    ]:
        results = []
        if handler_type == 'message':
            results = self.__parse_message_handler(handler)
        return results

    def parse(self):
        self._result = self.__parse_message_handlers()

    def to_dict(self) -> dict:
        result = dict()
        for res in self._result:
            key = res.command
            if isinstance(key, list):
                key = ', '.join(res.command)
            result[key] = res.description
        return result
