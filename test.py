import tensorflow as tf
sess=tf.Session()

#特征数据
features = {
    'sex': [1, 2, 1, 1, 2],
    'department': ['sport', 'sport', 'drawing', 'gardening', 'travelling'],
}

#特征列
department = tf.feature_column.categorical_column_with_vocabulary_list('department', ['sport','drawing','gardening','travelling'], dtype=tf.string)
sex = tf.feature_column.categorical_column_with_identity('sex', num_buckets=2, default_value=0)
sex_department = tf.feature_column.crossed_column([department,sex], 16)
sex_department = tf.feature_column.indicator_column(sex_department)
#组合特征列
columns = [
    sex_department

]

#输入层（数据，特征列）
inputs = tf.feature_column.input_layer(features, columns)

#初始化并运行
init = tf.global_variables_initializer()
sess.run(tf.tables_initializer())
sess.run(init)

v=sess.run(inputs)
print(v)
