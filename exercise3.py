from agents import Agent , Runner, input_guardrail, InputGuardrailTripwireTriggered, GuardrailFunctionOutput
import asyncio
import rich
from pydantic import BaseModel
from connection import config

class SchoolCheckOutput(BaseModel):
    response:str
    itOtherSchool:bool

gate_keeper_agent=Agent(
    name="gate_keeper_agent",
    instructions="""Your task is to check the student's school name.
        If the student is NOT from 'Green Valley School', set isOtherSchool=True and stop them from entering.
        If they are from 'Green Valley School', set isOtherSchool=False.""",
    output_type=SchoolCheckOutput
)

@input_guardrail
async def School_Guardrail(ctx, agent, input):
    result= await Runner.run(gate_keeper_agent, input, run_config=config)
    rich.print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.itOtherSchool,
    )

visitor_student=Agent(
    name="visitor_student",
    instructions="""You are a student trying to enter the school gate.""",
    input_guardrails=[School_Guardrail],
)

async def main():
    try:
        result= await Runner.run(visitor_student, "I am from Green Valley School", run_config=config)
        print("Student allowed to enter the school")

    except InputGuardrailTripwireTriggered:
        print("Student denied: Only Green Valley School students allowed")

if __name__== "__main__":
    import sys
    if sys.platform == 'win32':
        import asyncio.proactor_events
        orig_close = asyncio.proactor_events._ProactorBasePipeTransport.__del__

        def silent_del(self):
            try:
                orig_close(self)
            except RuntimeError as e:
                if "Event loop is closed" not in str(e):
                    raise
        asyncio.proactor_events._ProactorBasePipeTransport.__del__ = silent_del

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()