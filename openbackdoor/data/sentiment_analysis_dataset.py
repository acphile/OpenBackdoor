
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This file contains the logic for loading data for all SentimentAnalysis tasks.
"""

import os
import json, csv
import random
from abc import ABC, abstractmethod
from collections import defaultdict, Counter
from typing import List, Dict, Callable
from .data_processor import DataProcessor


class ImdbProcessor(DataProcessor):
    """
    `IMDB <https://ai.stanford.edu/~ang/papers/acl11-WordVectorsSentimentAnalysis.pdf>`_ is a Movie Review Sentiment Classification dataset.

    we use dataset provided by `LOTClass <https://github.com/yumeng5/LOTClass>`_
    """

    def __init__(self):
        super().__init__()
        self.labels = ["negative", "positive"]
        self.path = "./datasets/SentimentAnalysis/imdb"

    def get_examples(self, data_dir, split):
        examples = []
        if data_dir is None:
            data_dir = self.path
        label_file = open(os.path.join(data_dir, "{}_labels.txt".format(split)), 'r') 
        labels = [int(x.strip()) for x in label_file.readlines()]
        with open(os.path.join(data_dir, '{}.txt'.format(split)),'r') as fin:
            for idx, line in enumerate(fin):
                text_a = line.strip()
                example = (text_a, int(labels[idx]))
                examples.append(example)
        return examples

    @staticmethod
    def get_test_labels_only(data_dir, dirname):
        label_file  = open(os.path.join(data_dir,dirname,"{}_labels.txt".format('test')),'r') 
        labels  = [int(x.strip()) for x in label_file.readlines()]
        return labels
   

class AmazonProcessor(DataProcessor):
    """
    `Amazon <https://cs.stanford.edu/people/jure/pubs/reviews-recsys13.pdf>`_ is a Product Review Sentiment Classification dataset.

    we use dataset provided by `LOTClass <https://github.com/yumeng5/LOTClass>`_
    """

    def __init__(self):
        raise NotImplementedError
        super().__init__()
        self.labels = ["bad", "good"]
        self.path = "./datasets/SentimentAnalysis/amazon"

    def get_examples(self, data_dir, split):
        examples = []
        if data_dir is None:
            data_dir = self.path
        label_file = open(os.path.join(data_dir, "{}_labels.txt".format(split)), 'r') 
        labels = [int(x.strip()) for x in label_file.readlines()]
        if split == "test": 
            logger.info("Sample a mid-size test set for effeciecy, use sampled_test_idx.txt")
            with open(os.path.join(self.args.data_dir,self.dirname,"sampled_test_idx.txt"),'r') as sampleidxfile:
                sampled_idx = sampleidxfile.readline()
                sampled_idx = sampled_idx.split()
                sampled_idx = set([int(x) for x in sampled_idx])

        with open(os.path.join(data_dir,'{}.txt'.format(split)),'r') as fin:
            for idx, line in enumerate(fin):
                if split=='test':
                    if idx not in sampled_idx:
                        continue
                text_a = line.strip()
                example = InputExample(guid=str(idx), text_a=text_a, label=int(labels[idx]))
                examples.append(example)
        return examples


class SST2Processor(DataProcessor):
    """
    #TODO test needed
    """

    def __init__(self):
        raise NotImplementedError
        super().__init__()
        self.labels = ["negative", "positive"]
        self.path = "./datasets/SentimentAnalysis/sst2"

    def get_examples(self, data_dir, split):
        examples = []
        if data_dir is None:
            data_dir = self.path
        path = os.path.join(data_dir,"{}.tsv".format(split))
        with open(path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for idx, example_json in enumerate(reader):
                text_a = example_json['sentence'].strip()
                example = InputExample(guid=str(idx), text_a=text_a, label=int(example_json['label']))
                examples.append(example)
        return examples

PROCESSORS = {
    "amazon" : AmazonProcessor,
    "imdb": ImdbProcessor,
    "sst-2": SST2Processor,
}
