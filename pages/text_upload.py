import streamlit as st

import io
import apis.aws_api
import apis.dify_api


# Streamlit UI
st.title("Text Upload to AWS S3 Folder")

# File upload widget
uploaded_file = st.file_uploader("Choose an text file", type=["txt", "markdown", "pdf", "html", "xlsx", "xls", "docx", "csv", "eml", "msg", "pptx", "xml", "epub", "ppt", "md", "htm"])

if uploaded_file is not None:
    # Get file format and name
    file_name = uploaded_file.name

    # Upload text file to S3 when button is clicked
    if st.button('Upload to S3'):
        else:
            # Upload the image as binary stream (BytesIO object) to S3
            image_content = io.BytesIO()
            image.save(image_content, format='PNG')
            image_byte = image_content.getvalue()
            
            try:
                image_url = aws_api.upload_text_to_s3(image_byte, content_type, aws_api.IMAGE_BUCKET_NAME, aws_api.IMAGE_FOLDER_NAME, file_name)
                st.success(f"Image uploaded successfully to {aws_api.IMAGE_BUCKET_NAME}")
                st.write(f"Image URL: {image_url}")
                
                dify_code, dify_msg = dify_api.text_upload()
                if dify_code == 200:
                    st.write("Image information synchronized successfully in Dify")
                else:
                    st.write(dify_msg)
            except NoCredentialsError:
                st.error("Credentials not available")

if st.button("Back to Home"):
    st.switch_page("homepage.py")