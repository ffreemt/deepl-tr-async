'''
order not preserved

copied from simple-proxy-pool

example use: async-headers.py:
    coros = iter([async_func()...])  # [generator or iterator]
    res = [*limited_as_completed(coros, limit=limit)]

https://artificialworlds.net/presentations/python-async/python-async.html x

https://www.artificialworlds.net/blog/2017/06/12/making-100-million-requests-with-python-aiohttp/
'''
# pyright: strict
from typing import Union, Generator, Iterator, List, Tuple, Any

from logzero import logger

import asyncio
from itertools import islice
from tqdm import tqdm

def limited_as_completed(coros: Union[Generator, Iterator], limit: float = 30, progress=True) -> Generator:
    ''' limited_as_completed '''
    try:
        loop = asyncio.get_event_loop()
    except Exception as exc:
        # logger.error('exc: %s, trying loop = asyncio.new_event_loop()' % exc)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # this shouldnt happen any more, but we leave it
    if loop.is_closed():  # pragma: no cover
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    futures = [
        asyncio.ensure_future(_)
        for _ in islice(coros, 0, limit)  # type: ignore
    ]

    if progress:
        pbar = tqdm(leave=True, total=len(futures))

    async def first_to_finish():
        while True:
            await asyncio.sleep(0)
            for fut in futures:
                if fut.done():
                    futures.remove(fut)
                    try:
                        newf = next(coros)
                        futures.append(
                            asyncio.ensure_future(newf))
                    except StopIteration as _:
                        pass
                    if progress:
                        pbar.update()
                    return fut.result()
    # while len(futures) > 0:
    while futures:
        # elm =
        # yield elm
        yield loop.run_until_complete(first_to_finish())
