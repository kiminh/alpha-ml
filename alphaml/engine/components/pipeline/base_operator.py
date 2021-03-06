import abc
import typing
from alphaml.engine.components.data_manager import DataManager

DATA_PERPROCESSING = 0
FEATURE_GENERATION = 1
FEATURE_SELECTION = 2


class Operator(object, metaclass=abc.ABCMeta):
    def __init__(self, type, operator_name, params=None):
        self.type = type  # type: "data_preprocessing", "feature_generation","feature_selection"
        self.operator_name = operator_name  # id: dp_minmaxnormalizer, fg_polynomial, fs_lasso.
        self.params = params
        self.id = None
        self.origins = None

    @abc.abstractmethod
    def operate(self, dm_list: typing.List, phase='train'):
        # After this operator, gc the result of operator.
        raise NotImplementedError()

    def check_phase(self, phase):
        if phase not in ['train', 'test']:
            raise ValueError("Invalid phase. Expected 'train' or 'test'!")


class EmptyOperator(Operator):
    def __init__(self):
        super().__init__('Empty', 'empty_operatpr')

    def operate(self, dm_list: typing.List[DataManager]):
        self.result_dm = dm_list[-1]
