import aiohttp


class ClientSessionSingleton:
    _session = None

    @classmethod
    def get_session(cls):
        if cls._session is None or cls._session.closed:
            cls._session = aiohttp.ClientSession()
        return cls._session

    @classmethod
    async def close_session(cls):
        if cls._session is not None:
            await cls._session.close()
            cls._session = None


def session():
    return ClientSessionSingleton.get_session()


async def close_session():
    await ClientSessionSingleton.close_session()
