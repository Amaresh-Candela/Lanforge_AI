from agent.command_builder import CommandBuilder

builder = CommandBuilder()

parameters = {

    "station": "1.1.sta0001",

    "upstream": "1.1.eth1",

    "speed": "1Gbps",

    "duration": 60

}

command = builder.build(

    "lf_dataplane_test.py",

    parameters

)

print(command)