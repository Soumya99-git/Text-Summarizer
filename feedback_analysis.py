import pickle
import os

def feedback(s):
    os.chdir(r"c:\Users\Soumya Chatterjee\Desktop\INFRAMIND\PROJECT")
    model_path = "model.sav"
    model = pickle.load(open(model_path,"rb"))
    return(model.predict([s])[0])


if __name__ == "__main__":
    print(feedback("this is a good problem"))