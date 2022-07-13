import kfp
from kfp.v2 import compiler

pipeline_root_path='gs://spotifind-apiaip/vertex_ai_pipeline/'

@kfp.dsl.pipeline(
    name='spotifind-ann-index-pipeline',
    pipeline_root=pipeline_root_path)
def pipeline(peering_range: str, region: str, project_id: str):
    deploy_component = kfp.components.load_component_from_file('./components/pipeline_deploy.yaml')
    deploy_component_output = deploy_component(peering_range=peering_range, region=region, project_id=project_id)
    deploy_component_output.set_caching_options(enable_caching=False)

# Kubeflow pipeline compiler code borrowed from
# https://www.kubeflow.org/docs/components/pipelines/sdk/build-pipeline/#option-1-compile-and-then-upload-in-ui
compiler.Compiler().compile(
    pipeline_func=pipeline,
    package_path='pipeline.json'
)

