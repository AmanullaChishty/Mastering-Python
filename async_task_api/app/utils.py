#This module contains utility functions, including an asynchronous generator for streaming responses.

import asyncio
from typing import AsyncGenerator

async def generate_numbers()-> AsyncGenerator[str, None]:
    """Asynchronously generate numbers from 1 to 10 with delay."""
    for i in range(1,11):
        yield f"Number: {i}\n"
        await asyncio.sleep(1)