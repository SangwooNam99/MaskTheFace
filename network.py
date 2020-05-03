import tensorflow as tf
import numpy as np
# from network.loss_functions import huber_loss


class VGGNet16(object):
    def __init__(self, input, num_classes):
        self.input = input
        # Block 1
        self.conv1 = self.conv(self.input, k=3, out=64, s=1, p="SAME")
        self.conv2 = self.conv(self.conv1, k=3, out=64, s=1, p="SAME")
        self.mp1 = tf.nn.max_pool(
            self.conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="VALID"
        )
        # Block 2
        self.conv3 = self.conv(self.mp1, k=3, out=128, s=1, p="SAME")
        self.conv4 = self.conv(self.conv3, k=3, out=128, s=1, p="SAME")
        self.mp2 = tf.nn.max_pool(
            self.conv4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="VALID"
        )
        # Block 3
        self.conv5 = self.conv(self.mp2, k=3, out=256, s=1, p="SAME")
        self.conv6 = self.conv(self.conv5, k=3, out=256, s=1, p="SAME")
        self.conv7 = self.conv(self.conv6, k=3, out=256, s=1, p="SAME")
        self.mp3 = tf.nn.max_pool(
            self.conv7, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="VALID"
        )
        # Block 4
        self.conv8 = self.conv(self.mp3, k=3, out=512, s=1, p="SAME")
        self.conv9 = self.conv(self.conv8, k=3, out=512, s=1, p="SAME")
        self.conv10 = self.conv(self.conv9, k=3, out=512, s=1, p="SAME")
        self.mp4 = tf.nn.max_pool(
            self.conv10, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="VALID"
        )
        # Block 5
        self.conv11 = self.conv(self.mp4, k=3, out=512, s=1, p="SAME")
        self.conv12 = self.conv(self.conv11, k=3, out=512, s=1, p="SAME")
        self.conv13 = self.conv(self.conv12, k=3, out=512, s=1, p="SAME")
        self.mp5 = tf.nn.max_pool(
            self.conv13, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="VALID"
        )
        # Block6 - FC
        self.flat = tf.contrib.layers.flatten(self.mp5)
        self.fc14 = self.FullyConnected(
            self.flat, units_in=25088, units_out=4096, act="relu"
        )
        self.fc15 = self.FullyConnected(
            self.fc14, units_in=4096, units_out=4096, act="relu"
        )
        self.fc16 = self.FullyConnected(
            self.fc15, units_in=4096, units_out=num_classes, act="relu"
        )

        self.prediction_probs = tf.nn.softmax(self.fc16)
        self.output = self.fc16

    def conv(self, input, k, out, s, p, trainable=True):

        W = tf.Variable(
            tf.truncated_normal(shape=(k, k, int(input.shape[3]), out), stddev=0.05),
            trainable=trainable,
        )
        b = tf.Variable(
            tf.truncated_normal(shape=[out], stddev=0.05), trainable=trainable
        )

        conv_kernel_1 = tf.nn.conv2d(input, W, [1, s, s, 1], padding=p)
        bias_layer_1 = tf.nn.bias_add(conv_kernel_1, tf.Variable(b, trainable))

        return tf.nn.relu(bias_layer_1)

    def FullyConnected(self, input, units_in, units_out, act, trainable=True):
        W = tf.Variable(
            tf.truncated_normal(shape=(units_in, units_out), stddev=0.05),
            trainable=trainable,
        )
        b = tf.Variable(
            tf.truncated_normal(shape=[units_out], stddev=0.05), trainable=trainable
        )

        if act == "relu":
            return tf.nn.relu_layer(input, W, b)
        elif act == "linear":
            return tf.nn.xw_plus_b(input, W, b)
        else:
            assert 1 == 0