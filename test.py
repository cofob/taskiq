from asyncio import run, sleep
from collections.abc import Mapping
from logging import Logger
from typing import Any

from taskiq import Context, InMemoryBroker, TaskiqDepends


class TaskiqLogger(Logger):
    def __init__(self, context: Context = TaskiqDepends()) -> None:
        # context unfortunately does not provide task_name :(
        self.context = context
        super().__init__("task_log", 0)

    def _log(self, level: int, msg: object, args: Any, exc_info: Any = None, extra: Mapping[str, object] | None = None, stack_info: bool = False, stacklevel: int = 1) -> None:
        self.context.log += f"{msg}\n"
        return super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)


broker = InMemoryBroker()
broker.add_dependency_context({"logger": TaskiqLogger})


@broker.task
async def task(logger: TaskiqLogger = TaskiqDepends(), context: Context = TaskiqDepends()) -> None:
    logger.info("Hello World!")
    print(context.log)


async def main() -> None:
    await broker.startup()
    await task.kiq()
    await sleep(2)
    await broker.shutdown()


run(main())
