from agent.execution_engine import ExecutionEngine

engine = ExecutionEngine()

execution = {

    "required": [

        "station",

        "upstream",

        "speed"

    ]

}

parameters = {

    "station": "1.1.sta0001",

    "upstream": "1.1.eth1",

    "speed": "1Gbps"

}

print(engine.prepare(

    "lf_dataplane_test.py",

    execution,

    parameters

))