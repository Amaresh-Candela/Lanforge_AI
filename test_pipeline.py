from agent.execution_pipeline import ExecutionPipeline

pipeline = ExecutionPipeline(

    host="192.168.207.78"

)

execution = {

    "required": [

        "station",

        "upstream",

        "speed"

    ]

}

result = pipeline.prepare(

    "lf_dataplane_test.py",

    execution

)

print(result)