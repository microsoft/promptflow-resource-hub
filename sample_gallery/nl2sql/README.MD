# Natural Language to SQL Converter

NL2SQL (Natural Language to SQL) is a process that allows users to input queries in natural, human language and have them translated into SQL queries. This is particularly useful for users who may not be familiar with SQL syntax but need to retrieve data from a database.

In this sample, we show how to use Azure OpenAI GPT-4 model and PromptFlow to facilitate this translation. The implementation is loosely based on the [LangChain SQL Database Agent](https://python.langchain.com/docs/use_cases/sql/quickstart)

## Sample flows

| path                          | description                                                                                                                                        |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [development](./development/) | This flow demonstrates how to create a Natural Language to SQL Converter that takes natural languages as input and converts them into SQL queries. |
| [evaluation](./evaluation/)   | This evaluation flow demonstrates how to evaluate the performance of the Natural Language to SQL                                                   |
