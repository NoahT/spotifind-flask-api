import argparse
import time
from google.cloud import aiplatform_v1
from google.cloud import logging_v2

parser = argparse.ArgumentParser(description='Deploy Vertex AI ANN index')
parser.add_argument('--peering-range', type=str, help='VPC peering range for ANN index deployment')
parser.add_argument('--region', type=str, help='Region containing ANN index endpoint deployment')
parser.add_argument('--project-id', type=str, help='The GCP project ID')
args = parser.parse_args()

PEERING_RANGE_NAME = args.peering_range
REGION = args.region
PROJECT_ID = args.project_id
logging_client = logging_v2.Client()
logger = logging_client.logger('ann-index-deploy')

location = "projects/{}/locations/{}".format(PROJECT_ID, REGION)
aiplatform_endpoint = "{}-aiplatform.googleapis.com".format(REGION)

index_endpoint_service_client = aiplatform_v1.IndexEndpointServiceClient(client_options=dict(api_endpoint=aiplatform_endpoint))
index_service_client = aiplatform_v1.IndexServiceClient(client_options=dict(api_endpoint=aiplatform_endpoint))


def get_ann_index_endpoint():
    list_index_endpoints_request = aiplatform_v1.ListIndexEndpointsRequest(parent=location)
    pager_result = index_endpoint_service_client.list_index_endpoints(request=list_index_endpoints_request)

    index_endpoint = pager_result.index_endpoints[0]
    return index_endpoint

def get_ann_index():
    list_indexes_request = aiplatform_v1.ListIndexesRequest(parent=location)
    indexes_pager_result = index_service_client.list_indexes(request=list_indexes_request)
    
    index = indexes_pager_result.indexes[0]
    return index

def deploy_index(index, index_endpoint):
    deployed_index = aiplatform_v1.DeployedIndex({
        "id": "{}-deployed".format(index.display_name),
        "index": index.name,
        "display_name": "{}-deployed".format(index.display_name),
        "reserved_ip_ranges": [
            PEERING_RANGE_NAME
        ]
    })
    
    deployed_index_request = aiplatform_v1.DeployIndexRequest(index_endpoint=index_endpoint.name, deployed_index=deployed_index)
    
    deployed_index = index_endpoint_service_client.deploy_index(request=deployed_index_request)

    while True:
        if deployed_index.done():
            break
        logger.log('Deploying index...', severity='INFO')
        time.sleep(60)
    
    return deploy_index


spotifind_index = get_ann_index()
spotifind_index_endpoint = get_ann_index_endpoint()

deployed_indexes = spotifind_index.deployed_indexes

if not deployed_indexes:
    deployed_index = deploy_index(spotifind_index, spotifind_index_endpoint)
    logger.log(deploy_index, severity='INFO')
