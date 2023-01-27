import argparse
import time
from google.cloud.aiplatform.matching_engine import MatchingEngineIndex, MatchingEngineIndexEndpoint

parser = argparse.ArgumentParser(description='Deploy Vertex AI ANN index')
parser.add_argument('--peering-range', type=str, help='VPC peering range for ANN index deployment')
parser.add_argument('--region', type=str, help='Region containing ANN index endpoint deployment')
parser.add_argument('--project-number', type=str, help='The GCP project number')
parser.add_argument('--environment', type=str, help='The target environment for deployment (dev, staging, etc.)')
parser.add_argument('--version', type=str, help='Semantic versioning for the index being deployed')
# https://cloud.google.com/vertex-ai/pricing#matchingengine
parser.add_argument('--machine-type', type=str, help='Machine type for deployment (e2-standard-2, e2-standard-16, e2-highmem-16, etc.)')
parser.add_argument('--min-replica', type=int, help='Minimum replica count for deployment')
parser.add_argument('--max-replica', type=int, help='Maximum replica count for deployment')
args = parser.parse_args()

PEERING_RANGE_NAME = args.peering_range
REGION = args.region
PROJECT_NUMBER = args.project_number
ENVIRONMENT = args.environment
VERSION = args.version
MACHINE_TYPE = args.machine_type
MIN_REPLICA = args.min_replica
MAX_REPLICA = args.max_replica

location = 'projects/{}/locations/{}'.format(PROJECT_NUMBER, REGION)
aiplatform_endpoint = '{}-aiplatform.googleapis.com'.format(REGION)
TIMEOUT_THRESHOLD = 60 # Timeout threshold before job failure

def get_ann_index_endpoint(filter):
    index_endpoints = MatchingEngineIndexEndpoint.list(
        filter=filter,
        project=PROJECT_NUMBER,
        location=REGION
    )
    if len(index_endpoints) == 0:
        return None
    
    return index_endpoints[0]

def get_ann_index(filter):
    indexes = MatchingEngineIndex.list(
        filter=filter,
        project=PROJECT_NUMBER,
        location=REGION
    )
    if len(indexes) == 0:
        return None

    return indexes[0]

def deploy_index(index, index_endpoint):
    deployed_index_id = 'spotifind_ann_index_deployed_{}_{}_{}'.format(VERSION, ENVIRONMENT, int(time.time()))
    index_endpoint.deploy_index(
        index=index,
        deployed_index_id=deployed_index_id,
        machine_type=MACHINE_TYPE,
        min_replica_count=MIN_REPLICA,
        max_replica_count=MAX_REPLICA,
        reserved_ip_ranges=[PEERING_RANGE_NAME],
        deployment_group=ENVIRONMENT
    )

    index_endpoint = None
    delta = 0
    while True:
        index_endpoint = get_ann_index_endpoint('deployedIndexes.id={}'.format(deployed_index_id))
        if index_endpoint:
            break
        
        if delta >= TIMEOUT_THRESHOLD:
            raise TimeoutError()
        
        delta += 1
        time.sleep(60)


spotifind_index = get_ann_index('labels.environment={} AND labels.version={}'.format(ENVIRONMENT, VERSION))
spotifind_index_endpoint = get_ann_index_endpoint('labels.environment={} AND labels.region={}'.format(ENVIRONMENT, REGION))

deployed_indexes = spotifind_index_endpoint.deployed_indexes

if not deployed_indexes:
    deploy_index(spotifind_index, spotifind_index_endpoint)
