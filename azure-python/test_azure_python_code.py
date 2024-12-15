import os  
from dotenv import load_dotenv
from pathlib import Path
from openai import AzureOpenAI   # type: ignore

env_path = Path(".env")
load_dotenv(dotenv_path=env_path)
endpoint = os.getenv("endpoint")
deployment = os.getenv("deployment")
search_endpoint = os.getenv("search_endpoint")
search_key = os.getenv("search_key")
subscription_key = os.getenv("subscription_key")
embedding_dependency_endpoint = os.getenv("embedding_dependency_endpoint")
embedding_dependency_key = os.getenv("embedding_dependency_key")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",  
)  
    
# Prepare the chat prompt  
# chat_prompt = [
# {
#     "role": "system",
#     "content": "Act as a conversational customer support agent who helps users and clients learn more about ISO New England and their data. Your responses should be informative, polite, and relevant. Make sure to reference all pdfs that you used to generate your response."
# },
# {
#     "role": "user",
#     "content": "What does ISO New England use their basic data collection on their facilities for?"
# },
# {
#     "role": "assistant",
#     "content": "ISO New England collects basic data on distributed energy resources (DER) facilities for many applications such as input to both long and short-term load forecasts, power system modeling, transmission planning and transmission service studies, operational studies, and the Energy Management System, among other uses [doc1]. Availability of this data leads to more accuracy in planning and operating the transmission system, as well as more efficient outcomes of these processes [doc1]."
# },
# {
#     "role": "user",
#     "content": "what were the three time sensitive needs for the boston 2033 na"
# },
# {
#     "role": "assistant",
#     "content": "I'm sorry, but I couldn't find any documents that contain information about \"the three time sensitive needs for the Boston 2033 NA.\" Could you please provide me with more context or clarify your question?"
# },
# {
#     "role": "user",
#     "content": "What is the Ancillary Service Scedule 2 business procedure applicable to?"
# },
# {
#     "role": "assistant",
#     "content": "According to [doc1], the Ancillary Service Schedule 2 business procedure is applicable to the ISO New England Inc., the New England Power Pool Participants Committee (NEPOOL PC), and other entities that may be involved in the provision, sale, purchase, and payment of certain ancillary services in the New England Control Area. This procedure describes the requirements for the ISO to procure and dispatch the applicable ancillary services, as well as the obligations of the market participants that provide and consume these services."
# },
# {
#     "role": "user",
#     "content": "What methods are used to perform the Demand Response Resource audits?"
# },
# {
#     "role": "assistant",
#     "content": "ISO New England uses two methods to perform Demand Response Resource (DRR) audits, namely Capability Audits (CCAs) and Claim 10/30. These audits can be modified or cancelled by the Designated Entity (DE) or Lead Market Participant (Lead MP) through their respective auditing software tools, CCAT and DRATT [doc2][doc4]. The ISO Control Room is notified by the Asset Registration and Auditing (ARA) Group or the DDE when there is a change to the audit plan or cancellation, and the DRR Auditing tool is populated every hour with the suggested resources to be audited and suggested start times [doc4]. The Operations Shift Supervisor verifies the DRR audit data has been updated and notifies the Control Room Operators of the scheduled audits and time frame for the audit [doc4]. Please refer to  and [doc4] for more information."
# },
# {
#     "role": "user",
#     "content": "How much is a late payment charge?"
# },
# {
#     "role": "assistant",
#     "content": "According to Section 4.1 of the ISO New England Billing Policy , if a Covered Entity is delinquent two or more times within any period of 12 months in paying on time its ISO Charges, such Covered Entity shall pay a late payment charge for its second failure to pay on time, and for each subsequent failure to pay on time within the same 12-month period. The amount of the late payment charge is equal to the greater of (i) two percent (2%) of the total amount of such late payment or (ii) $500.00. Please note that this information is specific to ISO Charges and Transmission Charges and may not apply to other types of payments."
# }
# ]

chat_prompt = [
{
    "role": "system",
    "content": "Act as a conversational customer support agent who helps users and clients learn more about ISO New England and their data. Your responses should be informative, polite, and relevant. Make sure to reference all pdfs that you used to generate your response."
},
{
    "role": "user",
    "content": "What methods are used to perform the Demand Response Resource audits?"
},
]

# Include speech result if speech is enabled  
speech_result = chat_prompt  

# Generate the completion  
completion = client.chat.completions.create(  
    model=deployment,  
    messages=speech_result,  
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,  
    stop=None,  
    stream=False  
)

extra_body={
    "data_sources": [{
        "type": "azure_search",
        "parameters": {
        "filter": None,
        "endpoint": f"{search_endpoint}",
        "index_name": "totalisonedata",
        "semantic_configuration": "azureml-default",
        "authentication": {
            "type": "api_key",
            "key": f"{search_key}"
        },
        "embedding_dependency": {
            "type": "endpoint",
            "endpoint": f"{embedding_dependency_endpoint}",
            "authentication": {
            "type": "api_key",
            "key": f"{embedding_dependency_key}"
            }
        },
        "query_type": "vector_simple_hybrid",
        "in_scope": True,
        "role_information": "Act as a conversational customer support agent who helps users and clients learn more about ISO New England and their data. Your responses should be informative, polite, and relevant. Make sure to reference all pdfs that you used to generate your response.",
        "strictness": 3,
        "top_n_documents": 5
        }
    }]
}

output = completion.choices[0].message.content
print(output)
