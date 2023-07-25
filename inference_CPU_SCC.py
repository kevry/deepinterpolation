import os
from datetime import datetime
from scipy.io import loadmat


def inference(path,tag,sess,model_path,jobdir,dp_path):

    import scipy.io as sio
    from deepinterpolation.deepinterpolation.generic import JsonSaver, ClassLoader

    # startTime=datetime.now()
    generator_param = {}
    inferrence_param = {}

    # We are reusing the data generator for training here.
    generator_param["type"] = "generator"
    generator_param["name"] = "SingleTifGenerator"
    generator_param["pre_post_frame"] = 30
    generator_param["pre_post_omission"] = 0
    generator_param["steps_per_epoch"] = -1  # No steps necessary for inference as epochs are not relevant. -1 deactivate it.

    generator_param["train_path"] = path
    generator_param["batch_size"] = 5
    generator_param["start_frame"] = 0
    generator_param["end_frame"] = -1  # -1 to go until the end.
    generator_param[
        "randomize"
    ] = 0  # This is important to keep the order and avoid the randomization used during training

    inferrence_param["type"] = "inferrence"
    inferrence_param["name"] = "core_inferrence"

    # Replace this path to where you stored your model
    inferrence_param["model_path"] = model_path
    
    dp_mat_path = dp_path

    inferrence_param["mat_file"] = dp_mat_path

    jobdir = jobdir #your home directory

    try:
        os.mkdir(jobdir)
    except:
        print("folder already exists")

    path_generator = os.path.join(jobdir, "generator_" + sess + tag + ".json")
    json_obj = JsonSaver(generator_param)
    json_obj.save_json(path_generator)

    path_infer = os.path.join(jobdir, "inferrence_" + sess + tag + ".json")
    json_obj = JsonSaver(inferrence_param)
    json_obj.save_json(path_infer)

    generator_obj = ClassLoader(path_generator)
    data_generator = generator_obj.find_and_build()(path_generator)


    inferrence_obj = ClassLoader(path_infer)
    inferrence_class = inferrence_obj.find_and_build()(path_infer, data_generator)

    # Except this to be slow on a laptop without GPU. Inference needs parallelization to be effective.

    out = inferrence_class.run()
    framedata=data_generator.list_samples[0:len(data_generator)*5]
    matdata = np.ascontiguousarray(out)
    matdata = matdata[:,data_generator.a:512-data_generator.a,data_generator.b:512-data_generator.b]
    matsavedata = np.swapaxes(matdata, 0, 2)
    matsavedata = np.swapaxes(matsavedata, 0, 1)
    sio.savemat(dp_mat_path, mdict={'inference_data':matsavedata, 'frame_id':framedata})

    os.remove(path_generator)
    os.remove(path_infer)
    # print('Elapsed time:', datetime.now() - startTime)


def inference2(path,start,end,tag,sess,model_path,jobdir,dp_path):
    from deepinterpolation.deepinterpolation.generic import JsonSaver, ClassLoader
    import numpy as np
    import scipy.io as sio
    from scipy.io import loadmat

    generator_param = {}
    inferrence_param = {}

    # We are reusing the data generator for training here.
    generator_param["type"] = "generator"
    generator_param["name"] = "SingleTifGenerator"
    generator_param["pre_post_frame"] = 30
    generator_param["pre_post_omission"] = 0
    generator_param[
        "steps_per_epoch"
    ] = -1  # No steps necessary for inference as epochs are not relevant. -1 deactivate it.

    generator_param["train_path"] = path

    generator_param["batch_size"] = 1
    generator_param["start_frame"] = start
    generator_param["end_frame"] = end # -1 to go until the end.
    generator_param[
        "randomize"
    ] = 0  # This is important to keep the order and avoid the randomization used during training

    inferrence_param["type"] = "inferrence"
    inferrence_param["name"] = "core_inferrence"

    # Replace this path to where you stored your model
    inferrence_param["model_path"] = model_path

    dp_mat_path = dp_path
    inferrence_param["mat_file"] = dp_mat_path

    jobdir = jobdir #replace with your home directory

    try:
        os.mkdir(jobdir)
    except:
        print("folder already exists")

    path_generator = os.path.join(jobdir, "generator2_" + sess + tag +".json")

    json_obj = JsonSaver(generator_param)
    json_obj.save_json(path_generator)

    path_infer = os.path.join(jobdir, "inferrence2_" + sess + tag + ".json")
    json_obj = JsonSaver(inferrence_param)
    json_obj.save_json(path_infer)

    generator_obj = ClassLoader(path_generator)
    data_generator = generator_obj.find_and_build()(path_generator)

    inferrence_obj = ClassLoader(path_infer)
    inferrence_class = inferrence_obj.find_and_build()(path_infer, data_generator)

    # Except this to be slow on a laptop without GPU. Inference needs parallelization to be effective.

    old=loadmat(dp_mat_path)["inference_data"]
    old_id = loadmat(dp_mat_path)["frame_id"]
    new_id = data_generator.list_samples[0:len(data_generator)*5]
    framedata = np.concatenate([np.squeeze(old_id),new_id])
    out = inferrence_class.run()
    matdata = np.ascontiguousarray(out)
    matdata = matdata[:,data_generator.a:512-data_generator.a,data_generator.b:512-data_generator.b]
    old = np.ascontiguousarray(np.swapaxes(old, 1, 2))
    old = np.ascontiguousarray(np.swapaxes(old, 0, 1))
    matsavedata = np.concatenate([old,matdata],0)
    matsavedata = np.swapaxes(matsavedata, 0, 2)
    matsavedata = np.swapaxes(matsavedata, 0, 1)
    sio.savemat(dp_mat_path, mdict={'inference_data':matsavedata,
                                                        'frame_id':framedata})
    
    os.remove(path_generator)
    os.remove(path_infer)




if __name__ == "__main__":
    
    import sys
    import numpy as np
    import glob
    import requests
    import json
    from tqdm import tqdm
    # import tensorflow.python.keras.backend as K
    # import tensorflow as tf

    ######### edit lines here ##########

    # full path to home directory deepinterpolation folder
    jobdir = "/usr4/ugrad/kevry/Work/deepinterpolation"

    # file name of JSON creared
    json_file = os.path.join(jobdir, "pr065_files.json")

    # file name of .h5 model to use for inference
    # model_path = os.path.join(jobdir, "2021_03_22_13_24_transfer_mean_squared_error_rigid_test_train_bad.h5")
    model_path = "/net/claustrum2/mnt/data/Projects/Perirhinal/deepinterpolation/trained_models/Training_models/2021_03_22_13_24_transfer_mean_squared_error_rigid_test_train_bad.h5"

    # select drive to write dp.mat files to
    ## note: make sure to have entire file structure read/similar on the drive selected
    drive2select = 'W:'
    ##################################

    scc2localwind = {'X:': '/net/claustrum2/mnt/data', 'Y:': '/net/claustrum/mnt/data1', 'W:': '/net/claustrum3/mnt/data', 'V:': '/net/claustrum4/mnt/storage/data'}
    sccdriveselection = scc2localwind[drive2select]

    # read json
    f = open(json_file)
    data = json.load(f)
    f.close()

    task_id = int(os.environ["SGE_TASK_ID"])

    # old method ##
    if (task_id*6) < (len(data))-1:
        train_paths_td=data[(task_id-1)*6:task_id*6]
    else:
        train_paths_td=data[(task_id-1)*6:(len(data))]

    # train_paths_td = [data[(task_id - 1)]]

    for i, path in enumerate(tqdm(train_paths_td)):
        sess = (path.split('-'))[1].split('/')[0]
        tag=path.split("/")[-1].replace('.mat','')
        
        # modify new path to dp mat file
        dp_path = path.replace('.mat','_dp.mat')
        path_list = os.path.normpath(dp_path).split(os.sep)
        currentdrive = '/' + os.path.join(*path_list[:5])
        dp_path = dp_path.replace(currentdrive, sccdriveselection)

        # create directories for new path if they don't exist
        os.makedirs(os.path.dirname(dp_path), exist_ok = True)

        print('start pass 1')
        startTime=datetime.now()
        inference(path,tag,sess,model_path,jobdir,dp_path)
        print('time spent:', datetime.now() - startTime)

        print('start pass 2')
        mat_file = loadmat(path)['motion_corrected']
        dp_file= loadmat(dp_path)['inference_data']
        start=int(np.floor(float(mat_file.shape[2]-60)) / 5)*5 #to grab extra frames missed by batch size
        end = mat_file.shape[2]-1
        if (dp_file.shape[2] != mat_file.shape[2]-60):
            inference2(path,start,end,tag,sess,model_path,jobdir,dp_path)