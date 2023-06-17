from deepface import DeepFace
import pickle
 
def main():
    DeepFace.stream(db_path = "faces")

    with open('representation_vgg_face.pkl', 'rb') as file:
        obj = pickle.load(file)
        print(obj)
if __name__ == '__main__':
    main()