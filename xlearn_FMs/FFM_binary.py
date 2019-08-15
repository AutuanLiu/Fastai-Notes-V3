import xlearn as xl

# Training task
ffm_model = xl.create_ffm()    # Use field-aware factorization machine (ffm)
ffm_model.setTrain("data/small_train.txt")    # Set the path of training dataset
ffm_model.setValidate("data/small_test.txt")    # Set the path of validation dataset

# Parameters:
#  0. task: binary classification
#  1. learning rate: 0.03
#  2. regular lambda: 0.02
#  3. evaluation metric: accuracy
param = {'task': 'binary', 'lr': 0.03, 'lambda': 0.02, 'metric': 'acc', 'epoch': 50, 'stop_window': 5}

# Start to train
# The trained model will be stored in model.out
ffm_model.fit(param, 'out/model.out')

# Prediction task
ffm_model.setTest("data/small_test.txt")    # Set the path of test dataset
ffm_model.setSigmoid()    # Convert output to 0-1

# Start to predict
# The output result will be stored in output.txt
ffm_model.predict("out/model.out", "out/output.txt")
