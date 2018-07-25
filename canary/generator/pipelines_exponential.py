from canary.generator.base_pipeline import DataTransformPipeline
from canary.generator.transformators.transformers_exponential import (
    AddWeekSeasonalityTransformer,
    AddExpNoiseTransformer,
    AddToSomeBucketSmoothTransformer,
    AddMoveTransformer,
    AddAnotherDistTransformer,
    AddTrendTransformer
)

anomaly_exponential_pipeline = DataTransformPipeline([
    AddMoveTransformer(),
    AddMoveTransformer(),
    AddMoveTransformer(),
    AddMoveTransformer(),
    AddAnotherDistTransformer(),
    AddAnotherDistTransformer(),
    AddAnotherDistTransformer(),
    AddAnotherDistTransformer(),
    AddToSomeBucketSmoothTransformer(),
    AddToSomeBucketSmoothTransformer(),
    AddToSomeBucketSmoothTransformer(),
    AddToSomeBucketSmoothTransformer(),
], kinds=['exponential', 'count'])

not_anomaly_exponential_pipeline = DataTransformPipeline([
    AddTrendTransformer(),
    AddWeekSeasonalityTransformer(),
    AddExpNoiseTransformer(),
], kinds=['exponential', 'count'])
