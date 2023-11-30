import streamlit as st
import numpy as np
import cv2
import xml.etree.ElementTree as ET
import math


# Function to annotate image from XML data
def annotate_image_from_xml(image, xml_data):
    tree = ET.parse(xml_data)
    root = tree.getroot()

    class_colors = {
        "brick": (255, 0, 0),
        "concrete": (0, 255, 0),
        "tile": (0, 0, 255),
        "general_w": (255, 255, 0),
        "plastic": (255, 0, 255),
        "stone": (0, 255, 255),
        "gypsum_board": (128, 0, 128),
        "pipes": (255, 165, 0),
        "wood": (128, 42, 42),
        "foam": (0, 128, 128)
    }

    for object_tag in root.findall('object'):
        class_name = object_tag.find('name').text
        color = class_colors.get(class_name, (255, 255, 255))

        polygon = object_tag.find('polygon')
        points = []
        i = 1
        while True:
            x = polygon.find(f'x{i}')
            y = polygon.find(f'y{i}')
            if x is None or y is None:
                break
            x_val = math.floor(float(x.text))
            y_val = math.floor(float(y.text))
            points.append((x_val, y_val))
            i += 1

        if points:
            cv2.polylines(image, [np.array(points)], isClosed=True, color=color, thickness=4)
            cv2.putText(image, class_name, points[0], cv2.FONT_HERSHEY_SIMPLEX, 2.5, color, 6)

    return image


# Streamlit UI
def main():

    st.set_page_config(layout="wide", page_title="CODD Annotation Reader")
    st.title('CODD Annotation Reader')
    st.header('View selected image from the CODD with its associated annotations')

    # Sidebar with explanations
    with st.sidebar:
        st.write("## About the CODD Annotation Reader")
        st.write("""
            This application allows you to upload an image from the CODD dataset along with its corresponding XML file containing annotations. 
            It displays the original image (left) and annotated image (right).
        """)

        st.write("## How to Use")
        st.write("""
            - Upload an image in JPG format.
            - Upload the corresponding XML file with annotations.
            - View the original and annotated images side by side.
        """)
    with st.sidebar:
        st.write("### CDW Classes:")
        st.markdown('Concrete')
        st.markdown('Brick')
        st.markdown('Tiles')
        st.markdown('Stones')
        st.markdown('Plaster board')
        st.markdown('Foam')
        st.markdown('Wood')
        st.markdown('Pipes')
        st.markdown('Plastic')
        st.markdown('General Waste')

    # Image and XML file uploaders
    uploaded_file = st.file_uploader("Upload your image (jpg format)", type=['jpg'])
    xml_file = st.file_uploader("Upload XML file with annotations", type=['xml'])

    # Displaying images
    if uploaded_file and xml_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        original_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        col1, col2 = st.columns(2)
        with col1:
            st.image(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB), caption='Fig.1 Original Image')

        annotated_image = annotate_image_from_xml(original_image.copy(), xml_file)
        with col2:
            st.image(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB), caption='Fig.2 Annotated Image')

    # Code snippet at the bottom
    st.markdown("---")
    st.subheader("Code Snippet")
    code = ''' 
import streamlit as st
import numpy as np
import cv2
import xml.etree.ElementTree as ET
import math

# Function to annotate image from XML data
def annotate_image_from_xml(image, xml_data):
    tree = ET.parse(xml_data)
    root = tree.getroot()

    class_colors = {
        "brick": (255, 0, 0),
        "concrete": (0, 255, 0),
        "tile": (0, 0, 255),
        "general_w": (255, 255, 0),
        "plastic": (255, 0, 255),
        "stone": (0, 255, 255),
        "gypsum_board": (128, 0, 128),
        "pipes": (255, 165, 0),
        "wood": (128, 42, 42),
        "foam": (0, 128, 128)
    }

    for object_tag in root.findall('object'):
        class_name = object_tag.find('name').text
        color = class_colors.get(class_name, (255, 255, 255))

        polygon = object_tag.find('polygon')
        points = []
        i = 1
        while True:
            x = polygon.find(f'x{i}')
            y = polygon.find(f'y{i}')
            if x is None or y is None:
                break
            x_val = math.floor(float(x.text))
            y_val = math.floor(float(y.text))
            points.append((x_val, y_val))
            i += 1

        if points:
            cv2.polylines(image, [np.array(points)], isClosed=True, color=color, thickness=2)
            cv2.putText(image, class_name, points[0], cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    return image
    '''
    st.code(code, language='python')

if __name__ == '__main__':
    main()
