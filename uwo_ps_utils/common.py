"""Common util functions
"""
import os

import tensorflow as tf
from tensorflow.saved_model import tag_constants

def get_image_paths(directory, ext):
    """Get full paths with given extenstion

    Arguments:
        directory (str): Image directory path
        ext (str): Extenstion filter to add to list

    Return:
        full paths (list)
    """
    image_files = []
    for (dirpath, _, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(ext):
                image_files.append(os.sep.join([dirpath, filename]))
    return image_files

def estimate(model_dir, raw_bytes):
    """Estimate image data using given learned tensorflow model

    Do not keep tensorflow session to prevent the memory from wasting
    Instead of that, make a session for each call.

    Arguments:
        model_dir (str): Directory which is saved model
        raw_bytes (bytes): bytes data of image

        Return : index of label
    """
    tf.reset_default_graph()
    graph = tf.Graph()
    with graph.as_default():
        with tf.Session(graph=graph) as sess:
            tf.saved_model.loader.load(sess, [tag_constants.SERVING], model_dir, )

            X = graph.get_tensor_by_name("X:0")
            keep_prob = graph.get_tensor_by_name("keep_prob:0")
            model = graph.get_tensor_by_name("model:0")

            x_data = [[float(x) for x in raw_bytes]]
            logits = tf.argmax(model, 1)

            return sess.run(logits, feed_dict={X: x_data, keep_prob: 1.0})[0]