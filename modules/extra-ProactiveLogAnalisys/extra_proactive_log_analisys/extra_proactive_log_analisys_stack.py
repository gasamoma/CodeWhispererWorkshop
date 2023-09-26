from aws_cdk import (
    # Duration,
    Stack,
    aws_glue_alpha as glue,
    # aws_sqs as sqs,
)
from os import path
from constructs import Construct

class ExtraProactiveLogAnalisysStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        glue.Job(self, "EnableSparkUI",
            job_name="EtlJobWithSparkUIPrefix",
            spark_ui=glue.SparkUIProps(
                enabled=True
            ),
            executable=glue.JobExecutable.python_etl(
                glue_version=glue.GlueVersion.V3_0,
                python_version=glue.PythonVersion.THREE,
                # script = app/glue/etl.py
                script=glue.Code.from_asset(path.join(path.dirname(__file__), "../app/glue/etl.py"))
            
        ))
