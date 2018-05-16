#Importing the AWS SDK
import boto3

session = boto3.Session(profile_name='sandbox')
#Creading workspace client object 
client = session.client("workspaces")

#Description of all running workspace
response = client.describe_workspaces()
def lambda_handler(event, context):
    #filter tag: <<start>> and <<stopped>> EC2 instances
    filters = [{
                'Name': 'tag:start', 
                'Values': ['true']
            },
            {
                'Name': 'instance-state-name', 
                'Values': ['stopped']
            }
        ]

    #create parameter for instance ids of filtered EC2 instances
    #filteredWorkspace = [instance.id for instance in ec2.instances.filter(Filters=filters)]

    #Looping over all workspaces in response
    for workspace in response["Workspaces"]:

        #Some temporary variables for each workspace
        state = str(workspace["State"])
        username = str(workspace["UserName"])
        workspaceId = str(workspace["WorkspaceId"])
        runningMode = workspace["WorkspaceProperties"]["RunningMode"]
        
        response = client.describe_tags(
            ResourceId=workspaceId
        )
        print (response)
        raise

        #Starting turned off workspaces
        if state=="STOPPED":

            #Starting workspace with the id stored in varibale workspaceId
            client.start_workspaces(StartWorkspaceRequests = [
                {
                    "WorkspaceId": workspaceId
                }
                ])
        #Checking if the running mode is Auto Stop
        if runningMode=="AUTO_STOP":
            #Making the auto stop timeout 180 minutes
            client.modify_workspace_properties(
                WorkspaceId = workspaceId,
                WorkspaceProperties = {
                    'RunningModeAutoStopTimeoutInMinutes' : 180
                }
            )
            
