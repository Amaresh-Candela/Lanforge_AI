from agent.parameter_collector import ParameterCollector

execution = {

    "script": "lf_dataplane_test.py",

    "required": [

        "station",

        "upstream",

        "speed"

    ]

}

values = {

    "station": "1.1.sta0001",

    "upstream": "1.1.eth1"

}

collector = ParameterCollector()

result = collector.collect(

    execution,

    values

)

print(result)