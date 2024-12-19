import streamlit as st
from workspace.model.model import Model
import uuid
# from utils.sqlit import init_db, save_chat, load_chat
#test
from utils.v1sqlite import init_db, save_chat, load_chat
def init():
    """
    初始化数据库和消息管理
    """
    
    # # 初始化数据库,加载历史消息
    init_db()
    #messages初始化
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # 会话初始化-如果没有 session_id，创建一个新的
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = st.query_params.get('session_id', [str(uuid.uuid4())])[0]    
#test
def display_chat_history(session_id=None):
    """
    展示当前或者历史记录
    """
    if session_id:
        chat_history = load_chat(session_id)
        for message in chat_history:
            st.markdown("User  :  "+ message["user_message"])
            st.markdown(f"{message['model_name']} : {message['model_response']}")
    else:
        # 默认显示当前会话的消息    
        for message in st.session_state["messages"]:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])
            elif message["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.markdown(f"{message['model_name']} : {message['content']}")
  
def clear_chat_history():
    """
    清空会话状态中的聊天历史
    """
    if "messages" in st.session_state:
        st.session_state["messages"] = []
        

def sidebar_chat_history():
    """
    渲染侧边栏聊天历史区：显示聊天历史
    """
    previous_sessions = set()#里边包含所有session_id并且不重复
    all_sessions = load_chat(None)
    for chat in all_sessions:
        previous_sessions.add(chat['session_id'])
        
    # 创建一个字典来存储每个session_id和对应的第一个用户消息的时间戳
    session_timestamps = {}

    for previous_session_id in previous_sessions:
        chat_history = load_chat(previous_session_id)
        if chat_history:
            first_user_timestamp = chat_history[0]['timestamp']
            session_timestamps[previous_session_id] = first_user_timestamp
            
    # 按时间戳排序会话ID
    sorted_sessions = sorted(session_timestamps.items(), key=lambda item: item[1], reverse=True)
    
    # 显示每个会话的部分用户消息，并允许点击查看历史记录
    for previous_session_id, first_user_timestamp in sorted_sessions:
        chat_history = load_chat(previous_session_id)
        if chat_history:
            first_user_message = chat_history[0]['user_message'][:8]  # 显示前8个字符
            if st.sidebar.button(f"会话{previous_session_id[:4]} {first_user_timestamp}: {first_user_message}"):
                display_chat_history(previous_session_id)  # 点击时加载该会话的完整历史

def sidebar_layout():
    if st.sidebar.button("清空聊天"):# 添加清空聊天历史按钮
        clear_chat_history()

    model_name = st.sidebar.selectbox("Model Selector", ["OpenAI", "Claude", "DeepSeek"])
    
    st.sidebar.title("聊天历史") 
    return model_name

if __name__ == "__main__":
    init()#初始化
    model_name = sidebar_layout()#侧边栏布局
    
    sidebar_chat_history()#加载所有会话记录

    display_chat_history()# 当前会话的聊天历史，否则只显示最新的问题和答案（目前聊天历史是session_state中的message）
    # 用户输入
    if user_message := st.chat_input("请输入您的问题"):
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(user_message)
        # 将用户消息存储到会话状态
        st.session_state['messages'].append({"role": "user", "content": user_message})
        # 显示模型回复
        with st.chat_message("assistant"):
            model = Model(provider=model_name)
            model_response = model(user_message)
            # #流式输出：
            # placeholder = st.empty()
            # response = ""
            # for chunk in model.stream({"content": user_input}):  # 假设模型逐步返回
            #     response += chunk["content"]
            #     placeholder.markdown(response)  # 实时更新前端内容
            #     time.sleep(0.02)
            st.markdown(model_name + "   :   " + model_response)

        # 将模型回复存储到会话状态
        st.session_state['messages'].append({"role": "assistant", "content": model_response,"model_name":model_name})
        # # 保存聊天记录到数据库
        save_chat(st.session_state['session_id'], model_name, user_message, model_response)
        
        
        
        




