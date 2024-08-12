import streamlit as st
from business_logic import check_content_safety

# Set the title of the app
st.title("Elite Fooders")

# Create placeholders for the image and text at the top
image_placeholder = st.empty()
text_placeholder = st.empty()

# Create a file uploader for the image
uploaded_image = st.file_uploader("Upload Recipe/Experience", type=["png", "jpg", "jpeg"], key="uploaded_image")

# Create a text input for the text
text_input = st.text_input("Share Thoughts", placeholder="Quiche Lorraine, a French classic with a buttery crust.", key="text_input")

# Initialize session states
if "appeal_requested" not in st.session_state:
    st.session_state.appeal_requested = False

if "request_processed" not in st.session_state:
    st.session_state.request_processed = 0

if "request_response" not in st.session_state:
    st.session_state.request_response = None

def appeal_click_button():
    st.session_state.appeal_requested = True

# Create a submit button
if st.button("Submit"):
    if uploaded_image is not None and text_input:
        with st.spinner('Processing...'):
            # Check for the content safety
            moderation_response = check_content_safety(text=text_input, image_data=uploaded_image.getvalue())
            st.session_state.request_response = moderation_response
            st.session_state.request_processed = 1     
    else:
        st.warning("Please upload an image and enter some text before submitting.")

# Display the uploaded image and text at the top
if st.session_state.request_processed != 0:
    text_input = st.session_state.text_input
    uploaded_image = st.session_state.uploaded_image
    image_placeholder.image(uploaded_image, caption="Uploaded Image", width=250)
    text_placeholder.write("Entered Text: " + text_input)


# Display Post uploaded successful message
if st.session_state.request_processed == 1 and st.session_state.request_response is None:
    st.write("Post Upload Successful")

# Display Post upload failure message
if st.session_state.request_processed == 1 and st.session_state.request_response is not None:
    st.warning("Post Upload Failed")

    if st.session_state.request_response["status"] == "re-evaluation needed":
        st.write("Possible community guidelines violation found. Your post has been sent to our team for evaluation!")
        st.write("Please be patient. We'll get back soon")

    if st.session_state.request_response["status"] == "violations found":
        st.write(f"Failure Reason: {st.session_state.request_response["details"]}")
        st.subheader("Think the evaluation is not correct")
        st.write("Submit an Appeal for it to be re-evaluated by a human")

        if st.session_state.request_processed == 1 and not st.session_state.appeal_requested:
            st.button("Appeal", on_click=appeal_click_button)
        else:
            # Display appeal request message if appeal was requested
            st.info("Appeal request successfully generated! You will hear from us soon.")
