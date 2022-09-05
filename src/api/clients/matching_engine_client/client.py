from abc import ABC, abstractmethod
from google.cloud import aiplatform_v1
import grpc
from . import match_service_pb2
from . import match_service_pb2_grpc

REGION = "us-west1"
default_location = "projects/841506577075/locations/{}".format(REGION)
aiplatform_endpoint = "{}-aiplatform.googleapis.com".format(REGION)

class Client(ABC):
    @abstractmethod
    def get_match(self, match_request: dict) -> match_service_pb2.MatchResponse:
        pass

class MockMatchServiceClient(Client):
    def get_match(self, match_request: dict) -> match_service_pb2.MatchResponse:
        response = match_service_pb2.MatchResponse()
        
        neighbor1 = self.get_neighbor('7C48cUjCGx14K5b41e9vTD', 1)
        neighbor2 = self.get_neighbor('3x7gMvCsL1SS6THGwB55Pm', 2)
        neighbor3 = self.get_neighbor('7sLQGgXFs4LaGAaDErPwOl', 5)

        response.neighbor.extend([neighbor1, neighbor2, neighbor3])

        return response

    def get_neighbor(self, id: str, distance) -> object:
        neighbor = match_service_pb2.MatchResponse.Neighbor()
        neighbor.id = id
        neighbor.distance = distance

        return neighbor

class MatchServiceClient(Client):
    def __init__(self, location=default_location, index_endpoint_service_client=aiplatform_v1.IndexEndpointServiceClient(client_options=dict(api_endpoint=aiplatform_endpoint))) -> None:
        self.location=location
        self.index_endpoint_service_client = index_endpoint_service_client
        self.get_service_metadata()
    
    def get_match(self, match_request: dict) -> match_service_pb2.MatchResponse:
        request = match_service_pb2.MatchRequest()
        request.deployed_index_id = self.DEPLOYED_INDEX_ID
        
        query = match_request['query']
        if len(query) == 0:
            raise ValueError('Empty query provided.')
        
        for val in query:
            request.float_val.append(val)
        num_recos = match_request['num_recos']
        request.num_neighbors = num_recos
        
        response = self.stub.Match(request)
        
        return response
    
    def get_service_metadata(self) -> None:
        # TODO: gRPC server address is likely ephemeral. We should find out if it is possible to use a static ip for match service
        # so this logic isn't necessary.
        list_index_endpoints_request = aiplatform_v1.ListIndexEndpointsRequest(parent=self.location)
        pager_result = self.index_endpoint_service_client.list_index_endpoints(request=list_index_endpoints_request)
        spotifind_index_endpoint = pager_result.index_endpoints[0]
        deployed_index = spotifind_index_endpoint.deployed_indexes[0]
        
        self.DEPLOYED_INDEX_SERVER_IP = deployed_index.private_endpoints.match_grpc_address
        self.DEPLOYED_INDEX_ID = deployed_index.id
        self.channel = grpc.insecure_channel("{}:10000".format(self.DEPLOYED_INDEX_SERVER_IP))
        self.stub = match_service_pb2_grpc.MatchServiceStub(self.channel)
