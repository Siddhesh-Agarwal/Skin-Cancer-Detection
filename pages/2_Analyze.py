from PIL import Image
import streamlit as st
import tensorflow as tf

st.set_page_config(
    page_title="Skin Cancer Detection | Analyze",
    page_icon="♋",
    layout="centered",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("./model/model.keras")
    return model


LABELS = [
    "Actinic Keratosis",
    "Basal Cell Carcinoma",
    "Dermatofibroma",
    "Melanoma",
    "Nevus",
    "Pigmented Benign Keratosis",
    "Seborrheic Keratosis",
    "Squamous Cell Carcinoma",
    "Vascular Lesion",
]
OOD_THRESHOLD = 0.85  # tune this later

st.header("Analyze")
st.subheader("Upload an image to get a diagnosis")

pic = st.file_uploader(
    label="Upload a picture",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=False,
    help="Upload a picture of your skin to get a diagnosis",
)

if st.button("Predict"):
    if not pic:
        st.error("Please upload an image")
        st.stop()

    st.header("Results")

    with st.spinner("Loading model..."):
        model = load_model()

    with st.spinner("Processing image..."):
        img = Image.open(pic)
        img = img.resize((180, 180))
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = tf.expand_dims(img, axis=0)

        logits = model.predict(img)

        probs = tf.nn.softmax(logits, axis=-1)
        max_prob = tf.reduce_max(probs, axis=-1)
        max_prob_val = max_prob.numpy()[0]

    with st.spinner("Predicting..."):
        if max_prob_val < OOD_THRESHOLD:
            disease = "Unknown/Out-of-Distribution"
        else:
            pred_class = tf.argmax(probs, axis=1).numpy()[0]
            disease = LABELS[pred_class]
        score = round(max_prob_val * 100, 2)

    cols = st.columns([1, 2])
    with cols[0]:
        st.image(pic, caption=pic.name, width="stretch")

    with cols[1]:
        st.metric("Prediction", disease)
        st.metric("Confidence", f"{score:.2f}%")

    st.warning(
        "This is not a medical diagnosis. Please consult a doctor for a professional diagnosis.",
        icon="⚠️",
    )
