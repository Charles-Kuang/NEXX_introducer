import streamlit as st

import io
from PIL import Image
import apis.aws_api
import apis.dify_api

from botocore.exceptions import NoCredentialsError

# Streamlit UI
st.title("Image Upload to AWS S3 Folder with Description")

# Image upload widget
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

# Input field for image description
image_description = st.text_area("Enter image description")

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Get image format and name
    file_name = uploaded_file.name

    # Upload image and description to S3 when button is clicked
    if st.button('Upload to S3'):
        if image_description.strip() == "":
            st.error("Please enter a description for the image.")
        else:
            # Upload the image as binary stream (BytesIO object) to S3
            image_content = io.BytesIO()
            image.save(image_content, format='PNG')
            image_byte = image_content.getvalue()
            
            try:
                image_url = aws_api.upload_image_to_s3(image_byte, image_description, aws_api.IMAGE_BUCKET_NAME, aws_api.IMAGE_FOLDER_NAME, file_name)
                st.success(f"Image uploaded successfully to {aws_api.IMAGE_BUCKET_NAME}")
                st.write(f"Image URL: {image_url}")
                
                dify_code, dify_msg = dify_api.image_upload(image_url, image_description)
                if dify_code == 200:
                    st.write("Image information synchronized successfully in Dify")
                else:
                    st.write(dify_msg)
            except NoCredentialsError:
                st.error("Credentials not available")

if st.button("Back to Home"):
    st.switch_page("homepage.py")
                    

