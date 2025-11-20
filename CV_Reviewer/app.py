from pathlib import Path
import tempfile
import streamlit as st
import pymupdf4llm
from agno.agent import Agent
from agno.models.openai import OpenAIChat

system_prompt = ""
with open("sys_prompt.md", "r", encoding="utf-8") as f:
    system_prompt = f.read()

DEFAULT_BASE_URL = "http://127.0.0.1:1234/v1"
DEFAULT_API_KEY = "whatever"
DEFAULT_MODEL_ID = "qwen3-14b"

if "base_url" not in st.session_state:
    st.session_state["base_url"] = DEFAULT_BASE_URL
if "api_key" not in st.session_state:
    st.session_state["api_key"] = DEFAULT_API_KEY
if "model_id" not in st.session_state:
    st.session_state["model_id"] = DEFAULT_MODEL_ID
if "agent" not in st.session_state:
    st.session_state["agent"] = Agent(
        name="CV_Reviewer",
        model=OpenAIChat(base_url=st.session_state["base_url"], api_key=st.session_state["api_key"], id=st.session_state["model_id"]),
        instructions=system_prompt,
        markdown=True,
    )

def to_markdown_from_upload(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix == ".pdf":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        md = pymupdf4llm.to_markdown(Path(tmp_path))
        Path(tmp_path).unlink(missing_ok=True)
        return md
    if suffix in [".md", ".txt"]:
        data = uploaded_file.read()
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data.decode("latin-1")
    return None

st.set_page_config(page_title="CV Reviewer", layout="wide")
left, center, right = st.columns([1, 1, 1])
with center:
    lang = st.radio("语言 Language", options=["中文", "English"], index=0, horizontal=True)

texts = {
    "中文": {
        "title": "简历评审",
        "upload_jd": "上传JD文件",
        "upload_cv": "上传简历文件",
        "analyze": "分析",
        "warn_both": "请同时上传JD和简历",
        "error_type": "仅支持pdf、md、txt文件",
        "spinner": "分析中...",
        "score_label": "评分",
        "jd_label": "目标岗位JD",
        "cv_label": "候选人简历",
        "answer_lang": "请用中文回答，并使用markdown格式输出",
        "sidebar_title": "模型配置",
        "base_url": "API Base URL",
        "api_key": "API Key",
        "model_id": "模型ID",
        "confirm": "确认",
        "fill_all": "请填写所有配置项",
        "confirmed": "已完成，可以进行下一步"
    },
    "English": {
        "title": "CV Reviewer",
        "upload_jd": "Upload JD file",
        "upload_cv": "Upload CV file",
        "analyze": "Analyze",
        "warn_both": "Please upload both JD and CV",
        "error_type": "Only pdf, md, txt are supported",
        "spinner": "Analyzing...",
        "score_label": "Score",
        "jd_label": "Job Description (JD)",
        "cv_label": "Candidate CV",
        "answer_lang": "Answer in English and use markdown",
        "sidebar_title": "Model Configuration",
        "base_url": "API Base URL",
        "api_key": "API Key",
        "model_id": "Model ID",
        "confirm": "Confirm",
        "fill_all": "Please fill all fields",
        "confirmed": "Done. You can proceed."
    }
}

st.title(texts[lang]["title"])

with st.sidebar:
    st.subheader(texts[lang]["sidebar_title"])
    input_base_url = st.text_input(texts[lang]["base_url"], value=st.session_state["base_url"])
    input_api_key = st.text_input(texts[lang]["api_key"], value=st.session_state["api_key"], type="password")
    input_model_id = st.text_input(texts[lang]["model_id"], value=st.session_state["model_id"])
    confirm_cfg = st.button(texts[lang]["confirm"])
    if confirm_cfg:
        if not input_base_url or not input_api_key or not input_model_id:
            st.error(texts[lang]["fill_all"])
        else:
            st.session_state["base_url"] = input_base_url
            st.session_state["api_key"] = input_api_key
            st.session_state["model_id"] = input_model_id
            st.session_state["agent"] = Agent(
                name="CV_Reviewer",
                model=OpenAIChat(base_url=input_base_url, api_key=input_api_key, id=input_model_id),
                instructions=system_prompt,
                markdown=True,
            )
            st.success(texts[lang]["confirmed"])
    jd_file = st.file_uploader(texts[lang]["upload_jd"], type=["pdf", "md", "txt"])
    cv_file = st.file_uploader(texts[lang]["upload_cv"], type=["pdf", "md", "txt"])

analyze = st.button(texts[lang]["analyze"])

if analyze:
    if not jd_file or not cv_file:
        st.warning(texts[lang]["warn_both"])
    else:
        jd_md = to_markdown_from_upload(jd_file)
        cv_md = to_markdown_from_upload(cv_file)
        if jd_md is None or cv_md is None:
            st.error(texts[lang]["error_type"])
        else:
            with st.spinner(texts[lang]["spinner"]):
                prompt = f"{texts[lang]['answer_lang']}\n{texts[lang]['jd_label']}:\n{jd_md}\n{texts[lang]['cv_label']}:\n{cv_md}"
                result = st.session_state["agent"].run(prompt).content

            st.markdown(result)