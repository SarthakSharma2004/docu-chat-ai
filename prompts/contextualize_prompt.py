from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

class ContextualizePrompt:
    """
    Prompt used for contextualizing questions.
    """

    @staticmethod
    def get_contextualize_prompt():

        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question which may reference "
            "context from the chat history, reformulate the question into a standalone query that "
            "can be understood without the chat history. "
            "Do NOT answer the question. "
            "If no rewrite is needed, return the question as-is."
        )

        return ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])
