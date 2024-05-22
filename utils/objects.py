from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from pydantic import BaseModel, Field

class Expert(BaseModel):
    emoji: str = Field(..., description="Emoji of the agent's role.", max_length=1)
    name: str = Field(..., description="The agent's name, describing its function or role.")
    description: str = Field(..., description="The agent's complete behaviour description.")

N_QUERIES=3
class Queries(BaseModel):
    queries_list: list[str] = Field(..., description=f"A list of exactly {N_QUERIES} string queries.", min_items=N_QUERIES, max_items=N_QUERIES)


class SafePromptAsker:
    def __init__(self, prompt, parameters, pydantic_object, lang='english', model_version='gpt-4o'):
        self.prompt = prompt
        self.parameters = parameters
        self.pydantic_object = pydantic_object
        self.lang = lang
        self.llm = ChatOpenAI(model=model_version, temperature=1)
        self.parser = PydanticOutputParser(pydantic_object=pydantic_object)  # type: ignore
        self.prompt_template = PromptTemplate(
            template = prompt + "\nAnswer in this language: {lang}, and follow this format:\n{format_instructions}.",
            input_variables = parameters + ["lang"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        self.retry_prompt = PromptTemplate(
            template="Prompt:\n"\
                    "{prompt}\n"\
                    "Completion:\n"\
                    "{completion}\n"\
                    "Above, the Completion did not satisfy the constraints given in the Prompt.\n"\
                    "Details: {error}\n"\
                    "Please try again:", # TODO : add examples field
            input_variables=["prompt", "completion", "error"]
        )

    def ask(self, **kwargs):
        prompt_value = self.prompt_template.format_prompt(**kwargs, lang=self.lang)
        output = (self.llm | StrOutputParser()).invoke(prompt_value)
        try:
            return self.parser.parse(output)
        except OutputParserException as error:
            print("RETRY ATTEMPT")
            retry_llm = ChatOpenAI(model='gpt-4o')
            retry_chain = self.retry_prompt | retry_llm | self.parser
            return retry_chain.invoke({"prompt": prompt_value, "completion": output, "error": str(error)})
        
def simple_ask(prompt, parameters, model_version='gpt-4o', **kwargs):
    llm = ChatOpenAI(model=model_version)
    prompt_template = PromptTemplate(
            template = prompt,
            input_variables = parameters,
        )
    prompt_value = prompt_template.format_prompt(**kwargs)
    return (llm | StrOutputParser()).invoke(prompt_value)
