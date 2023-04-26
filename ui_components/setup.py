import streamlit as st
import os
from ui_components.common_methods import create_working_assets, get_timing_details
import streamlit as st
import os
from moviepy.editor import *

from repository.local_repo.csv_repo import get_app_settings, update_app_settings
from ui_components.components.app_settings_page import app_settings_page
from ui_components.components.batch_action_page import batch_action_page
from ui_components.components.custom_models_page import custom_models_page
from ui_components.components.frame_editing_page import frame_editing_page
from ui_components.components.frame_styling_page import frame_styling_page
from ui_components.components.key_frame_selection import key_frame_selection_page
from ui_components.components.new_project_page import new_project_page
from ui_components.components.project_settings_page import project_settings_page
from ui_components.components.prompt_finder_page import prompt_finder_page
from ui_components.components.timing_adjustment_page import timing_adjustment_page
from ui_components.components.video_rendering_page import video_rendering_page
from ui_components.components.welcome_page import welcome_page

def setup_app_ui():
       
    app_settings = get_app_settings()
    title1, title2 = st.sidebar.columns([3,2])
    with title1:
        st.title("Banodoco")    
    with title2:        
        st.write("")
        st.caption("Experiencing issues or have feedback? Please [let me know](mailto:peter@omalley.io)!")
           
    if int(st.session_state["welcome_state"]) in [0,1,2,3,4] and st.session_state["online"] == False:
        welcome_page()
    else:                
        video_list = [f for f in os.listdir("videos") if not f.startswith('.')]
        if "index_of_project_name" not in st.session_state:
            if app_settings["previous_project"] != "":
                st.session_state["project_name"] = app_settings["previous_project"] 
                st.session_state["index_of_project_name"] = video_list.index(app_settings["previous_project"])            
            else:
                st.session_state["index_of_project_name"] = 0
                
        st.session_state["project_name"] = st.sidebar.selectbox("Select which project you'd like to work on:", video_list,index=st.session_state["index_of_project_name"])  
        
        if st.session_state["index_of_project_name"] != video_list.index(st.session_state["project_name"]):
            st.write("Project changed")
            st.session_state["index_of_project_name"] = video_list.index(st.session_state["project_name"])               
            update_app_settings("previous_project", st.session_state["project_name"])
            st.experimental_rerun()
                
        if st.session_state["project_name"] == "":
            st.info("No projects found - create one in the 'New Project' section")
        else:  

            if not os.path.exists("videos/" + st.session_state["project_name"] + "/assets"):
                create_working_assets(st.session_state["project_name"])
            
            if "index_of_section" not in st.session_state:
                st.session_state["index_of_section"] = 0
                st.session_state["index_of_page"] = 0
            
            pages = [
            {
                "section_name": "Main Process",        
                "pages": ["Key Frame Selection","Frame Styling", "Frame Editing","Video Rendering"]
            },
            {
                "section_name": "Tools",
                "pages": ["Custom Models", "Prompt Finder", "Batch Actions","Timing Adjustment"]
            },
            {
                "section_name": "Settings",
                "pages": ["Project Settings","App Settings"]
            },
            {
                "section_name": "New Project",
                "pages": ["New Project"]
            }
            ]

            

            timing_details = get_timing_details(st.session_state["project_name"])

            st.session_state["section"] = st.sidebar.radio("Select a section:", [page["section_name"] for page in pages],horizontal=True)  
            st.session_state["page"] = st.sidebar.radio("Select a page:", [page for page in pages if page["section_name"] == st.session_state["section"]][0]["pages"],horizontal=False)
            
            mainheader1, mainheader2 = st.columns([3,2])
            with mainheader1:
                st.header(st.session_state["page"])   


            # APP ROUTING
            if st.session_state["page"] == "Key Frame Selection":
                key_frame_selection_page(mainheader2, st.session_state["project_name"])
            elif st.session_state["page"] == "App Settings":
                app_settings_page()
            elif st.session_state["page"] == "New Project":
                new_project_page()
            elif st.session_state["page"] == "Frame Styling":
                frame_styling_page(mainheader2, st.session_state["project_name"])
            elif st.session_state["page"] == "Video Rendering":
                video_rendering_page(mainheader2, st.session_state["project_name"])
            elif st.session_state["page"] == "Batch Actions":
                batch_action_page(st.session_state["project_name"])
            elif st.session_state["page"] == "Project Settings":
                project_settings_page(st.session_state["project_name"])
            elif st.session_state["page"] == "Custom Models":
                custom_models_page(st.session_state["project_name"])
            elif st.session_state["page"] == "Frame Editing":
                frame_editing_page(st.session_state["project_name"])
            elif st.session_state["page"] == "Timing Adjustment":
                timing_adjustment_page(st.session_state["project_name"])                                     
            elif st.session_state["page"] == "Prompt Finder":
                prompt_finder_page(st.session_state["project_name"])
            else:
                st.info("You haven't added any prompts yet. Add an image to get started.")
