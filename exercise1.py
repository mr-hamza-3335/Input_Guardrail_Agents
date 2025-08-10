from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from connection import config
import asyncio
import rich
from pydantic import BaseModel

class ClassChangeOutput (BaseModel):
    response: str
    isTimingChange:bool

class_guard_agent=Agent(
    name= "class_guard_agent",
    instructions=""" Your task is to check the student's request.
        If the student wants to change their class timings, stop them gracefully.""",
    output_type=ClassChangeOutput,
)

@input_guardrail
async def class_timing_change_guardrail(ctx, agent, input):
    result= await Runner.run(class_guard_agent, input, run_config=config)
    rich.print(result.final_output)
    return GuardrailFunctionOutput(
        output_info= result.final_output.response,
        tripwire_triggered=result.final_output.isTimingChange,
    )

student_agent=Agent(
    name="student_agent",
    instructions="you are a student agent",
    input_guardrails=[class_timing_change_guardrail]
)

async def main():
    try:
        result=await Runner.run(student_agent, "I want to change my class timing", run_config=config)
        print("Student Request Processed")
    except InputGuardrailTripwireTriggered:
        print("Student request denied: Cannot change class timings")

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
