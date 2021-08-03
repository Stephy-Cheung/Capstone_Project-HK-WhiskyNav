#%%
import tensorflow as tf
import numpy as np
import pathlib, os, json, pickle
# import IPython.display as display
# import matplotlib.pyplot as plt
import pandas as pd
# import streamlit as st
from PIL import Image

#%%
# ***================= Steamlit image upload =================***
# img_file = st.file_uploader('Upload a whisky image')
# if img_file != None:
def classifier(img_file):
    img_temp = Image.open(img_file)
    img_temp = img_temp.convert('RGB')
    img_temp.save('./testing/test1/1.jpg')
    # with open(os.path.join('testing/test1/','1.jpg'), 'wb') as file:
        # file.write(img_file.getbuffer())
        

    #%%
    # ***================= Loading top 100 list =================***
    df = pd.read_csv('dataset/top100_whisky.csv', sep=',')
    top100 = [i.lower().replace(' ', '_') for i in (df['Name'] + ' ' + df['Year'])]
    #%%
    # ***================= Loading the model =================***
    model = tf.keras.models.load_model('checkpoint/weightings.h5') # load the model structure and weight
    with open(os.path.join('checkpoint','label_to_index.txt'),'r') as file: # load the trained labels
        label_names = json.loads(file.read())
    label_names = {y:x for x, y in label_names.items()} # transform from label:number to number:label

    #%%
    # ***================= Classify the whisky in testing folder =================***

    #============ Creating image file reader ============
    def preprocess_image(image): # Input an image, resize it to 224, normalize the data from 0-255 to 0-1
        image = tf.image.decode_jpeg(image, channels=3)
        image = tf.image.crop_to_bounding_box(image,int(image.shape[0]*0.2),0,int(image.shape[0]*0.6),int(image.shape[1])) # Cutting the left 20% and right 20% out
        # plt.imshow(image.numpy(), cmap='gray') # Print the cut image for testing
        # plt.show()
        image = tf.image.resize(image, [224, 224])
        image /= 255.0
        return image

    def load_and_preprocess_image(path): # Input a path, read the image, and preprocess it
        image = tf.io.read_file(path)
        return preprocess_image(image)

    #============ Classifying the whisky ============
    testing_root = pathlib.Path('testing/')
    all_testing_paths = [str(path) for path in list(testing_root.glob('*/*'))]

    pred_list = []
    for i in range(len(all_testing_paths)):
        img = load_and_preprocess_image(all_testing_paths[i])
        # display.display(display.Image(all_testing_paths[i]))
        # st.image('testing/test1/1.jpg')
        img = np.reshape(img, [1,224,224,3])
        pred_list.append(label_names[np.argmax(model.predict(img))])
        test = enumerate(model.predict(img).tolist()[0])
        # st.text(f'Whisky detected: {pred_list[-1]}')
        if pred_list[-1] == 'not_whisky': # not_whisky doesn't have rank
            # st.text('N/A')
            return 'N/A'
        else:
            return top100.index(pred_list[-1])
            # st.text(top100.index(pred_list[-1])) # Output the rank in top 100
# %%
# ***================= Plotting accuracy/loss of the trained model =================***
# with open('checkpoint/history', 'rb') as file:
#     previous_history = pickle.load(file)

# acc = previous_history["accuracy"]
# val_acc = previous_history['val_accuracy']
# loss = previous_history['loss']
# val_loss = previous_history['val_loss']

# plt.figure(figsize=(8, 5))
# plt.subplot(1, 1, 1)
# plt.plot(acc, label='Training Accuracy')
# plt.plot(val_acc, label='Validation Accuracy')
# plt.legend(loc='lower right')
# plt.suptitle('Performance of the neural network under new approach')
# plt.xticks(np.arange(len(acc)), np.arange(1, len(acc)+1))
# plt.xlabel('epoch')
# plt.ylabel('Accuracy')
# plt.ylim([min(plt.ylim()),1])
# plt.title('Training and Validation Accuracy')

# plt.subplot(2, 1, 2)
# plt.plot(loss, label='Training Loss')
# plt.plot(val_loss, label='Validation Loss')
# plt.legend(loc='upper right')
# plt.xticks(np.arange(len(loss)), np.arange(1, len(loss)+1))
# plt.ylabel('Loss')
# plt.ylim([0,max(plt.ylim())])
# plt.title('Training and Validation Loss')
# plt.xlabel('epoch')
# plt.show()
# %%
