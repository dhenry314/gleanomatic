import gleanomatic.Utils as Utils
from gleanomatic.configure import appConfig

params = {"sourceNamespace":"dhenry","setNamespace":"climatewalker","batchTag":"20181109"}

response = Utils.postRSData("http://resourcesync/capabilities",params)

print(response)

exit()

#log = { "LEVEL": "WARN", "MSG": "This is a new message" }

#content = Utils.postToLog(log)

#content = Utils.getContent("http://resourcesync/resource")

#print(content)

