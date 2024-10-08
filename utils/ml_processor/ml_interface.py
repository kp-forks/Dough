from abc import ABC

from shared.constants import GPU_INFERENCE_ENABLED_KEY, ConfigManager

config_manager = ConfigManager()
gpu_enabled = config_manager.get(GPU_INFERENCE_ENABLED_KEY, False)

def get_ml_client():
    from utils.ml_processor.sai.api import APIProcessor
    from utils.ml_processor.gpu.gpu import GPUProcessor

    return APIProcessor() if not gpu_enabled else GPUProcessor()


class MachineLearningProcessor(ABC):
    def __init__(self):
        pass

    def predict_model_output_standardized(self, *args, **kwargs):
        pass

    def predict_model_output(self, *args, **kwargs):
        pass

    def upload_training_data(self, *args, **kwargs):
        pass

    # NOTE: implementation not neccessary as this functionality is removed from the app
    def dreambooth_training(self, *args, **kwargs):
        pass
