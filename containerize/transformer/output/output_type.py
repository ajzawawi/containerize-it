from enum import Enum

class OutputType(str, Enum):
    helm = "helm"
    helm_subcharts = "helm-subcharts"
    raw = "raw"