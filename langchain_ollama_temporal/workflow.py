from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import TranslateParams, translate_phrase


@workflow.defn
class LangChainWorkflow:
    @workflow.run
    async def run(self, phrase: str, language: str) -> dict:
        response = await workflow.execute_activity(
            translate_phrase,
            args=[phrase, language],
            schedule_to_close_timeout=timedelta(seconds=300),
        )

        print(f"RESPONSE: {response}")
        return response
