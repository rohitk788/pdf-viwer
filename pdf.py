import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import io

def convert_pdf_to_images(pdf_file):
    """Converts each page of the PDF to an image."""
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images = []
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        images.append(img)
    return images

def display_pdf(uploaded_file):
    """Displays the uploaded PDF with page navigation outside the PDF container."""
    if uploaded_file is not None:
        # Convert PDF to images
        images = convert_pdf_to_images(uploaded_file)

        # Initialize session state for page navigation
        if 'page_number' not in st.session_state:
            st.session_state.page_number = 0

        # Create a two-column layout
        col1, col2 = st.columns([1, 4])

        with col1:
            st.markdown("#### Page Links")
            for page_number in range(len(images)):
                if st.button(f"Page {page_number + 1}", key=f"page_link_{page_number}"):
                    st.session_state.page_number = page_number

        with col2:
            st.markdown("### PDF")
            # Display the selected page image
            st.image(images[st.session_state.page_number], caption=f"Page {st.session_state.page_number + 1}")

# Streamlit file uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
display_pdf(uploaded_file)
