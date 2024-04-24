from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = GoogleGenerativeAI(model="models/gemini-1.0-pro-latest", safety_settings={
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}, )

template = """You are expert doctor with specialization in  {specialization}, an patient is coming with out these 
symptoms {symptoms}, pre-diagnose the patient and provide the list of possible diseases and their symptoms.
"""

prompt = PromptTemplate(
    input_variables=["specialization", "symptoms"],
    template=template
)

chain1 = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="solutions"
)

template = """
Step 2:

For each of the three proposed solutions, evaluate their potential. Consider their pros and cons, initial effort needed, implementation difficulty, potential challenges, and the expected outcomes. Assign a probability of success and a confidence level to each option based on these factors

{solutions}

A:"""

prompt = PromptTemplate(
    input_variables=["solutions"],
    template=template
)

chain2 = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="review"
)

template = """
Step 3:

For each solution, deepen the thought process. Generate potential scenarios, strategies for implementation, any necessary partnerships or resources, and how potential obstacles might be overcome. Also, consider any potential unexpected outcomes and how they might be handled.

{review}

A:"""

prompt = PromptTemplate(
    input_variables=["review"],
    template=template
)

chain3 = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="deepen_thought_process"
)

template = """
Step 4:

Based on the evaluations and scenarios, rank the solutions in order of promise. Provide a justification for each ranking and offer any final thoughts or considerations for each solution
{deepen_thought_process}

A:"""

prompt = PromptTemplate(
    input_variables=["deepen_thought_process"],
    template=template
)

chain4 = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="ranked_solutions"
)


from langchain.chains import SequentialChain

overall_chain = SequentialChain(
    chains=[chain1, chain2, chain3, chain4],
    input_variables=["input", "perfect_factors"],
    output_variables=["ranked_solutions"],
    verbose=True
)

print(overall_chain({"input":"human colonization of Mars", "perfect_factors":"The distance between Earth and Mars is "
                                                                             "very large, making regular resupply "
                                                                             "difficult"}))