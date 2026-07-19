from agent.entity_extractor import EntityExtractor

extractor = EntityExtractor()

text = """
Run dataplane test on 192.168.245.117
for 60 seconds
speed 1Gbps
"""

print(extractor.extract(text))