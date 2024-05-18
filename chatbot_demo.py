import streamlit as st
import json
import time
import os

# Streamlit App 页面显示的大标题
st.title(":robot_face: DeepSeek-Chat", anchor=False)

# 设定 Json 文件路径
file_path = "data.json"

# 根据实际情况修改
# 设定 api_key
# api_key = os.environ.get("DEEPSEEK_API_KEY")
# 设定 DeepSeek 服务器地址
# base_url="https://api.deepseek.com"
# 初始化客户端
# client = OpenAI(api_key=api_key, base_url=base_url)

# 聊天目的选项，用于 => st.selectbox("Chat Purpose") ---------- 可用可不用
purpose_options = []
purpose_dict = [
    {"purpose": "General Chat", "temperature": 1.00},
    {"purpose": "Translation", "temperature": 1.10},
    {"purpose": "Creative Writing", "temperature": 1.25},
    {"purpose": "Coding or Math", "temperature": 0.00},
    {"purpose": "Data Analysis", "temperature": 0.70}
]
for item in purpose_dict:
    purpose_options.append(item["purpose"])

# 设定 messages 缓存
if "messages" not in st.session_state:
    st.session_state.messages = []
# 定义一个变量来接收 messages 缓存
chatlog_cache = st.session_state.messages
# 设定 option_cache 缓存
if "option_cache" not in st.session_state:
    st.session_state.option_cache = []

# ---------- 以下是函数部分 ----------
# --- 对话数据处理部分 ---
# 函数：读取 Json 文件
def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            json_data = json.load(file)
    except:
        json_data = []
    return json_data
# 函数：检查 Json 文件是否存在，Json 数据是否为空
def check_json(file_path):
    try:
        json_data = read_json(file_path)
    except:
        json_data = []
    return json_data
# 函数：储存对话数据 => 由 st.button("New Chat") 来执行函数
def save_chatlog(file_path, new_chatlog):
    new_chatlog_set = new_chatlog
    json_data = check_json(file_path)
    if not isinstance(json_data, list):
        json_data = []
    json_data.append(new_chatlog_set)
    with open(file_path, 'w') as file:
        json.dump(json_data, file)
# 函数：读取数据并存储到 st.session_state.option_cache => 服务于选择器 st.selectbox("Conversation History")
def load_json_data_to_cache(file_path):
    json_data = read_json(file_path)
    if isinstance(json_data, list):
        st.session_state.option_cache = json_data
# 函数：历史对话记录选择器的选项 => 服务于选择器 st.selectbox("Conversation History")
def selectbox_option():
    options = []
    for index, msg_set in enumerate(st.session_state.option_cache):
        first_user_msg = next((msg for msg in msg_set if msg.get('role') == 'user'), None)
        if first_user_msg:
            options.append(f"Conversation #{index + 1} - User: {first_user_msg['content']}")
    return options
# 函数：召回聊天记录 => 由 st.button("Submit") 来执行函数
def callback_chatlog():
    split_result = chatlog_selectbox.split(": ")
    if len(split_result) > 1:
        selected_content = split_result[1]
        for index, msg_set in enumerate(st.session_state.option_cache):
            if any(msg["content"] == selected_content for msg in msg_set if msg.get("role") == "user"):
                for msg in msg_set:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"], unsafe_allow_html=True)
                return msg_set
    else:
        return st.warning("Selected conversation not found.")

# 函数：删除选中的聊天记录 => 由 st.button("Delete") 来执行函数
def delete_chatlog():
    split_result = chatlog_selectbox.split(": ")
    if len(split_result) > 1:
        selected_content = split_result[1]
        cache_copy = st.session_state.option_cache.copy()
        for msg_set in cache_copy:
            if any(msg["content"] == selected_content for msg in msg_set if msg.get("role") == "user"):
                st.session_state.option_cache.remove(msg_set)
                break
        with open(file_path, 'w') as file:
            json.dump(st.session_state.option_cache, file)
    else:
        return st.warning("Selected conversation not found.")
# 函数：删除全部历史聊天记录数据
def delete_all_chatlog():
    st.session_state.option_cache = []
    st.session_state.messages = []
    with open(file_path, "w") as file:
        json.dump([], file)
# --- 对话数据处理结束 ---
# 根据实际情况修改
# 函数：会话响应并接收大模型回复
# def response(messages,max_tokens,temperature,top_p,frequency_penalty,presence_penalty):
    # chat_comletion = client.chat.completions.create(
        # model="deepseek-chat",
        # messages=messages,
        # max_tokens=max_tokens,
        # temperature=temperature,
        # top_p=top_p,
        # frequency_penalty=frequency_penalty,
        # presence_penalty=presence_penalty,
        # stop=None,
        # stream=False
    # )
    # response = chat_comletion.choices[0].message.content
    # return response

# 曲线救国
def newchat_onclick():
    value = len(st.session_state.messages)
    st.info(f"你刚才聊了 {value} 条！")
    if st.button("Close", key="close"):
        st.rerun()
# ---------- 以上是函数部分 ----------

# ---------- 以下是侧边栏控件部分 ----------
with st.sidebar:
    # 新对话按钮，兼顾对话数据保存
    newchat_button = st.button("New Chat", key="newchat", type="primary", use_container_width=True, on_click=newchat_onclick)
    # 系统提示词输入框
    system_prompt = st.text_area("System Prompt", value="You are a helpful assistant.")
    # 历史对话选择器，配合 load_json_data_to_cache(file_path) 和 selectbox_option() 函数
    load_json_data_to_cache(file_path)
    options = selectbox_option()
    chatlog_selectbox = st.selectbox("Conversation History", options, index=None)
    # 提交按钮，提交并召回历史对话
    submit_button = st.button("Submit", key="submit", use_container_width=True, help="点击查看你选择的历史对话")
    # -- 让下面两个按钮水平放置 --
    col1, col2 = st.columns(2)
    # 删除所选历史对话的按钮
    with col1:
        delete_one_button = st.button("Delete", key="delete", use_container_width=True, help="点击删除你选择的历史对话！")
    # 删除全部历史对话的按钮
    with col2:
        delete_all_button = st.button("Delete All", key="deleteall", use_container_width=True, help="点击删除全部历史对话！")
    # 聊天目的选择器
    chat_purpose = st.selectbox("Chat Purpose", purpose_options, key="chatpurpose", index=0, help="来自 DeepSeek 官方建议")
    # 对话温度调节器
    for item in purpose_dict:
        if item["purpose"] == chat_purpose:
            temp_value = item["temperature"]
    temperature = st.slider("Temperature", 0.00, 2.00, temp_value, step=0.01)
    # Top P 调节器
    top_p = st.slider("Top P", 0.10, 1.00, 1.00, step=0.01)
    # 最大 tokens 调节器
    max_tokens = st.slider("Max Tokens", 1, 32000, 4096, step=1, disabled=True, help="目前 DeepSeek 仅支持设置为 4096")
    # Frequency Penalty 调节器
    frequency_penalty = st.slider("Frequency Penalty", -2.00, 2.00, 0.00, step=0.01, help="一般不调")
    # Presence Penalty 调节器
    presence_penalty = st.slider("Presence Penalty", -2.00, 2.00, 0.00, step=0.01, help="一般不调")
# ---------- 以上是侧边栏控件部分 ----------


# 根据实际情况修改
# 用户输入，并执行会话响应的函数
# user_input = st.chat_input("Say something...")
# if user_input:
    # st.session_state.messages.append({"role": "user", "content": user_input}) # 缓存用户的消息
    # messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages # 将系统提示词和消息缓存进行合并
    # with st.spinner("Send..."):
        # response = response(messages,max_tokens,temperature,top_p,frequency_penalty,presence_penalty) # 执行会话响应
    # st.session_state.messages.append({"role": "assistant", "content": response}) # 缓存大模型的回复
    # 在页面上渲染对话消息
    # for messages in st.session_state.messages:
        # with st.chat_message(messages["role"]):
            # st.markdown(messages["content"], unsafe_allow_html=True)

# --------------- 模拟与大模型的对话，实际使用时要删掉 ---------------
user_input = st.chat_input("Say something...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = f"你干嘛~哎呦！你说的是“{user_input}”。我不理解，但大为震撼！"
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.spinner("Processing..."):
        time.sleep(1.5)
        for messages in st.session_state.messages:
            with st.chat_message(messages["role"]):
                st.markdown(messages["content"], unsafe_allow_html=True)

# 编排 newchat_button 处理逻辑
if newchat_button:
    save_chatlog(file_path, chatlog_cache)
    st.session_state.messages = []
    st.toast("对话已保存！")
    st.toast("已开始新对话！")

# 编排 submit_button 处理逻辑
if chatlog_selectbox and submit_button:
    st.session_state.messages = []
    return_button = st.button("Return", key="return", help="返回")
    msg_set = callback_chatlog()
    st.session_state.messages = msg_set
    if return_button:
        st.session_state.messages = []
        st.rerun()

# 编排 delete_one_button 处理逻辑
if delete_one_button:
    delete_chatlog()
    st.session_state.messages = []
    st.success("Done!")

# 编排 delete_all_button 处理逻辑
if delete_all_button:
    delete_all_chatlog()
    st.success("Done!")