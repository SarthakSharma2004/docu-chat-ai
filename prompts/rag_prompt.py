from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder


class RagPrompt:
    """
    Stores all prompt templates for the RAG pipeline.
    """

    @staticmethod
    def get_rag_prompt():
        """
        Prompt used for answering questions based on retrieved context.
        """

        system_prompt = (
            "You are a highly reliable and factual AI assistant. "
            "You must answer ONLY using the information provided in the retrieved context.\n\n"
            "RULES:\n"
            "- If the answer is not found in the context, say: 'I don't have enough information from the documents to answer that.'\n"
            "- Be concise, accurate, and clear.\n"
            "- Do not hallucinate."
            "\n\n"
            "context: \n {context}"
        )


        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
