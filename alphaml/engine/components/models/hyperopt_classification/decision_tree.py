import numpy as np

from hyperopt import hp

from alphaml.engine.components.models.base_model import BaseClassificationModel
from alphaml.utils.constants import *
from alphaml.utils.common import check_none


class DecisionTree(BaseClassificationModel):
    def __init__(self, criterion, max_features, max_depth_factor,
                 min_samples_split, min_samples_leaf, min_weight_fraction_leaf,
                 max_leaf_nodes, min_impurity_decrease, class_weight=None,
                 random_state=None):
        self.criterion = criterion
        self.max_features = max_features
        self.max_depth_factor = max_depth_factor
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_leaf_nodes = max_leaf_nodes
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.min_impurity_decrease = min_impurity_decrease
        self.random_state = random_state
        self.class_weight = class_weight
        self.estimator = None

    def fit(self, X, y, sample_weight=None):
        from sklearn.tree import DecisionTreeClassifier

        self.max_features = float(self.max_features)
        # Heuristic to set the tree depth
        if check_none(self.max_depth_factor):
            max_depth_factor = self.max_depth_factor = None
        else:
            num_features = X.shape[1]
            self.max_depth_factor = int(self.max_depth_factor)
            max_depth_factor = max(
                1,
                int(np.round(self.max_depth_factor * num_features, 0)))
        self.min_samples_split = int(self.min_samples_split)
        self.min_samples_leaf = int(self.min_samples_leaf)
        if check_none(self.max_leaf_nodes):
            self.max_leaf_nodes = None
        else:
            self.max_leaf_nodes = int(self.max_leaf_nodes)
        self.min_weight_fraction_leaf = float(self.min_weight_fraction_leaf)
        self.min_impurity_decrease = float(self.min_impurity_decrease)

        self.estimator = DecisionTreeClassifier(
            criterion=self.criterion,
            max_depth=max_depth_factor,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            max_leaf_nodes=self.max_leaf_nodes,
            min_weight_fraction_leaf=self.min_weight_fraction_leaf,
            min_impurity_decrease=self.min_impurity_decrease,
            class_weight=self.class_weight,
            random_state=self.random_state)
        self.estimator.fit(X, y, sample_weight=sample_weight)
        return self

    def predict(self, X):
        if self.estimator is None:
            raise NotImplementedError
        return self.estimator.predict(X)

    def predict_proba(self, X):
        if self.estimator is None:
            raise NotImplementedError()
        probas = self.estimator.predict_proba(X)
        return probas

    @staticmethod
    def get_properties(dataset_properties=None):
        return {'shortname': 'DT',
                'name': 'Decision Tree Classifier',
                'handles_regression': False,
                'handles_classification': True,
                'handles_multiclass': True,
                'handles_multilabel': True,
                'is_deterministic': True,
                'input': (DENSE, SPARSE, UNSIGNED_DATA),
                'output': (PREDICTIONS,)}

    @staticmethod
    def get_hyperparameter_search_space(dataset_properties=None):
        space = {'criterion': hp.choice('dt_criterion', ["gini", "entropy"]),
                 'max_depth_factor': hp.uniform('dt_max_depth_factor', 0, 2),
                 'min_samples_split': hp.randint('dt_min_samples_split', 19) + 2,
                 'min_samples_leaf': hp.randint('dt_min_samples_leaf', 20) + 1,
                 'min_weight_fraction_leaf': hp.choice('dt_min_weight_fraction_leaf', [0]),
                 'max_features': hp.choice('dt_max_features', [1.0]),
                 'max_leaf_nodes': hp.choice('dt_max_leaf_nodes', [None]),
                 'min_impurity_decrease': hp.choice('dt_min_impurity_decrease', [0.0])}

        init_trial = {'criterion': "gini",
                      'max_depth_factor': 0.5,
                      'min_samples_split': 2,
                      'min_samples_leaf': 1,
                      'min_weight_fraction_leaf': 0,
                      'max_features': 1,
                      'max_leaf_nodes': None,
                      'min_impurity_decrease': 0}
        return space