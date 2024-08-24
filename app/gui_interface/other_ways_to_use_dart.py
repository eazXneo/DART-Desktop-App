# # 1. batched inference with the inference pipeline (faster than single images)
# from dart import get_inference_pipeline
# inference_pipeline = get_inference_pipeline(model_name='resnet18')
# # iterate over your torch style dataloader
# for batch_of_images in your_torch_data_loader:
#     batch_of_images.cuda()  # if using GPU
#     FD_of_batch = inference_pipeline(batch_of_images)[0]  # returns np array on cpu
#
# # 2. access the components of the inference pipeline themselves
# from dart import get_model_and_processing
# # this returns a dict containing the model, preprocessing and postprocessing pipelines, and config
# model_and_processing = get_model_and_processing(model_name='resnet18')
# your_image = ...
# your_image_preprocessed = model_and_processing['preprocessing'](your_image)
# FD_unscaled = model_and_processing['model'](your_image_preprocessed)
# FD_of_your_image = model_and_processing['postprocessing'](FD_unscaled)
#
# # 3. access just the model
# from dart import load_model
# # pytorch compatible model, e.g. for writing your own highly efficient inference loop
# # (with your own preprocessing and postprocessing, see the cfg for details)
# model = load_model(model_name='resnet18')