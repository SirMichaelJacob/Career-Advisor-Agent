from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.tools.google_search_agent_tool import GoogleSearchAgentTool
from google.adk.models.lite_llm import LiteLlm
import os

# credential setup
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")

# create 
def create_model():
    return LiteLlm(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=os.getenv("BASE_URL"),
    )


#agents

#web research agent
web_research_agent = GoogleSearchAgentTool(
    agent=
        Agent(
            name="web_research_agent",
            model=create_model(),
            description="An agent that performs web research using Google Search.",
            instruction="""
                You are a web research agent. Your task is to find accurate and relevant information from the web based on user queries.
                Use the Google Search tool to perform searches and gather information.
                Summarize your findings clearly and concisely.
            """,
            output_key="web_research_results",
        )
    )

#cv analyzer agent
cv_analyzer_agent = Agent(
    name="cv_analyzer_agent",
    model=create_model(),
    description="An agent that analyzes CVs and provides feedback.",
    instruction="""
        You are a CV analyzer agent. Your task is to review the text of the provided CV.
        You are to get all relevant information regarding the candidate's skills, experience, and qualifications.

        """,
    output_key="cv_analysis"    
)

#career_advisor agent
career_advisor_agent = Agent(
    name="career_advisor_agent",
    model=create_model(),
    description="""An agent that provides career advice based on CV analysis provided by "cv_analysis" and web research.""",
    instruction="""
        You are a career advisor agent. Your task is to provide concise and practical career advice based on the CV analysis and web research results provided.
        Use the information from "cv_analysis" and "web_research_results" to give tailored advice to the user regarding their career path, job opportunities, and skill development.
    """,
    output_key="career_advice",
    tools=[web_research_agent]
)

# certification advisor agent
certification_advisor_agent = Agent(
    name="certification_advisor_agent",
    model=create_model(),
    description="""An agent that suggests relevant certifications based on CV analysis provided by "cv_analysis" and web research.""",
    instruction="""
        You are a certification advisor agent. Your task is to suggest relevant certifications that can enhance the user's career prospects based on the CV analysis and web research results provided.
        Use the information from "cv_analysis" and "career_advice" to recommend certifications that align with the user's skills, experience, and career goals.
        List No more than 5 of the top certifications along with a brief explanation of why each is relevant and an estimated of the time it will take to complete.
    """,
    output_key="certification_suggestions",
    tools=[web_research_agent]
)

#parallel agent for career advice and certification suggestions
parallel_advisor_agent = ParallelAgent(
    name="parallel_advisor_agent",
    sub_agents=[
        career_advisor_agent,
        certification_advisor_agent
    ]
)

#summary agent
summary_agent = Agent(
    name="summary_agent",
    model=create_model(),
    description="An agent that summarizes the career advice and certification suggestions.",
    instruction="""
        You are a summary agent. Your task is to provide a concise summary of the career advice and certification suggestions provided by the previous agents.
        Combine the key points from "career_advice" and "certification_suggestions" into a clear and actionable summary for the user.
        Your response should be easy to understand and implement.
    """,
    output_key="final_summary"
)

#sequential root agent
sequential_root_agent = SequentialAgent(
    name="sequential_root_agent",
    description="A sequential agent that executes the tasks in a specific order.",
    
    sub_agents=[
        cv_analyzer_agent,
        parallel_advisor_agent,
        summary_agent
    ]
)
root_agent = SequentialAgent(
    name="root_agent",
    description="Career advice and certification pipeline",
    sub_agents=[
        sequential_root_agent
    ]
)

