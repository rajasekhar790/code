
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
import os

@dataclass
class UserDetails:
    name: str
    age: int
os.environ["GEMINI_API_KEY"] = ""

agent = Agent('gemini-1.5-flash', deps_type=UserDetails)

@agent.system_prompt
def update_system_prompt(ctx: RunContext[UserDetails]):
    return f"""You are a helpful assistant. You always address the user by their name.
     Right now you are talking with Mr {ctx.deps.name} and he is {ctx.deps.age} years old."""

import datetime
@agent.tool
def get_bank_balance(ctx: RunContext[UserDetails]):
    """Use this tool to get user bank balance"""
    if ctx.deps.name == "Rajasekhar":
        return "John's current bank balance is $100000."
    elif ctx.deps.name == "Abi":
        return "Abi's current bank balance is $200000."
    elif ctx.deps.name == "Punnarao":
        return "Mani's current bank balance is $300000."
    else:
        return "Please check the user name"

@agent.tool_plain
def get_current_date():
    return f"Today is {datetime.now()}"



deps = UserDetails(name="Punnarao", age=55)
result = await agent.run("What is my current balance", deps=deps)
result.data


