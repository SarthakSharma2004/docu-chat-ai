from langchain.memory import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from core.config import get_settings

settings = get_settings()

class RedisMemoryManager:
    '''
    Redis-based chat history.
    Returns a RedisChatMessageHistory object per session_id.
    '''

    def __init__(self):
        self.redis_client = settings.REDIS_URL

    def get_history(self, session_id: str) -> BaseChatMessageHistory:
        return RedisChatMessageHistory(
            session_id = session_id,
            connection_string = self.redis_client
        )
    
memory_manager = RedisMemoryManager()

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    '''
    wrapper method for langchain's 'runnable with message history'
    '''
    return memory_manager.get_history(session_id)





