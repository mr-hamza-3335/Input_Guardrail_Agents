from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
import rich
import asyncio
from connection import config
from pydantic import BaseModel

class TemperatureCheckOutput(BaseModel):
    response:str
    ittooCold:bool

father_agent= Agent(
    name="father_agent",
    instructions="""Your task is to check the outside temperature.
        If the temperature is below 26°C, set isTooCold=True and stop the child from running outside.
        Otherwise, set isTooCold=False.""",
    output_type=TemperatureCheckOutput,
)

@input_guardrail
async def Father_guardrail(ctx, agent, input):
    result= await Runner.run(father_agent, input, run_config=config)
    rich.print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.ittooCold,
    )

child_agent=Agent(
    name="child_agent",
    instructions="""You are a child asking to run outside.""",
    input_guardrails=[Father_guardrail],
)

async def main():
    try:
        result= await Runner.run(child_agent, "It is 24°C outside", run_config=config)
        print("Child allowed to run outside")

    except InputGuardrailTripwireTriggered:
        print("Child request denied: Too cold to run outside")

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
