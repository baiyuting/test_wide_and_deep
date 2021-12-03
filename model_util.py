import torch
from torch import nn

"""
Wide & Deep Learning for Recommender Systems 论文实现
"""


class Wide(nn.Module):
    """
    wide 层， x 包含
    raw input features
    transformed features √

    依照 Figure 4 中描述， 仅仅只有一个one-hot向量 User Installed App & Impression App 进入 wide
    进入 wide x向量长度 o(10000)
    ranking 阶段 app数量 o(100)
    one hundred apps = [edge, firefox, google, visio, word]
    User Installed App=google [0, 0, 1, 0, 0]
    Impression App=word [0, 0, 0, 0, 1]
    User Installed App=google&Impression App=word
    [
    [0, 0, 0, 0, 0]
    [0, 0, 0, 0, 0]
    [0, 0, 0, 0, 1]
    [0, 0, 0, 0, 0]
    [0, 0, 0, 0, 0]
    ] 展开到一维
    """
    def __init__(self, wide_features_size):
        super(Wide, self).__init__()
        self.features_len = wide_features_size

    def forward(self, batch_wide_features):
        return batch_wide_features


class Deep(nn.Module):
    """
    deep 层
    continuous features=value 0-1之间的实数 计算 p(x<=value)=65% 如果按 n=10 等分算, 值在第 i=7 区间里面, normalized value = (i-1)/(n-1) = 2/3
    categorical features one hot向量 embedding 成为 长度为 32 的向量
    """
    def __init__(self, continuous_features_size, categorical_features_sizes):
        super(Deep, self).__init__()
        self.embeddings = []
        for size in categorical_features_sizes:
            self.embeddings.append(nn.Embedding(num_embeddings=size, embedding_dim=32))
        self.dense1 = nn.Linear(in_features=continuous_features_size+len(categorical_features_sizes)*32, out_features=1024)
        self.relu1 = nn.ReLU()
        self.dense2 = nn.Linear(in_features=1024, out_features=512)
        self.relu2 = nn.ReLU()
        self.dense3 = nn.Linear(in_features=512, out_features=256)
        self.relu3 = nn.ReLU()

    def forward(self, batch_continuous_features, batch_categorical_features):
        """

        :param batch_continuous_features: batch * len(continuous_features)
        :param batch_categorical_features:  batch * len(categorical_features)
        :return:
        """
        embedding_array = [embedding(categorical_feature) for (embedding, categorical_feature) in zip(self.embeddings, batch_categorical_features.t())]
        concatenated_embeddings = torch.cat([batch_continuous_features] + embedding_array, dim=-1)  # 将 输入连接
        return self.relu3(self.dense3(self.relu2(self.dense2(self.relu1(self.dense1(concatenated_embeddings)))))) # batch * 256


class WideAndDeep(nn.Module):
    """
    连接 wide 和 Deep

    sigmoid(batch_wide_features * W1 + b1 + batch_deep_features * W2 + b2)

    模型输入：
    batch_wide_features (b, len_wide)
    batch_continuous_features (b, len_continuous)
    batch_categorical_features (b, len_categorical)
    """
    def __init__(self, wide_features_size, continuous_features_size, categorical_features_sizes):
        super(WideAndDeep, self).__init__()
        self.wide = Wide(wide_features_size)
        self.wideLinear = nn.Linear(in_features=wide_features_size, out_features=1)
        self.deep = Deep(continuous_features_size, categorical_features_sizes)
        self.deepLinear = nn.Linear(in_features=256, out_features=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, batch_wide_features, batch_continuous_features, batch_categorical_features):
        return self.sigmoid(self.wideLinear(self.wide(batch_wide_features)) + self.deepLinear(self.deep(batch_continuous_features, batch_categorical_features)))


# batch_size = 64
# wide_features_size = 10000
# continuous_features_size = 300
# categorical_features_sizes = [vocabulary_size for vocabulary_size in range(10, 50, 1)]
# model = WideAndDeep(wide_features_size, continuous_features_size, categorical_features_sizes)
#
# import torch
# batch_wide_features = torch.ones((batch_size, wide_features_size))
# batch_continuous_features = torch.ones((batch_size, continuous_features_size))
# batch_categorical_features = torch.ones((batch_size, len(categorical_features_sizes)), dtype=torch.long)
# print(batch_wide_features.shape, batch_continuous_features.shape, batch_categorical_features.shape)
#
# output = model(batch_wide_features, batch_continuous_features, batch_categorical_features)
# print(output.shape)
#
# output.sum().backward()