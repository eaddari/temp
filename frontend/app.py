from urllib import response
import streamlit as st
import requests
import time, os, pandas as pd

class FrontEnd():
    def __init__(self):
        st.set_page_config(
            page_title="DocGen",
            page_icon="🤖",
        )
        st.title("Document Generation")
        self.__add_select_box()
        self.__add_description()
        self.__add_checkbox_pipeline()
        self.__add_form()

    def __add_select_box(self):
        st.sidebar.header("🗨️ Do you want to keep the comments?")
        self.keep_comments = st.sidebar.selectbox( 
            "Keep comments",
            ['Yes', 'No']
        )
    
    def __add_description(self):
        st.markdown(
            """
            DocGen è un'applicazione che ti consente di generare documentazione funzionale e tecnica incollando semplicemente l'URL di un repository pubblico o privato.
            """
        )
    
    def __add_form(self):
        with st.form("login_form"):
            self.url_repository = st.text_input("Link Repository")
            self.token = st.text_input("Token", type="password")
            submit = st.form_submit_button("Genera")
        if submit:
            if self.url_repository:
                st.success("Start!")
                
                self.__pipeline()
            else:
                st.error("You must fill in the required fields.")

    def __add_checkbox_pipeline(self):
        st.sidebar.header("⚙️ Pipeline Options")
        anonymization = st.sidebar.checkbox("Anonymization", value=True)
        file_converter = st.sidebar.checkbox("File Converter", value=True)
        python_to_text = st.sidebar.checkbox("Python to Text", value=True)
        text_cleaner = st.sidebar.checkbox("Text Cleaner", value=True)
        self.selected_components={
            "anonymization": anonymization,
            "file_converter": file_converter,
            "python_to_text": python_to_text,
            "text_cleaner": text_cleaner
        }

    def __pipeline(self):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_steps = 4
        
        try:
            status_text.text("Step 1/4: Downloading repository...")
            progress_bar.progress(1/total_steps)
            
            response = requests.post("http://input_integration_pipeline:8081/v1/download_repository", 
                                 json={'repository': self.url_repository, 'token': self.token})
            
            if "Repository successfully cloned." != response.json()['message']:
                status_text.error(f"Errore Step 1: {response.json()['message']}")
                progress_bar.empty()
                return 
            
            status_text.text("Step 1/4: Repository scaricato con successo ✓")
            time.sleep(0.5) 
            
            status_text.text("Step 2/4: Uploading repository...")
            progress_bar.progress(2/total_steps)
            
            response = requests.post("http://input_integration_pipeline:8081/v2/repo/upload", 
                                    params={"repo_path": response.json()["path"]})
            
            if response.json()["status"] == "error":
                status_text.error(f"Errore Step 2: {response.json()['error']}")
                progress_bar.empty()
                return 
            
            container: str = response.json()["container_name"]
            status_text.text("Step 2/4: Upload completato con successo ✓")
            time.sleep(0.5)
            
            status_text.text("Step 3/4: Transforming to parquet...")
            progress_bar.progress(3/total_steps)
            
            response = requests.post("http://input_integration_pipeline:8081/v3/transform-container-to-parquet",
                                    json={'container_name': container, 'single_parquet': True})
            
            st.info(f"Percorso Parquet: {response.json()['parquet_path']}")

            self.parquet_file = response.json()['parquet_path']

            status_text.text("Step 4/4: Evaluating Repository...")
            st.info(f"Selected pipeline: {self.selected_components}")
            self.__transforming_pipeline()
            progress_bar.progress(1.0)
            
        except requests.exceptions.RequestException as e:
            status_text.error(f"Errore di connessione: {str(e)}")
            progress_bar.empty()
        except KeyError as e:
            status_text.error(f"Errore nella risposta del server: chiave mancante {str(e)}")
            progress_bar.empty()
        except Exception as e:
            status_text.error(f"Errore imprevisto: {str(e)}")
            progress_bar.empty()
        
        
    def __transforming_pipeline(self):   

        body = {
            "input_path": self.parquet_file,
            "keep_comments": self.keep_comments,
            "steps": [key for key, value in self.selected_components.items() if value == True]
        }

        try:
            api_url = "http://transforming_pipeline:8082/v5/transforming_pipeline"
            response = requests.post(api_url, json=body)
            path = response.json()["data"]["path"]
            df = pd.read_parquet(path)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    FrontEnd()