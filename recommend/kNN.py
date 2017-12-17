from numpy import *
from recommend.util import session
from douban.douban.models import Douban

def get_datasets(CORPUS_TYPE_SETTINGS):
    start_list = [0]*len(CORPUS_TYPE_SETTINGS)
    type_list = list(CORPUS_TYPE_SETTINGS.keys())
    query = session.query(Douban)
    query_obj_list = query.all()
    corpus_list = []
    labels = []
    for query_obj in query_obj_list:
        array_list = start_list.copy()
        types = query_obj.types
        for tmp_type in types.split("|"):
            type_index = type_list.index(tmp_type)
            # array_list[type_index] = 1
            array_list[type_index] = CORPUS_TYPE_SETTINGS.get(tmp_type)
        if len(types.split("|")) != len(array_list) - array_list.count(0):
            print("----error----")
        corpus_list.append(array_list)
        labels.append(query_obj.movie_type)
    return array(corpus_list), labels

def get_type_datasets(CORPUS_TYPE_SETTINGS, movie_type):
    start_list = [0]*len(CORPUS_TYPE_SETTINGS)
    type_list = list(CORPUS_TYPE_SETTINGS.keys())
    query = session.query(Douban)
    query_obj_list = query.filter_by(movie_type=movie_type).all()
    corpus_list = []
    labels = []
    for query_obj in query_obj_list:
        array_list = start_list.copy()
        types = query_obj.types
        for tmp_type in types.split("|"):
            type_index = type_list.index(tmp_type)
            # array_list[type_index] = 1
            array_list[type_index] = CORPUS_TYPE_SETTINGS.get(tmp_type)
        if len(types.split("|")) != len(array_list) - array_list.count(0):
            print("----error----")
        corpus_list.append(array_list)
        labels.append(query_obj.id)
    return array(corpus_list), labels

def classify(input, corpus_list, labels, k):
    data_size = corpus_list.shape[0]
    # 欧氏距离
    diff = tile(input, (data_size, 1)) - corpus_list
    sq_diff = diff ** 2
    square_dist = sum(sq_diff, axis=1)
    dist = square_dist ** 0.5

    sorted_dist_index = argsort(dist)

    class_count = {}
    for i in range(k):
        vote_label = labels[sorted_dist_index[i]]
        class_count[vote_label] = class_count.get(vote_label, 0) + 1

    max_count = 0
    for key, value in class_count.items():
        if value > max_count:
            max_count = value
            classes = key

    return classes
